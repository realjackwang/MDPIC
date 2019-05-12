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
from threading import Thread
from PIL import ImageGrab
from pynput import keyboard
from git import Repo
from pyperclip import copy

current_key_pressed = []  # 当前按下的按键
github_username = ''  # 填入你的github的用户名
repository_name = ''

repo = Repo(os.getcwd())
git = repo.git


def init():
    with open('config.yml', 'r', encoding='utf-8') as f:
        cont = f.read()
        config = yaml.load(cont, Loader=yaml.BaseLoader)
        try:
            global github_username, repository_name
            github_username = config['github_username']
            repository_name = config['repository_name']
        except:
            pass


def savepic():
    try:
        im = ImageGrab.grabclipboard()
        filename = len(os.listdir('images'))
        im.save(r'images/image_' + str(filename) + '.png')
        ThreadUpload('images\\image_' + str(filename) + '.png')
        copy(
            'https://raw.githubusercontent.com/' + github_username + '/' + repository_name + '/master/images/image_' + str(
                filename) + '.png')
    except:
        pass


def on_release(key):
    if 'Key.ctrl_l' in current_key_pressed and "'m'" in current_key_pressed:
        savepic()
    if str(key) in current_key_pressed:
        current_key_pressed.remove(str(key))


def on_press(key):
    if str(key) not in current_key_pressed and str(key) != 'Key.f1':
        current_key_pressed.append(str(key))
    print(current_key_pressed)


class ThreadKey(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.start()  # start the thread

    def run(self):
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()


class ThreadUpload(Thread):
    def __init__(self, filename):
        Thread.__init__(self)
        self.filename = filename
        self.start()  # start the thread

    def run(self):
        git.add(os.path.join(os.getcwd(), self.filename))
        git.commit('-m', 'Add ' + self.filename)
        git.push()


class MyTaskBarIcon(wx.adv.TaskBarIcon):
    ICON = "logo.ico"  # 图标地址
    ID_ABOUT = wx.NewId()  # 菜单选项“关于”的ID
    ID_EXIT = wx.NewId()  # 菜单选项“退出”的ID
    ID_SHOW_WEB = wx.NewId()  # 菜单选项“显示页面”的ID
    TITLE = "MDPIC"  # 鼠标移动到图标上显示的文字

    def __init__(self):
        wx.adv.TaskBarIcon.__init__(self)
        self.SetIcon(wx.Icon(self.ICON), self.TITLE)  # 设置图标和标题
        self.Bind(wx.EVT_MENU, self.onAbout, id=self.ID_ABOUT)  # 绑定“关于”选项的点击事件
        self.Bind(wx.EVT_MENU, self.onExit, id=self.ID_EXIT)  # 绑定“退出”选项的点击事件
        self.Bind(wx.EVT_MENU, self.onShowWeb, id=self.ID_SHOW_WEB)  # 绑定“显示页面”选项的点击事件
        if github_username == '' or repository_name == '':
            wx.MessageBox('config.yml is not complete yet, please fill it', "Warning")
            wx.Exit()

    # “关于”选项的事件处理器
    def onAbout(self, event):
        wx.MessageBox('Author：Jack Wang\nEmail Address：544907049@qq.com\nLatest Update：2019-5-12', "info")

    # “退出”选项的事件处理器
    def onExit(self, event):
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
        return [('Upload Clipboard To GitHub', self.ID_SHOW_WEB),
                ('Info', self.ID_ABOUT),
                ('Exit', self.ID_EXIT)]


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self)
        MyTaskBarIcon()  # 显示系统托盘图标
        ThreadKey()


class MyApp(wx.App):
    def OnInit(self):
        MyFrame()
        return True


if __name__ == "__main__":
    init()
    app = MyApp()
    app.MainLoop()
