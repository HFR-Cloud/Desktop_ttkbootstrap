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
- 新建WebDAV账户

## 目前未实现但严重影响体验的功能
- 文件上传(因为技术原因本人实在无法完成)
- 无法登录需要谷歌与腾讯验证码的 HeyCloud / Cloudreve
- 账号与Cookies为明文保存

## 兼容的 HeyCloud / Cloudreve 版本
- HeyCloud：V0.0.x
- Cloudreve：V3.8.x `推荐V3.8.3`

## 程序配置设置
需要在程序根目录新建文件`config.ini`。示例内容如下：
```
[account]
url = http://localhost:5212         ;这里填写服务端的地址，若为ip访问，HeyCloud默认使用7030端口，Cloudreve默认使用5212端口；填写你需要接入的地址，结尾不需要加“/”
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
使用`python3 GUI_Launcher.py`即可启动

## 开源许可 & 杂谈
本来我并不想开源这个项目的（因为之前我的项目开源之后被别人申请著作权以后返回来告我抄袭，加之这个项目也是自己很久做出来的心血），现在想通了，所以采用**GPL v3**进行开源。但是你也可以赞助我，感谢您的投喂！感谢您的star！

## 小广告
- 如果你有自己的网站，请请将你的网站名称、网站描述与网站头像地址（注意是地址，否则会被cloudflare打回）发送给`admin@yuxiaoqiu.cn`，并提前在你的网站友链区域填上我的网站信息，我会尽快使用邮件回复：
```
网站名称：海枫筑梦计划
网站地址：https://yuxiaoqiu.cn
头像地址：https://img2.imgtp.com/2024/05/01/6GBVrmz2.jpg
```