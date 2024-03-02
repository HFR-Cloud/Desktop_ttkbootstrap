<p align = "center">
<img alt="Logo" src="./Resources/Logo.png" height="250px">
<br><br>
<h1><center>Cloudreve Desktop</center></h1>
一个基于Tkinter的可跨平台的Cloudreve客户端，并使用ttkbootstrap库进行美化<br><br>

## 目前已经实现的功能
- 登录 & 注销
- 根目录浏览

## 兼容的Cloudreve版本
- 3.8.3 `推荐`

## 三方开发指南
需要在程序根目录新建文件`config.ini`，并写入以下内容：
```
[account]
url = http://localhost:5212
(上面填写你需要接入的地址，结尾不需要加“/”,如果是本地调试，则不需要加，程序会自动填充http://localhost:5212)
```

## 启动&构建方式
确保操作系统内包含以下依赖项：
```
ttkbootstrap
PIL
os
requests
json
http
webbrowser
configparser
```

Windows:
双击GUI_Launcher.py即可启动

Linux:
使用`chomod +x GUI_Launcher.py`命令后再使用`./GUI_Launcher.py`即可启动。

## 开源许可
本程序使用GPLv3开源许可。
