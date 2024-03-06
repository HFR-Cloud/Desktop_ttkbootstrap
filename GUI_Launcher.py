# -*- coding: utf-8 -*-

# Cloudreve Desktop 作者：于小丘 / 暗之旅者

App_Version = "0.0.5"

#导入必要库
import ttkbootstrap as ttk
from ttkbootstrap import dialogs
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os,requests,json,math,http.cookiejar,webbrowser
from configparser import ConfigParser

#登录页图片展示准备
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.join(current_dir, 'Resources')
except:
    print('文件缺失，以Tiny模式启动')

# Cookie与配置文件准备
cookie_jar = http.cookiejar.CookieJar()
config = ConfigParser()
config.read('config.ini')

# 设置配置文件中目标Cloudreve的地址，没有则默认连接本机Cloudreve
try:
    URL = config['account']['url']
except:
    URL = "http://localhost:5212"

# 从本机中读取账号密码，这一功能在后续会添加加密读取
try:
    localaccount = localpassword = ""
    localaccount = config.get('account','username')
    localpassword = config.get('account','password')
except:
    print('没有保存账号密码')

# 获取云盘信息
Cloud_Info = requests.get(URL + "/manifest.json")
if Cloud_Info.status_code == 200:
    Cloud_Info = Cloud_Info.json()
    Cloud_name = Cloud_Info['short_name']

# 注册与忘记密码跳转网页
def SignUP():
    SignUP_URL = URL + "/signup"
    webbrowser.open(SignUP_URL)

def FogetPassword():
    Foget_URL = URL + "/foget"
    webbrowser.open(Foget_URL)

# 登录成功后执行
def SuccessLogin(response,WhenStart=False):
    if WhenStart:
        AutoLoginURL = URL + "/api/v3/site/config"      #返回预览：{"code": 0,"data": {"title": "Cloudreve","loginCaptcha": false,"regCaptcha": false,"forgetCaptcha": false,"emailActive": false,"themes": "{\"#3f51b5\":{\"palette\":{\"primary\":{\"main\":\"#3f51b5\"},\"secondary\":{\"main\":\"#f50057\"}}},\"#2196f3\":{\"palette\":{\"primary\":{\"main\":\"#2196f3\"},\"secondary\":{\"main\":\"#FFC107\"}}},\"#673AB7\":{\"palette\":{\"primary\":{\"main\":\"#673AB7\"},\"secondary\":{\"main\":\"#2196F3\"}}},\"#E91E63\":{\"palette\":{\"primary\":{\"main\":\"#E91E63\"},\"secondary\":{\"main\":\"#42A5F5\",\"contrastText\":\"#fff\"}}},\"#FF5722\":{\"palette\":{\"primary\":{\"main\":\"#FF5722\"},\"secondary\":{\"main\":\"#3F51B5\"}}},\"#FFC107\":{\"palette\":{\"primary\":{\"main\":\"#FFC107\"},\"secondary\":{\"main\":\"#26C6DA\"}}},\"#8BC34A\":{\"palette\":{\"primary\":{\"main\":\"#8BC34A\",\"contrastText\":\"#fff\"},\"secondary\":{\"main\":\"#FF8A65\",\"contrastText\":\"#fff\"}}},\"#009688\":{\"palette\":{\"primary\":{\"main\":\"#009688\"},\"secondary\":{\"main\":\"#4DD0E1\",\"contrastText\":\"#fff\"}}},\"#607D8B\":{\"palette\":{\"primary\":{\"main\":\"#607D8B\"},\"secondary\":{\"main\":\"#F06292\"}}},\"#795548\":{\"palette\":{\"primary\":{\"main\":\"#795548\"},\"secondary\":{\"main\":\"#4CAF50\",\"contrastText\":\"#fff\"}}}}","defaultTheme": "#3f51b5","home_view_method": "icon","share_view_method": "list","authn": false,"user": {"id": "kpcv","user_name": "admin@yuxiaoqiu.cn","nickname": "于小丘 测试","status": 0,"avatar": "file","created_at": "2024-02-29T22:22:05.0800767+08:00","preferred_theme": "","anonymous": false,"group": {"id": 1,"name": "Admin","allowShare": true,"allowRemoteDownload": true,"allowArchiveDownload": true,"shareDownload": true,"compress": true,"webdav": true,"sourceBatch": 1000,"advanceDelete": true,"allowWebDAVProxy": true},"tags": []},"captcha_ReCaptchaKey": "defaultKey","captcha_type": "normal","tcaptcha_captcha_app_id": "","registerEnabled": true,"app_promotion": true,"wopi_exts": null},"msg": ""}
        cookies_txt = open('cookies.txt', 'r')          #以reader读取模式，打开名为cookies.txt的文件
        cookies_dict = json.loads(cookies_txt.read())   #调用json模块的loads函数，把字符串转成字典
        cookies = requests.utils.cookiejar_from_dict(cookies_dict)  #把转成字典的cookies再转成cookies本来的格式
        session = requests.Session()
        session.keep_alive = False
        session.cookies = cookies
        response = session.get(AutoLoginURL)
    Login_Frame.pack_forget()
    Home_Frame.pack(fill=ttk.BOTH, expand=True)
    app.geometry('800x600')
    app.place_window_center()
    TitleShow = '/ - ' + Cloud_name
    app.title(TitleShow)
    if not WhenStart:
        cookies_dict = requests.utils.dict_from_cookiejar(response.cookies) #把cookies转化成字典
        cookies_str = json.dumps(cookies_dict)                              #调用json模块的dumps函数，把cookies从字典再转成字符串。
        cookieWriter = open('cookies.txt', 'w')             #创建名为cookies.txt的文件，以写入模式写入内容
        cookieWriter.write(cookies_str)
        cookieWriter.close()
    if WhenStart:
            config.set('account', 'user_name', response.json()['data']['user']['user_name'])
            config.set('account', 'nickname', response.json()['data']['user']['nickname'])
            config.set('account', 'groupname', response.json()['data']['user']['group']['name'])
            config.set('account', 'AllowShare', str(response.json()['data']['user']['group']['allowShare']))
            config.set('account', 'AllowRemoteDownload', str(response.json()['data']['user']['group']['allowRemoteDownload']))
            config.set('account', 'AllowArchiveDownload', str(response.json()['data']['user']['group']['allowArchiveDownload']))
            try:
                config.set('account','AdvanceDelete', str(response.json()['data']['user']['group']['advanceDelete']))
                config.set('account', 'AllowWebDAVProxy', str(response.json()['data']['user']['group']['allowWebDAVProxy']))
            except:
                print('无法读取某些配置，可能是服务端版本过低')
    else:
        config.set('account', 'user_name', response.json()['data']['user_name'])
        config.set('account', 'nickname', response.json()['data']['nickname'])
        config.set('account', 'groupname', response.json()['data']['group']['name'])
        config.set('account', 'AllowShare', str(response.json()['data']['group']['allowShare']))
        config.set('account', 'AllowRemoteDownload', str(response.json()['data']['group']['allowRemoteDownload']))
        config.set('account', 'AllowArchiveDownload', str(response.json()['data']['group']['allowArchiveDownload']))
        try:
            config.set('account','AdvanceDelete', str(response.json()['data']['group']['advanceDelete']))
            config.set('account', 'AllowWebDAVProxy', str(response.json()['data']['group']['allowWebDAVProxy']))
        except:
            print('无法读取某些配置，可能是服务端版本过低')
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    GetDirList()
    RefrushStorage()

# TODO：带验证码的登录
def captcha_Login():
    CAPTCHA_GET_URL = URL + '/api/v3/site/captcha'
    session = requests.session()
    session.keep_alive = False
    response = session.get(CAPTCHA_GET_URL)
    print(response.text)

# OTP登录
def loginOTP():
    username = entry_username.get()
    config.set('account', 'username', username)
    password = entry_password.get()
    config.set('account', 'password', password)
    #Copy From login
    username = entry_username.get()
    try:
        config.set('account', 'username', username)
    except:
        config.add_section('account')
        config.set('account', 'username', username)
    password = entry_password.get()
    config.set('account', 'password', password)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    login_data = {
        'username': username,
        'password': password
    }
    TwoFACode = entry_OTP.get()
    TwoFA_data = {
        'code': TwoFACode
    }
    LOGIN_URL = URL + '/api/v3/user/session'
    TwoFA_URL = URL + '/api/v3/user/2fa'
    try:
        response = requests.post(LOGIN_URL, json=login_data)
    except ConnectionError:
        errorCode.set('无法连接到服务器')
        loginErrorCode.pack()
        pass
    if response.status_code == 200:
        status_code = response.json()['code']
        if status_code == 203:    # 需要OTP验证码
            OTP_Cookies = response.cookies
            response2 = requests.post(TwoFA_URL, json=TwoFA_data, cookies=OTP_Cookies)
            if response2.status_code == 200:
                status_code = response2.json()['code']
                if status_code == 0:
                    SuccessLogin(response=response2)
                elif status_code == 40022:
                    errorCode.set('OTP验证码错误')
                else:
                    print('未知错误：',response2.json())
        else:
            print(response.json())
            raise Exception("未知错误")
        if status_code != 0:
            loginErrorCode.pack()

# 登录相关
def login():
    entry_username.config(state='disabled')
    entry_password.config(state='disabled')
    button_login.config(state='disabled')
    username = entry_username.get()
    try:
        config.set('account', 'username', username)
    except:
        config.add_section('account')
        config.set('account', 'username', username)
    password = entry_password.get()
    config.set('account', 'password', password)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    login_data = {
        'username': username,
        'password': password
    }
    LOGIN_URL = URL + '/api/v3/user/session'
    try:
        response = requests.post(LOGIN_URL, json=login_data)
    except ConnectionError:
        errorCode.set('无法连接到服务器')
        loginErrorCode.pack()
        pass
    if response.status_code == 200:
        status_code = response.json()['code']
        if status_code == 0:        #登录成功函数
            SuccessLogin(response=response)
            entry_username.config(state='normal')
            entry_password.config(state='normal')
            button_login.config(state='normal')
        elif status_code == 203:    # 需要OTP验证码
            frame_username.pack_forget()
            frame_password.pack_forget()
            frame_OTP.pack()
            button_login.pack_forget()
            button_register.pack_forget()
            button_forget.pack_forget()
            button_BackToLogin.pack(side=ttk.LEFT,ipadx=20,padx=5)
            button_TwoStepLogin.pack(side=ttk.LEFT,ipadx=20,padx=5)
            frame_button.pack_forget()
            frame_button.pack(pady=5)
            errorCode.set('需要OTP验证码')
        elif status_code == 40001:
            errorCode.set('账号密码不能为空')
            entry_username.config(state='normal')
            entry_password.config(state='normal')
            button_login.config(state='normal')
            print(response.json())
        elif status_code == 40017:  #账号被封禁
            errorCode.set('账号被封禁')
            print(response.json())
        elif status_code == 40018:  #账号尚未激活
            entry_username.config(state='normal')
            entry_password.config(state='normal')
            button_login.config(state='normal')
            errorCode.set('账号尚未激活，请在邮箱中确认')
            print(response.json())
        elif status_code == 40020:  #用户名或密码错误
            errorCode.set('用户名或密码错误')
            entry_username.config(state='normal')
            entry_password.config(state='normal')
            button_login.config(state='normal')
            print(response.json())
        elif status_code == 40026:
            errorCode.set('暂不支持登录带验证码的服务端')
            captcha_Login()
        else:
            print(response.json())
            raise Exception("未知错误")
        if status_code != 0:
            loginErrorCode.pack()

# 从输入OTP验证码页面返回账号密码页面的布局显示
def BackToLogin():
    entry_OTP.delete(0, ttk.END)
    frame_button.pack_forget()
    frame_OTP.pack_forget()
    frame_username.pack(pady=5)
    frame_password.pack(pady=5)
    button_BackToLogin.pack_forget()
    button_TwoStepLogin.pack_forget()
    button_login.pack(side=ttk.LEFT,ipadx=20,padx=5)
    button_register.pack(side=ttk.LEFT,ipadx=20,padx=5)
    button_forget.pack(side=ttk.LEFT,padx=10)
    frame_button.pack(pady=5)
    loginErrorCode.pack_forget()

# 退出登录相关
def LogOut():
    ROOTPATH_URL = URL + '/api/v3/user/session'
    cookies_txt = open('cookies.txt', 'r')          #以reader读取模式，打开名为cookies.txt的文件
    cookies_dict = json.loads(cookies_txt.read())   #调用json模块的loads函数，把字符串转成字典
    cookies = requests.utils.cookiejar_from_dict(cookies_dict)  #把转成字典的cookies再转成cookies本来的格式
    session = requests.Session()
    session.keep_alive = False
    session.cookies = cookies
    response = session.delete(ROOTPATH_URL)
    if response.status_code == 200:
        status_code = response.json()['code']
        if status_code == 0:        #退出登录成功
            dialogs.Messagebox.ok(message='退出登录成功')
            fileList.delete(*fileList.get_children())   #清空文件列表
            Home_Frame.pack_forget()
            app.title(Cloud_name)
            app.geometry("623x350")
            app.place_window_center()
            Login_Frame.pack()

# 获取文件后缀的处理
def get_last_part(variable):
    parts = variable.split('.')
    return parts[-1]

# 返回上级文件的地址处理
def last_dir(s):
    dir = s[:s.rfind('/')] if '/' in s else ''
    if dir == '':
        return "/"
    else:
        return dir

# 文件大小转换，可提供Byte转成正常人易读的类型
def convert_size(size_bytes):
    if size_bytes == 0:
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s%s" % (s, size_name[i])

# 文件列表双击事件，处理文件（夹）打开
def filelistonclick(event):
    select_ID = fileList.focus()
    selected_item_values = fileList.item(select_ID)['values']
    if selected_item_values != '':
        if str(selected_item_values[0]) == '../':
            path = last_dir(AddressBar.get())
            GetDirList(path)
        elif str(selected_item_values[2]) == 'dir':
            if AddressBar.get() == "/":
                path = AddressBar.get() + str(selected_item_values[0])
            else:
                path = AddressBar.get() + "/" + str(selected_item_values[0])
            GetDirList(path)
        elif str(selected_item_values[2]) == '上级目录':
            pass
        elif get_last_part(str(selected_item_values[0])) == 'txt':
            print('TXT文件预览相关代码')
        else:
            dialogs.Messagebox.ok(message='暂不支持文件操作')
    else:
        fileList.selection_clear()

# 请求文件列表并展示相关
def GetDirList(path="%2F",WhenStart=False):
    ROOTPATH_URL = URL + '/api/v3/directory' + path
    cookies_txt = open('cookies.txt', 'r')          #以reader读取模式，打开名为cookies.txt的文件
    cookies_dict = json.loads(cookies_txt.read())   #调用json模块的loads函数，把字符串转成字典
    cookies = requests.utils.cookiejar_from_dict(cookies_dict)  #把转成字典的cookies再转成cookies本来的格式
    session = requests.Session()
    session.keep_alive = False
    session.cookies = cookies
    response = session.get(ROOTPATH_URL)
    status_code = response.json()['code']
    if status_code == 0:
        fileList.delete(*fileList.get_children())   #清空文件列表
        path2 = path.replace('%2F','/')
        if path2 != '/':
            fileList.insert("",'0',values=('../', '', '上级目录', ''))
        AddressBar.delete(0, END)
        AddressBar.insert(0, path2)
        TitleShow = path2 + ' - ' + Cloud_name
        app.title(TitleShow)
        FileList = json.loads(response.text)
        objects = FileList['data']['objects']
        objects_list = []
        objects = FileList.get('data', {}).get('objects', [])
        for obj in objects:
            name = obj.get('name', '')
            size = obj.get('size', '')
            size = convert_size(size)
            if size == '0B':
                size = ''
            type = obj.get('type', '')
            date = obj.get('date', '').replace('T', ' ').split('.')[0]
            objects_list.append((name, str(size), type, date))
        for itm in objects_list:
            fileList.insert("",'end',values=itm)
        if WhenStart:
            Login_Frame.pack_forget()
            Home_Frame.pack()

# 处理地址栏更改后刷新文件列表事件
def ListNewDir(event):
    GetDirList(AddressBar.get().replace('/', '%2F'))

# 刷新用户容量函数
def RefrushStorage():
    Require_URL = URL + '/api/v3/user/storage'
    cookies_txt = open('cookies.txt', 'r')          #以reader读取模式，打开名为cookies.txt的文件
    cookies_dict = json.loads(cookies_txt.read())   #调用json模块的loads函数，把字符串转成字典
    cookies = requests.utils.cookiejar_from_dict(cookies_dict)  #把转成字典的cookies再转成cookies本来的格式
    session = requests.Session()
    session.keep_alive = False
    session.cookies = cookies
    response = session.get(Require_URL)             #返回内容 {"code":0,"data":{"used":896322996,"free":177418828,"total":1073741824},"msg":""}
    Storage = json.loads(response.text)
    used = convert_size(Storage['data']['used'])
    total = convert_size(Storage['data']['total'])
    accountText = config.get('account','nickname') + ' ' + used + '/' + total
    accountInfo.config(text=accountText)

# TODO：文件预览相关
def filePreview():
    textbox.delete(1.0,END)
    textbox.insert(1.0, 'a fox jumps over a lazy dog.\na fox jumps over a lazy dog.')
    Home_Frame.pack_forget()
    FilePreview_Frame.pack(fill=BOTH)
    #TODO:文件预览地址：/api/v3/file/content/ + 文件id

def filePreview_Back():
    textbox.delete(1.0,END)
    FilePreview_Frame.pack_forget()
    Home_Frame.pack()

# 处理密码框回车即登录事件
def on_enter_pressed(event):
    login()

# 个人设置页面
def Personal_Settings():
    Home_Frame.pack_forget()
    Personal_Settings_Frame.pack(fill=BOTH, expand=YES)

# 从个人设置返回到文件列表页
def Personal_Settings_Back():
    Personal_Settings_Frame.pack_forget()
    Home_Frame.pack(fill=BOTH, expand=YES)

# 为地址栏至少填充一个“/”
def CheckAddressBarEmpty(event):
    if AddressBar.get() == '':
        AddressBar.insert(0, '/')

"""
======================================
以下是前端相关
======================================
"""

app = ttk.Window(themename='superhero')
# 测试中的功能 - 无边框窗口 app.overrideredirect(True)
app.geometry("623x350")
app.resizable(0,0) #禁止窗口缩放

#登录页布局
Login_Frame = ttk.Frame(app)
Login_Frame.pack()

#底部栏相关
info_label_text = "App版本：" + App_Version + " 功能补全开发版本 | 2018-2024 于小丘 版权所有并保留最终解释权。\n继续使用本软件即代表同意本软件与您登录的Cloudreve服务商的用户协议与隐私政策。"
info_label = ttk.Label(Login_Frame, text=info_label_text,font=('思源黑体',10))
info_label.pack(side=ttk.BOTTOM,fill=ttk.X)

try:
    image_path = os.path.join(resources_dir, 'Logo.png')
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)

    pictureFrame = ttk.Frame(Login_Frame)
    pictureFrame.pack(side=ttk.LEFT)

    label = ttk.Label(pictureFrame, image=photo)
    label.pack(side=ttk.RIGHT)
except:
    pass

loginFrame = ttk.Frame(Login_Frame)
loginFrame.pack(side=ttk.LEFT,fill=BOTH, expand=YES)

iloginFrame = ttk.Frame(loginFrame)
iloginFrame.pack(side=ttk.LEFT)

LoginAppName = '登录 ' + Cloud_name
label_APPNAME = ttk.Label(iloginFrame, text=LoginAppName,font=('思源黑体',24))
label_APPNAME.pack(pady=10)

errorCode = ttk.StringVar()
loginErrorCode = ttk.Label(iloginFrame, bootstyle="danger",font=('思源黑体',12),textvariable=errorCode)

frame_username = ttk.Frame(iloginFrame)
frame_username.pack(pady=5)
frame_password = ttk.Frame(iloginFrame)
frame_password.pack(pady=5)
frame_OTP = ttk.Frame(iloginFrame)
frame_button = ttk.Frame(iloginFrame)
frame_button.pack(pady=5)

label_username = ttk.Label(frame_username, text="用户名:",font=('思源黑体',12))
label_username.pack(side=ttk.LEFT)

entry_username = ttk.Entry(frame_username)
entry_username.insert(0,localaccount)
entry_username.pack(side=ttk.LEFT,ipadx=30,padx=5)

label_password = ttk.Label(frame_password, text="密    码:",font=('思源黑体',12))
label_password.pack(side=ttk.LEFT)

entry_password = ttk.Entry(frame_password, show="*")
entry_password.insert(0,localpassword)
entry_password.pack(side=ttk.LEFT,ipadx=30,padx=5)
entry_password.bind('<Return>', on_enter_pressed)

label_OTP = ttk.Label(frame_OTP, text="验证码:",font=('思源黑体',12))
label_OTP.pack(side=ttk.LEFT)
entry_OTP = ttk.Entry(frame_OTP)
entry_OTP.pack(side=ttk.LEFT,ipadx=30,padx=5)

button_login = ttk.Button(frame_button, text="登录", command=login)
button_login.pack(side=ttk.LEFT,ipadx=20,padx=5)

#注册按钮相关
button_register = ttk.Button(frame_button, text="注册",bootstyle="outline",command=SignUP)
button_register.pack(side=ttk.LEFT,ipadx=20,padx=5)

#忘记密码相关
button_forget = ttk.Button(frame_button, text="忘记密码",bootstyle="link",command=FogetPassword)
button_forget.pack(side=ttk.LEFT,padx=10)

#两步验证返回按钮
button_BackToLogin = ttk.Button(frame_button, text="返回",bootstyle="outline",command=BackToLogin)

#两步验证登录按钮
button_TwoStepLogin = ttk.Button(frame_button, text="登录",command=loginOTP)

#登录页布局结束,云盘主页布局开始

Home_Frame = ttk.Frame(app)

MenuBar = ttk.Frame(Home_Frame)
MenuBar.pack(side=ttk.TOP,fill=ttk.X)

fileMenuButton = ttk.Menubutton(MenuBar, text="文件",bootstyle="secondary")
fileMenuButton.pack(side=ttk.LEFT)
HelpMenuButton = ttk.Menubutton(MenuBar, text="实验室",bootstyle="secondary")
HelpMenuButton.pack(side=ttk.LEFT)

AddressBar = ttk.Entry(MenuBar)
AddressBar.insert(0,'/')
AddressBar.bind('<KeyRelease>',CheckAddressBarEmpty)
AddressBar.bind('<Return>', ListNewDir)
AddressBar.pack(side=ttk.LEFT,fill=ttk.X,padx=10,ipadx=40)

accountInfo = ttk.Menubutton(MenuBar, text="读取信息中……",bootstyle="secondary")
accountInfo.pack(side=ttk.RIGHT)

FileMenu = ttk.Menu(fileMenuButton,relief='raised')
FileMenu.add_command(label="全部文件",font=('思源黑体',10))  #/api/v3/directory/
FileMenu.add_command(label="视频",font=('思源黑体',10))      #/api/v3/file/search/video/internal
FileMenu.add_command(label="图片",font=('思源黑体',10))      #/api/v3/file/search/image/internal
FileMenu.add_command(label="音乐",font=('思源黑体',10))      #/api/v3/file/search/audio/internal
FileMenu.add_command(label="文档",font=('思源黑体',10))      #/api/v3/file/search/doc/internal
FileMenu.add_command(label="视频",font=('思源黑体',10))      #/api/v3/file/search/video/internal
FileMenu.add_separator()
FileMenu.add_command(label="上传文件",font=('思源黑体',10))
FileMenu.add_command(label="上传文件夹",font=('思源黑体',10))
FileMenu.add_separator()
FileMenu.add_command(label="我的分享",font=('思源黑体',10))
FileMenu.add_command(label="离线下载",font=('思源黑体',10))
FileMenu.add_command(label='连接',font=('思源黑体',10))
FileMenu.add_command(label='任务队列',font=('思源黑体',10))
fileMenuButton.config(menu=FileMenu)

DebugMenu = ttk.Menu(HelpMenuButton,relief='raised')
DebugMenu.add_command(label="打开文件预览界面",command=filePreview,font=('思源黑体',10))
HelpMenuButton.config(menu=DebugMenu)

UserMenu = ttk.Menu(accountInfo,relief='raised')
UserMenu.add_command(label="个人设置",font=('思源黑体',10),command=Personal_Settings)
UserMenu.add_command(label="APP设置",font=('思源黑体',10))
UserMenu.add_command(label="管理面板",font=('思源黑体',10))
UserMenu.add_command(label="退出登录",font=('思源黑体',10),command=LogOut)
accountInfo.config(menu=UserMenu)

fileListFrame = ttk.Frame(Home_Frame)
fileListFrame.pack(side=ttk.BOTTOM,fill=ttk.BOTH,expand=True)

fileList = ttk.Treeview(fileListFrame,columns=["名称","大小","类型","修改日期"],show=HEADINGS)
fileList.pack(side=ttk.LEFT,fill=ttk.BOTH,expand=True)
fileList.bind("<Double-Button-1>",filelistonclick)

# 主页布局结束，文件预览界面开始

FilePreview_Frame = ttk.Frame(app)

FilePreview_title = ttk.Label(FilePreview_Frame,text="untitled.txt",font=("思源黑体", 18))
FilePreview_title.pack(anchor="nw",padx=20,pady=20)

textbox = ttk.ScrolledText(FilePreview_Frame)
textbox.pack(fill=ttk.BOTH,expand=True)

FilePreview_Button_Frame = ttk.Frame(FilePreview_Frame)
FilePreview_Button_Frame.pack(side=ttk.BOTTOM,anchor="sw",padx=20,pady=20)

FilePreview_Save_button = ttk.Button(FilePreview_Button_Frame,text="保存 ( 暂不支持 )",state='disabled')
FilePreview_Save_button.pack(side=ttk.LEFT,padx=10,ipadx=20)

FilePreview_Cancel_button = ttk.Button(FilePreview_Button_Frame,text="取消",bootstyle='outline',command=filePreview_Back)
FilePreview_Cancel_button.pack(side=ttk.LEFT,padx=10,ipadx=20)

# 文件预览界面结束，个人设置页布局开始

Personal_Settings_Frame = ttk.Frame(app)

Personal_Settings_title = ttk.Label(Personal_Settings_Frame,text="个人设置(待开发)",font=("思源黑体", 18))
Personal_Settings_title.pack(anchor="nw",padx=20,pady=20)

Personal_Settings_info = ttk.Label(Personal_Settings_Frame,text="个人资料",font=("思源黑体", 12))
Personal_Settings_info.pack(anchor="nw",padx=40)

Personal_Settings_Button_Frame = ttk.Frame(Personal_Settings_Frame)
Personal_Settings_Button_Frame.pack(padx=10,pady=10)

Personal_Settings_Save = ttk.Button(Personal_Settings_Button_Frame,text="保存",state="disabled")
Personal_Settings_Save.pack(side=ttk.LEFT,padx=10,pady=10)

Personal_Settings_Cancel = ttk.Button(Personal_Settings_Button_Frame,text="取消",bootstyle="outline",command=Personal_Settings_Back)
Personal_Settings_Cancel.pack(side=ttk.LEFT,padx=10,pady=10)

# APP布局结束

# 自动登录
try:
    SuccessLogin('',True)
except:
    Home_Frame.pack_forget()
    app.geometry("623x350")
    app.title(Cloud_name)
    app.place_window_center()
    Login_Frame.pack()

app.place_window_center()
app.mainloop()