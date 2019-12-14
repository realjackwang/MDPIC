# encoding = utf-8
# =====================================================
#   Copyright (C) 2019 All rights reserved.
#
#   filename : mdpic.py
#   version  : 0.1
#   author   : Jack Wang / 544907049@qq.com
#   date     : 2019/5/12 下午 1:26
#   desc     : 
# =====================================================

import os
import wx
import wx.adv
import yaml
import datetime

from threading import Thread, Timer
from PIL import ImageGrab
from pynput import keyboard
from git import Repo
from pyperclip import copy

current_key_pressed = []  # 当前按下的按键
github_username = ''  # 填入你的github的用户名
repository_name = ''
keycode = {}
hotkey = ''
repo = Repo(os.getcwd())
git = repo.git
listener = None
text = ''


def write_keycode():
    # key code for function keys
    for i in range(1, 13):
        keycode['f' + str(i)] = 111 + i
    # key code for letter keys
    for i in range(26):
        keycode[chr(97 + i)] = 65 + i
    keycode['ctrl'] = 162
    keycode['alt'] = 164


def init():
    write_keycode()
    with open('config.yml', 'r', encoding='utf-8') as f:
        cont = f.read()
        config = yaml.load(cont, Loader=yaml.BaseLoader)
        try:
            global github_username, repository_name, hotkey, text
            github_username = config['github_username']
            repository_name = config['repository_name']
            hotkey = config['hotkey'].lower().split('+')
            language = config['language']
            with open('language/'+language + '.yml', 'r', encoding='utf-8') as f:
                cont = f.read()
                config = yaml.load(cont, Loader=yaml.BaseLoader)
                global text
                text = [config['Info'],
                        config['Exit'],
                        config['Upload Clipboard To GitHub'],
                        config['config.yml is not complete yet, please fill it']]

            for i in range(len(hotkey)):
                hotkey[i] = keycode[hotkey[i]]
        except KeyError:
            pass


def savepic(window):
    try:
        im = ImageGrab.grabclipboard()
        filename = '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())
        im.save(r'images/image_' + str(filename) + '.png')
        ThreadUpload('images\\image_' + str(filename) + '.png', window)
        copy(
            'https://raw.githubusercontent.com/' + github_username + '/' + repository_name + '/master/images/image_' + str(
                filename) + '.png')
    except:
        wx.CallAfter(window.Failed)


def is_pressed():
    for key in hotkey:
        if key not in current_key_pressed:
            return False
    return True


class ThreadKey(Thread):
    def __init__(self, window):
        Thread.__init__(self)
        self.window = window
        self.start()  # start the thread

    def run(self):
        global listener
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()

    def on_release(self, key):
        try:
            if key.value.vk in current_key_pressed:
                current_key_pressed.remove(key.value.vk)
        except AttributeError:
            if key.vk in current_key_pressed:
                current_key_pressed.remove(key.vk)

    def on_press(self, key):
        try:
            if key.value.vk not in current_key_pressed:
                current_key_pressed.append(key.value.vk)
        except AttributeError:
            if key.vk not in current_key_pressed:
                current_key_pressed.append(key.vk)

        if is_pressed():
            wx.CallAfter(self.window.Uploading)
            savepic(self.window)


class ThreadUpload(Thread):
    def __init__(self, filename, window):
        Thread.__init__(self)
        self.filename = filename
        self.window = window
        self.start()  # start the thread

    def run(self):
        try:
            git.pull()
            git.add(os.path.join(os.getcwd(), self.filename))
            git.commit('-m', 'Add ' + self.filename)
            git.push()
            wx.CallAfter(self.window.UploadSuccess)
        except:
            wx.CallAfter(self.window.Uploading)


class Trans(wx.Frame):
    def __init__(self, parent, title=' ', size=(700, 500)):
        wx.Frame.__init__(self, parent, title=title, size=size, style=wx.STAY_ON_TOP)

        label_user = wx.StaticText(self, -1, title, pos=(0, 0))

        # self.Text = wx.TextCtrl(self, size=(700, 500))
        # self.Text.SetBackgroundColour('Black'), self.Text.SetForegroundColour('Steel Blue')
        self.SetTransparent(100)  # 设置透明


class MyTaskBarIcon(wx.adv.TaskBarIcon):
    ICON = "logo.ico"  # 图标地址
    ID_ABOUT = wx.NewIdRef()  # 菜单选项“关于”的ID
    ID_EXIT = wx.NewIdRef()  # 菜单选项“退出”的ID
    ID_SHOW_WEB = wx.NewIdRef()  # 菜单选项“显示页面”的ID
    TITLE = "MDPIC"  # 鼠标移动到图标上显示的文字

    def __init__(self):
        wx.adv.TaskBarIcon.__init__(self)

        self.SetIcon(wx.Icon(self.ICON), self.TITLE)  # 设置图标和标题
        self.Bind(wx.EVT_MENU, self.onAbout, id=self.ID_ABOUT)  # 绑定“关于”选项的点击事件
        self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_EXIT)  # 绑定“退出”选项的点击事件
        self.Bind(wx.EVT_MENU, self.onShowWeb, id=self.ID_SHOW_WEB)  # 绑定“显示页面”选项的点击事件

        if github_username == '' or repository_name == '':
            wx.MessageBox(text[3], "Warning")
            wx.Exit()

        self.frame2 = Trans(parent=None, title='上传中', size=(50, 20))
        self.frame2.Center()
        self.frame2.Show(False)

        self.frame3 = Trans(parent=None, title='上传成功', size=(50, 20))
        self.frame3.Center()
        self.frame3.Show(False)

        self.frame4 = Trans(parent=None, title='上传失败', size=(50, 20))
        self.frame4.Center()
        self.frame4.Show(False)

        ThreadKey(self)

    # “关于”选项的事件处理器
    def onAbout(self, event):
        wx.MessageBox('Author：Jack Wang\nEmail Address：544907049@qq.com\nLatest Update：2019-5-12', "info")

    # “退出”选项的事件处理器
    def onExit(self, event):
        global listener
        listener.stop()
        wx.Exit()

    # “显示页面”选项的事件处理器
    def onShowWeb(self, event):
        savepic()

    # 创建菜单选项
    def CreatePopupMenu(self):
        menu = wx.Menu()
        for mentAttr in self.getMenuAttrs():
            menu.Append(mentAttr[1], mentAttr[0])
        return menu

    # 获取菜单的属性元组
    def getMenuAttrs(self):
        return [(text[2], self.ID_SHOW_WEB),
                (text[0], self.ID_ABOUT),
                (text[1], self.ID_EXIT)]

    def Uploading(self):
        pos = wx.GetMousePosition()
        pos = (pos[0] + 15, pos[1])
        self.frame2.SetPosition(pos)

        def timestop():
            self.frame2.Show(False)
            timer.cancel()

        self.frame2.Show(True)
        timer = Timer(2.0, timestop)
        timer.start()

    def UploadSuccess(self):
        pos = wx.GetMousePosition()
        pos = (pos[0] + 15, pos[1])
        self.frame3.SetPosition(pos)

        def timestop():
            self.frame3.Show(False)
            timer.cancel()

        self.frame3.Show(True)
        timer = Timer(2.0, timestop)
        timer.start()

    def UploadFailed(self):
        pos = wx.GetMousePosition()
        pos = (pos[0] + 15, pos[1])
        self.frame4.SetPosition(pos)

        def timestop():
            self.frame4.Show(False)
            timer.cancel()

        self.frame4.Show(True)
        timer = Timer(2.0, timestop)
        timer.start()


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self)
        MyTaskBarIcon()  # 显示系统托盘图标


class MyApp(wx.App):
    def OnInit(self):
        MyFrame()
        return True


if __name__ == "__main__":
    init()
    app = MyApp()
    app.MainLoop()
