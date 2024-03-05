<p align = "center">
<img alt="Logo" src="./Resources/Logo.png" height="250px">
<br><br>
<h1><center>Cloudreve Desktop</center></h1>
一个基于Tkinter的可跨平台的Cloudreve客户端，并使用ttkbootstrap库进行美化<br><br>

## 目前已经实现的功能
- 登录 & 注销
- 文件夹浏览（需要使用地址栏，列表暂时无法点击）

## 兼容的Cloudreve版本
- 3.x.x 
- 建议使用3.8.3，对旧版目前仅做了登录的适配

## 三方开发指南
需要在程序根目录新建文件`config.ini`，并写入以下内容：
```
[account]
url = http://localhost:5212
```
上面填写你需要接入的地址，结尾不需要加“/”

如果是本地调试，则无需新建`config.ini`，程序会自动填充http://localhost:5212

## 温馨提示
目前本程序是以明文保存账号，密码和cookies的，请注意保护好隐私

后续会增加加密

顺便

## 启动&构建方式
将完整代码拉取到本地（Resources可选，若不拉取会以`Tiny`模式启动）

Windows:
双击GUI_Launcher.py即可启动

Linux:
使用`chomod +x GUI_Launcher.py`命令后再使用`./GUI_Launcher.py`即可启动。

## 开源许可
本程序暂时闭源，后续可能会考虑开源，请持续关注。
