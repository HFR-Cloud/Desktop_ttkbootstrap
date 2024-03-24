<p align = "center">
<br><br>
<h1><center>HeyCloud Desktop</center></h1>
原名Cloudreve Desktop，一个基于Tkinter的可跨平台的海枫云存储客户端，兼容Cloudreve V3，并使用ttkbootstrap库进行美化<br><br>

## 目前已经实现的功能
- 登录 & 注销
- 文件夹浏览
- 文件搜索
- 新建文件 / 文件夹
- 删除文件 / 文件夹
- 文件分类浏览
- 文件预览 / 下载
- WebDAV列表

## 目前未实现但严重影响体验的功能
- 无法登录需要谷歌与腾讯验证码的 HeyCloud / Cloudreve
- 账号与Cookies为明文保存

## 兼容的 HeyCloud / Cloudreve 版本
- HeyCloud：V0.0.x
- Cloudreve：V3.x.x `推荐V3.8.3`

## 程序配置设置
需要在程序根目录新建文件`config.ini`。示例内容如下：
```
[account]
url = http://localhost:5212         ;这里填写服务端的地址，若为ip访问，HeyCloud默认使用0703端口，Cloudreve默认使用5212端口；填写你需要接入的地址，结尾不需要加“/”
username = admin@yuxiaoqiu.cn       ;这里填写你的邮箱，程序会保存这个邮箱并在启动时自动填充
id = AqbS                           ;用户ID
nickname = Cloudreve                ;用户名
groupname = Admin                   ;头衔（在Cloudreve被称为用户组名称）
allowshare = True                   ;是否允许分享
allowremotedownload = True          ;是否允许多线程下载
allowarchivedownload = True         ;是否允许打包下载
advancedelete = True                ;是否允许高级删除
allowwebdavproxy = False            ;是否允许webdav代理

[settings]
theme = light                       ;程序主题，可自行填写light或者dark
```

如果是本地调试，则无需新建`config.ini`，程序会自动为url填充http://localhost:5212

## 启动&构建方式
将完整代码拉取到本地（也可仅拉取`GUI_Launcher.py`，程序会以`Tiny`模式启动 **但非常不建议这样做** ）

Windows:
双击GUI_Launcher.py即可启动

Linux:
使用`chomod +x GUI_Launcher.py`命令后再使用`./GUI_Launcher.py`即可启动。

## 开源许可
基于以下许可证，本程序闭源。
```
ttkbootstrap   开源许可:MIT
tkinter        开源许可:Python Software Foundation License
Pillow         开源许可:Python Imaging Library License
Python         开源许可:Python Software Foundation License
requests       开源许可:Apache License 2.0
windnd         开源许可:MIT
pyotp          开源许可:MIT
Python         开源许可:Python Software Foundation License
pyperclip      开源许可:MIT
```