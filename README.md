# MDPIC
<p align="center" class="has-mb-6">
<img class="not-gallery-item" height="48" src="https://i.loli.net/2019/12/14/L3ZzHyqvshx9c2o.png">
<br> 利用Github搭建自己的图床！
<br>
<a href="https://github.com/skycity233/MDPIC">Preview</a> |
<a href="https://github.com/skycity233/MDPIC/releases/download/v1.0/MDPIC.rar">Download</a>
<br>
</p>

### :cd: 安装
首先fork这个本仓库，然后在电脑本地clone下来

```shell
git clone [your froked repository]
```
完成后，打开[config.yml](https://github.com/skycity233/MDPIC/blob/master/config.yml)将github_username和repository_name修改为你的用户名和仓库名。

### :gift: 如何使用

当你clone到本地后，你会得到如下的文件夹

![folder](https://raw.githubusercontent.com/skycity233/MYMDPIC/master/images/image_20191214215017952015.png)

确保你已经修改了config.yml再进行下一步

- 如果你有完整的python环境可以运行mdpic.py，不过推荐使用exe。

```shell
python mdpic.py
```

- 直接点击exe打开软件，可以在桌面创建快捷方式便于打开。

**当软件运行后**

1.复制一张照片到剪贴板，或者使用截图软件截图到剪贴板（例如Snipaste）

2.按下F8上传你的图片到你的github（**快捷键可以通过修改config.yml自定义**）

3.上传成功后，会有提示，同时url会返回到你的剪贴板。

🔨 改进

由于某些原因，命令行未能隐藏，本人正在寻找解决方案，我试过`pyinstaller -F -w` ，但是无法运行，应该和我使用了GitPython有关。

如果有人有解决方案，不妨提交一个issue，或者发邮件给我，感谢！:smile:
