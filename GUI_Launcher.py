# -*- coding: utf-8 -*-

# HFR-Cloud Desktop 作者：于小丘 / Debug：暗之旅者

# 填充程序信息
App_Version = "0.2.3"

# 填充国际化信息
zh_CN = {'launching': '启动中……', 'login_title': '登录 ', "username": "用户名：", "password": "密    码：","captcha": "验证码：", "OTP": "OTP验证码", "login": "登录"}
zh_TW = {"login": "登錄", "username": "用戶名：", "password": "密    碼：", "captcha": "驗證碼：", "OTP": "OTP驗證碼"}
en_US = {"login": "Login", "username": "Username", "password": "Password", "captcha": "Captcha", "OTP": "OTP Code"}

# 填充api信息
Cloudreve_V3 = {
    "ping":"/api/v3/site/ping",
    "siteConfig":"/api/v3/site/config",
    "session":"/api/v3/user/session",
    "captcha":"/api/v3/site/captcha",
    "2fa":"/api/v3/user/2fa",
    "filePreview":"/api/v3/file/content/",
    "dirList":"/api/v3/directory",
    "fileUpload":"/api/v3/file/upload",
    "OneDriveCallback":"/api/v3/callback/onedrive/finish/",
    "fileDownload":"/api/v3/file/download/",
    "userStorage":"/api/v3/user/storage",
    "searchKeywords":"/api/v3/search/keywords/",
    "searchVideo":"/api/v3/search/video/internal",
    "searchAudio":"/api/v3/search/audio/internal",
    "searchImage":"/api/v3/search/image/internal",
    "searchDoc":"/api/v3/search/doc/internal",
    "MakeFile":"/api/v3/file/create",
    "MakeDir":"/api/v3/directory",
    "DeleteFileDir":"/api/v3/object",
    "webdavAccount":"/api/v3/webdav/accounts"
}
Hfrcloud = {
    "ping":"/api/site/ping",
    "siteConfig":"/api/site/config",
    "session":"/api/oauth/session",
    "captcha":"/api/oauth/captcha",
    "2fa":"/api/oauth/2fa",
    "filePreview":"/api/disk/file/preview/",
    "dirList":"/api/disk/directory",
    "fileUpload":"/api/disk/file/upload",
    "OneDriveCallback":"/api/disk/callback/onedrive/finish/",
    "fileDownload":"/api/disk/file/download/",
    "userStorage":"/api/disk/user/storage",
    "searchKeywords":"/api/disk/search/keywords/",
    "searchVideo":"/api/disk/video/internal",
    "searchAudio":"/api/disk/audio/internal",
    "searchImage":"/api/disk/image/internal",
    "searchDoc":"/api/disk/doc/internal",
    "MakeFile":"/api/disk/create/file",
    "MakeDir":"/api/disk/create/directory",
    "DeleteFileDir":"/api/disk/object",
    "webdavAccount":"/api/disk/webdav/account"
}

# 导入必要库
import ttkbootstrap as ttk              # ttkbootstrap   开源许可:MIT
from ttkbootstrap import dialogs        # ttkbootstrap   开源许可:MIT
from ttkbootstrap.constants import *    # ttkbootstrap   开源许可:MIT
from tkinter import filedialog          # tkinter        开源许可:Python Software Foundation License
from PIL import Image, ImageTk          # Pillow         开源许可:Python Imaging Library License
import os                               # Python         开源许可:Python Software Foundation License
import requests                         # requests       开源许可:Apache License 2.0
import json                             # Python         开源许可:Python Software Foundation License
import math                             # Python         开源许可:Python Software Foundation License
import http.cookiejar                   # Python         开源许可:Python Software Foundation License
import webbrowser                       # Python         开源许可:Python Software Foundation License
import sys                              # Python         开源许可:Python Software Foundation License
import threading                        # Python         开源许可:Python Software Foundation License
import pyotp                            # pyotp          开源许可:MIT
import base64                           # Python         开源许可:Python Software Foundation License
import io                               # Python         开源许可:Python Software Foundation License
import pyperclip                        # pyperclip      开源许可:MIT
from configparser import ConfigParser   # Python         开源许可:Python Software Foundation License
import ctypes                           # Python         开源许可:Python Software Foundation License
import qrcode                           # qrcode         开源许可:MIT

# 资源文件目录访问
def source_path(relative_path):
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 修改当前工作目录，使得资源文件可以被正确访问
cd = source_path('')
os.chdir(cd)

# 高分屏优化(Alpha测试)
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)

# Cookie与配置文件准备
cookie_jar = http.cookiejar.CookieJar()
config = ConfigParser()
config.read('config.ini')

# 主题配置文件预载（如果配置文件不存在则预载浅色模式）
try:
    if config['settings']['theme'] == 'Light':
        theme = {'Theme': "cosmo", 'Menu': 'light'}
    else:
        theme = {'Theme': "darkly", 'Menu': 'secondary'}
except:
    theme = {'Theme': "litera", 'Menu': 'light'}

# 语言包预载（如果配置文件不存在则预载中文）
try:
    if config['settings']['language'] == 'zh_CN':
        locales = zh_CN
    elif config['settings']['language'] == 'zh_TW':
        locales = zh_TW
    elif config['settings']['language'] == 'en_US':
        locales = en_US
except:
    locales = zh_CN

# 服务端选择
try:
    if config['settings']['Server'] == 'Cloudreve_V3':
        router = Cloudreve_V3
    elif config['settings']['Server'] == 'Hfrcloud':
        router = Hfrcloud
except:
    router = Cloudreve_V3

# 设置配置文件中目标HFR-Cloud / Cloudreve的地址，没有则默认连接本机Cloudreve
try:
    URL = config['account']['url']
    if URL == "":
        URL = "http://127.0.0.1:5212"
except:
    URL = "http://127.0.0.1:5212"

# 设置配置文件中的字体，没有则默认使用思源黑体，如果系统未安装思源黑体则使用默认字体
try:
    Fonts = config['settings']['fonts']
except:
    Fonts = "思源黑体"

# 从本机中读取账号与2FA密钥，如果没有保存就pass
try:
    localaccount = config.get('account', 'username')
    otp_key = pyotp.TOTP(config.get('account', 'OTPKey'))
except:
    pass

# 初始化全局变量
Cloud_name = 'Loading……'
Login_captcha = False

# 初始化软件服务
def init():
    app.place_window_center()
    # 定义全局变量
    global Cloud_name
    global Login_captcha

    # 获取云盘信息
    try:
        Cloud_Info = requests.get(URL + router["siteConfig"])
        if Cloud_Info.status_code == 200:
            Cloud_Info = Cloud_Info.json()
            Cloud_name = Cloud_Info['data']['title']
            LoginAppName = '登录 ' + Cloud_name
            label_APPNAME.config(text=LoginAppName)
            captcha_Type = Cloud_Info['data']['captcha_type']
            Login_captcha = Cloud_Info['data']['loginCaptcha']
            if captcha_Type == 'recaptcha' and Login_captcha == True:
                app.geometry("623x400")
                app.place_window_center()
                Launching_Label.configure(text='暂不支持登录reCaptcha的服务端', font=('思源黑体', 12))
                sys.exit()
            elif captcha_Type == 'tcaptcha' and Login_captcha == True:
                app.geometry("623x400")
                app.place_window_center()
                Launching_Label.configure(text='暂不支持登录腾讯云验证码的服务端', font=('思源黑体', 12))
                sys.exit()
        # 原本是需要下面这一行来判断远程Cloudreve版本的，但是新版不需要，仅留获取版本接口
        # Cloud_Version = requests.get(URL + "/api/v3/site/ping").json()['data']
    except Exception as e:
        app.geometry("623x400")
        app.place_window_center()
        Launching_Label.configure(text='程序出现错误或无法连接到服务端，错误原因：' + str(e), font=('思源黑体', 12))
        sys.exit()

    try:
        SuccessLogin('', True)
    except:
        entry_username.config(state='normal')
        entry_password.config(state='normal')
        button_login.config(state='normal')
        ProgressBar.pack_forget()
        Launch_Frame.pack_forget()
        errorCode.set('自动登录失败，请手动登录')
        Home_Frame.pack_forget()
        # 判断是否需要验证码，如果需要则将窗口放大来适应验证码
        if Login_captcha:
            app.geometry("623x450")
        else:
            app.geometry("623x400")
        app.title(Cloud_name)
        app.place_window_center()
        Login_Frame.pack()

    # 刷新验证码
    if Login_captcha:
        captcha_Login()
    
# 定义上传/下载队列（目前没什么用）
Upload_queue = []
Download_queue = []

# 读取Cookies
def ReadCookies():
    try:
        appdata_path = os.getenv('APPDATA')  # 获取%appdata%的路径
        cookies_file_path = os.path.join(appdata_path, 'HeyFun', 'HFR-Cloud Desktop Community', 'HFsession')  # 拼接文件路径
        with open(cookies_file_path, 'r') as cookies_txt:  # 以reader读取模式，打开名为HFsession的文件
            cookies_dict = json.loads(cookies_txt.read())  # 调用json模块的loads函数，把字符串转成字典
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)  # 把转成字典的cookies再转成cookies本来的格式
            return cookies
    except:
        raise Exception("无法读取Cookies")  # raise需要一个异常实例，不能直接使用字符串

# 注册与忘记密码跳转网页
def SignUP():
    SignUP_URL = URL + "/signup"
    webbrowser.open(SignUP_URL)

def forgetPassword():
    forget_URL = URL + "/forget"
    webbrowser.open(forget_URL)

# 带验证码的登录事件（请求验证码，base64格式的图片）
def captcha_Login():
    CAPTCHA_GET_URL = URL + router["captcha"]
    cookies = ReadCookies()
    session = requests.session()
    session.cookies = cookies
    session.keep_alive = False
    response = session.get(CAPTCHA_GET_URL)
    status_code = response.json()['code']
    if status_code == 0:
        base64_string = response.json()['data']
        prefix = "data:image/png;base64,"
        base64_string = base64_string[len(prefix):]
        image_bytes = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_bytes))
        captcha_photo = ImageTk.PhotoImage(image)
        label_captcha_Pic.config(image=captcha_photo)
        label_captcha_Pic.image = captcha_photo  # 保存对图片的引用

# 登录成功后执行
def SuccessLogin(response, WhenStart=False):        # WhenStart：程序启动时自动登录时的请求
    if WhenStart:
        AutoLoginURL = URL + router["siteConfig"]
        cookies = ReadCookies()
        session = requests.Session()
        session.keep_alive = False
        session.cookies = cookies
        response = session.get(AutoLoginURL)
    if not WhenStart:
        cookies_dict = requests.utils.dict_from_cookiejar(response.cookies)  # 把cookies转化成字典
        cookies_str = json.dumps(cookies_dict)  # 调用json模块的dumps函数，把cookies从字典再转成字符串。
        appdata_path = os.getenv('APPDATA')  # 获取%appdata%的路径
        cookies_file_path = os.path.join(appdata_path, 'HeyFun', 'HFR-Cloud Desktop Community', 'HFsession')  # 拼接文件路径
        try:
            with open(cookies_file_path, 'w') as cookieWriter:  # 创建名为HFsession的文件，以写入模式写入内容
                cookieWriter.write(cookies_str)
        except:
            # 创建文件夹路径
            os.makedirs(os.path.dirname(cookies_file_path), exist_ok=True)
            # 创建名为HFsession的文件，以写入模式写入内容
            with open(cookies_file_path, 'w') as cookieWriter:
                cookieWriter.write(cookies_str)
        if WhenStart:
            data = response.json()['data']['user']
        else:
            data = response.json()['data']
        config.set('account', 'id', data['id'])
        config.set('account', 'nickname', data['nickname'])
        config.set('account', 'groupname', data['group']['name'])
        config.set('account', 'AllowShare', str(data['group']['allowShare']))
        config.set('account', 'AllowRemoteDownload', str(data['group']['allowRemoteDownload']))
        config.set('account', 'AllowArchiveDownload', str(data['group']['allowArchiveDownload']))
        try:
            config.set('account', 'AdvanceDelete', str(data['group']['advanceDelete']))
            config.set('account', 'AllowWebDAVProxy', str(data['group']['allowWebDAVProxy']))
        except:
            print('无法读取某些配置，可能是服务端版本过低')
    GetDirList()
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    Launch_Frame.pack_forget()
    Login_Frame.pack_forget()
    Home_Frame.pack(fill=ttk.BOTH, expand=True)
    app.geometry('800x600')
    app.place_window_center()
    TitleShow = '/ - ' + Cloud_name
    app.title(TitleShow)
    RefrushStorage()

# 刷新验证码
def RefrushCaptcha(event):
    CAPTCHA_GET_URL = URL + router["captcha"]
    cookies = ReadCookies()
    session = requests.session()
    session.cookies = cookies
    session.keep_alive = False
    response = session.get(CAPTCHA_GET_URL)
    status_code = response.json()['code']
    if status_code == 0:
        base64_string = response.json()['data']
        prefix = "data:image/png;base64,"
        base64_string = base64_string[len(prefix):]
        image_bytes = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_bytes))
        captcha_photo = ImageTk.PhotoImage(image)
        label_captcha_Pic.config(image=captcha_photo)
        label_captcha_Pic.image = captcha_photo  # 保存对图片的引用
        # 写入Cookies
        cookies_dict = requests.utils.dict_from_cookiejar(response.cookies)  # 把cookies转化成字典
        cookies_str = json.dumps(cookies_dict)  # 调用json模块的dumps函数，把cookies从字典再转成字符串。
        cookieWriter = open('HFsession', 'w')  # 创建名为HFsession的文件，以写入模式写入内容
        cookieWriter.write(cookies_str)
        cookieWriter.close()

# OTP登录
def loginOTP():
    entry_OTP.config(state='disabled')
    button_TwoStepLogin.config(state='disabled')
    button_BackToLogin.config(state='disabled')
    threading.Thread(target=loginOTP_Process).start()

# OTP登录处理（线程不卡GUI）
def loginOTP_Process():
    username = entry_username.get()
    config.set('account', 'username', username)
    password = entry_password.get()
    try:
        config.set('account', 'username', username)
    except:
        config.add_section('account')
        config.set('account', 'username', username)
    password = entry_password.get()
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
    LOGIN_URL = URL + router["session"]
    TwoFA_URL = URL + router["2fa"]
    try:
        response = requests.post(LOGIN_URL, json=login_data)
    except ConnectionError:
        errorCode.set('无法连接到服务器')
        loginErrorCode.pack()
        pass
    if response.status_code == 200:
        status_code = response.json()['code']
        if status_code == 203:  # 需要OTP验证码
            OTP_Cookies = response.cookies
            response2 = requests.post(TwoFA_URL, json=TwoFA_data, cookies=OTP_Cookies)
            if response2.status_code == 200:
                status_code = response2.json()['code']
                if status_code == 0:
                    SuccessLogin(response=response2)
                elif status_code == 40022:
                    errorCode.set('OTP验证码错误')
                    entry_OTP.config(state='normal')
                    button_TwoStepLogin.config(state='normal')
                    button_BackToLogin.config(state='normal')
                else:
                    print('未知错误：', response2.json())
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

    # 创建新线程来处理登录过程
    login_thread = threading.Thread(target=login_process)
    login_thread.start()


def login_process():
    username = entry_username.get()
    password = entry_password.get()
    captcha = entry_captcha.get()
    try:
        config.set('account', 'username', username)
    except:
        config.add_section('account')
        config.set('account', 'username', username)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    login_data = {
        'username': username,
        'password': password,
        'captchaCode': captcha
    }
    LOGIN_URL = URL + router["session"]
    try:
        cookies = ReadCookies()
    except:
        pass
    session = requests.Session()
    try:
        session.cookies = cookies
    except:
        pass
    try:
        response = session.post(LOGIN_URL, json=login_data)
    except ConnectionError:
        errorCode.set('无法连接到服务器')
        loginErrorCode.pack()
        pass
    if response.status_code == 200:
        status_code = response.json()['code']
        if status_code == 0:  # 登录成功函数
            SuccessLogin(response=response)
            entry_username.config(state='normal')
            entry_password.config(state='normal')
            button_login.config(state='normal')
        elif status_code == 203:  # 需要OTP验证码
            frame_username.pack_forget()
            frame_password.pack_forget()
            frame_OTP.pack()
            button_login.pack_forget()
            button_register.pack_forget()
            button_forget.pack_forget()
            button_BackToLogin.pack(side=ttk.LEFT, ipadx=20, padx=5)
            button_TwoStepLogin.pack(side=ttk.LEFT, ipadx=20, padx=5)
            frame_button.pack_forget()
            frame_button.pack(pady=5)
            errorCode.set('需要OTP验证码')
            try:
                otp_code = otp_key.now()
                entry_OTP.insert(0, otp_code)
                loginOTP()
            except:
                pass
        elif status_code == 40001:
            errorCode.set('账号密码不能为空')
            entry_username.config(state='normal')
            entry_password.config(state='normal')
            button_login.config(state='normal')
            print(response.json())
        elif status_code == 40017:  # 账号被封禁
            errorCode.set('账号被封禁')
            print(response.json())
        elif status_code == 40018:  # 账号尚未激活
            entry_username.config(state='normal')
            entry_password.config(state='normal')
            button_login.config(state='normal')
            errorCode.set('账号尚未激活，请在邮箱中确认')
            print(response.json())
        elif status_code == 40020:  # 用户名或密码错误
            errorCode.set('用户名或密码错误')
            entry_username.config(state='normal')
            entry_password.config(state='normal')
            button_login.config(state='normal')
            print(response.json())
        elif status_code == 40026:
            errorCode.set('验证码错误')
            entry_username.config(state='normal')
            entry_password.config(state='normal')
            button_login.config(state='normal')
            print(response.text)
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
    button_login.pack(side=ttk.LEFT, ipadx=20, padx=5)
    button_register.pack(side=ttk.LEFT, ipadx=20, padx=5)
    button_forget.pack(side=ttk.LEFT, padx=10)
    frame_button.pack(pady=5)
    loginErrorCode.pack_forget()
    entry_username.config(state='normal')
    entry_password.config(state='normal')
    button_login.config(state='normal')


# 退出登录相关
def LogOut():
    # 创建新线程来处理退出登录过程
    fileList.pack_forget()
    fileList.delete(*fileList.get_children())  # 清空文件列表
    ROOTPATH_URL = URL + router["session"]
    cookies = ReadCookies()
    session = requests.Session()
    session.keep_alive = False
    session.cookies = cookies
    response = session.delete(ROOTPATH_URL)
    if response.status_code == 200:
        status_code = response.json()['code']
        if status_code == 0:  # 退出登录成功
            fileList.delete(*fileList.get_children())  # 清空文件列表
            Home_Frame.pack_forget()
            app.title(Cloud_name)
            if Login_captcha:
                app.geometry("623x450")
            else:
                app.geometry("623x400")
            app.place_window_center()
            loginErrorCode.pack_forget()
            entry_username.config(state='normal')
            entry_password.config(state='normal')
            button_login.config(state='normal')
            Login_Frame.pack()


# 获取文件后缀的处理
def get_last_part(variable):
    parts = variable.split('.')
    return parts[-1]


# 返回上级文件的地址处理    调用：last_dir("/1/2/3/4") 返回：/1/2/3
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


# 处理单击取消选中事件
def LeftKeyOnclick(event):
    selected_items = fileList.selection()
    for item in selected_items:
        fileList.selection_remove(item)

# 处理右键打开文件事件
def RightKeyClickOpenFile():
    filelistonclick(event='')


# 处理右键打开文件夹事件
def RightKeyClickOpenDir():
    filelistonclick(event='')


# 文件列表双击事件，处理文件（夹）打开
def filelistonclick(event):
    select_ID = fileList.focus()
    selected_item_values = fileList.item(select_ID)['values']
    try:
        choose_name = str(selected_item_values[0])
        choose_name = choose_name[2:]
        fileType = get_last_part(choose_name).lower()
        if selected_item_values != '':
            if str(selected_item_values[0]) == '../':
                path = last_dir(RealAddress)
                GetDirList(path)
            elif str(selected_item_values[2]) == 'dir':
                if RealAddress == "/":
                    path = RealAddress + choose_name
                else:
                    path = RealAddress + "/" + choose_name
                GetDirList(path)
            elif str(selected_item_values[2]) == '上级目录':
                pass
            elif str(selected_item_values[2]) == 'loading':
                pass
            elif fileType == 'txt' or fileType == 'md' or fileType == 'json' or fileType == 'php' or fileType == 'py' or fileType == 'bat' or fileType == 'cpp' or fileType == 'c' or fileType == 'h' or fileType == 'java' or fileType == 'js' or fileType == 'html' or fileType == 'css' or fileType == 'xml' or fileType == 'yaml' or fileType == 'yml' or fileType == 'sh' or fileType == 'ini' or fileType == 'conf' or fileType == 'log':
                FilePreview_title.config(text=choose_name)
                Preview_Url = URL + router["filePreview"] + str(selected_item_values[4])
                cookies = ReadCookies()
                session = requests.Session()
                session.keep_alive = False
                session.cookies = cookies
                response = session.get(Preview_Url)
                TextPreview_textbox.delete('1.0', END)
                TextPreview_textbox.insert(END, response.text)
                Home_Frame.pack_forget()
                FilePreview_Frame.pack(fill='both', expand=True)
                title = choose_name + ' - ' + Cloud_name
                app.title(title)
            else:
                DownloadFile()
        else:
            fileList.selection_clear()
    except IndexError:
        pass


# 处理文件列表按下右键事件
def filelistonrightclick(event):
    select_ID = fileList.focus()
    selected_item_values = fileList.item(select_ID)['values']
    if selected_item_values == '':
        fileList_Menu_No_Select.post(event.x + app.winfo_rootx(), event.y + app.winfo_rooty())
        app.update()
    elif str(selected_item_values[2]) == 'dir':
        fileList_Menu_Select_dir.post(event.x + app.winfo_rootx(), event.y + app.winfo_rooty())
        app.update()
    elif str(selected_item_values[2]) == 'file':
        fileList_Menu_Select_file.post(event.x + app.winfo_rootx(), event.y + app.winfo_rooty())
        app.update()


# 请求文件列表并展示相关
def GetDirList(path="%2F", WhenStart=False):
    def task():
        fileList.pack_forget()
        Home_Frame.pack_forget()
        ProgressBar.pack(side=ttk.TOP, fill=ttk.X)
        Home_Frame.pack(fill=ttk.BOTH, expand=True)

        ROOTPATH_URL = URL + router["dirList"] + path
        cookies = ReadCookies()
        session = requests.Session()
        session.keep_alive = False
        session.cookies = cookies
        response = session.get(ROOTPATH_URL)
        status_code = response.json()['code']
        if status_code == 0:
            # 网络请求完成后，安排一个回调函数在主线程中执行
            app.after(0, update_gui, response)
        elif status_code == 40016:
            dialogs.Messagebox.show_error(message='目录不存在')
        elif status_code == 401:
            pass
        else:
            dialogs.Messagebox.show_error(message='未知错误：' + response.text)
        fileList.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=True)

    # 利用线程防止卡GUI
    def update_gui(response):
        fileList.delete(*fileList.get_children())  # 清空文件列表
        path2 = path.replace('%2F', '/')
        if path2 != '/':
            fileList.insert("", '0', values=('../', '', '上级目录', ''))
        AddressBar.delete(0, END)
        AddressBar.insert(0, path2)
        global DirID
        DirID = response.json()['data']['parent']
        global RealAddress
        RealAddress = AddressBar.get()
        TitleShow = path2 + ' - ' + Cloud_name
        app.title(TitleShow)
        FileList = json.loads(response.text)
        global Policy_ID
        Policy_ID = FileList['data']['policy']['id']
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
            if type == 'file':
                name = "📄 " + name
            elif type == 'dir':
                name = "📁 " + name
            date = obj.get('date', '').replace('T', ' ').split('.')[0]
            FileID = obj.get('id', '')
            objects_list.append((name, str(size), type, date, str(FileID)))
        for itm in objects_list:
            fileList.insert("", 'end', values=itm)
        if WhenStart:
            Login_Frame.pack_forget()
            Home_Frame.pack()

        ProgressBar.pack_forget()
        scrollbar.pack(side=ttk.RIGHT, fill=ttk.Y)

    threading.Thread(target=task).start()


# 处理地址栏更改后刷新文件列表事件
def ListNewDir(event):
    Address = AddressBar.get()
    if Address == '/':
        GetDirList(RealAddress.replace('/', '%2F'))
    else:
        SearchFile(Address)

# 上传到本地存储/Onedrive事件
def UploadLocalFile():
    # 创建一个新的线程来执行文件上传的任务
    dialogs.Messagebox.show_info(message='目前传输队列很简陋，在文件-传输队列可看到模拟终端输出内容\n传输完成后自动刷新上传列表')
    upload_thread = threading.Thread(target=UploadFileLocalThread)
    upload_thread.start()

def UploadFileLocalThread():
    file_Path = filedialog.askopenfilenames()
    if file_Path != '':
        FileNumber = len(file_Path)
        log = '\n共选择了 ' + str(FileNumber) + ' 个文件，准备上传'
        Transfer_CMD.insert(END, log)
        # 循环获取文件路径、大小、名字
        for i in range(FileNumber):
            file_path = file_Path[i]
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            UploadFile_URL_Require = URL + router["fileUpload"]
            data = {
                'path': RealAddress,
                'policy_id': Policy_ID,
                'size': file_size,
                'name': file_name
             }
            session = requests.Session()
            session.keep_alive = False
            session.cookies = ReadCookies()
            response = session.put(UploadFile_URL_Require, data=json.dumps(data))
            print(response.text)
            sessionID = response.json()['data']['sessionID']
            chunk_size = response.json()['data']['chunkSize']
            try:
                Upload_URL = response.json()['data']['uploadURLs'][0]
                log = '\n上传请求成功，识别上传策略……'
                Transfer_CMD.insert(END, log)  #('非本地文件上传，识别上传地址中……')
                IsSharePoint = "sharepoint.com" in Upload_URL
                if IsSharePoint == True:
                    log = '\n识别成功，上传策略为SharePoint'
                    Transfer_CMD.insert(END, log)
                    Upload_Type = 'onedrive'
                    UploadFile_URL = Upload_URL
                    CallbackURL = URL + router["OneDriveCallback"] + sessionID
            except:
                Transfer_CMD.insert('', 'end', values='\n本地策略上传')
                Upload_Type = 'local'
                UploadFile_URL = URL + router["fileUpload"] + '/' + sessionID + '/'
            if Upload_Type == "local":
                try:
                    with open(file_path, 'rb') as f:
                        chunk_no = 0
                        for chunk_file in range(0, file_size, chunk_size):
                            chunk = f.read(chunk_size)
                            UploadFile_URL_Now = UploadFile_URL + str(chunk_no)
                            Transfer_CMD.insert('', 'end', values="\n准备上传文件 " + file_name + "的第" + chunk_no + "个分片")
                            response = session.post(UploadFile_URL_Now, data=chunk)
                            if response.json()['code'] == 0:
                                Transfer_CMD.insert('', 'end', values="\n" + file_name + '的第' + chunk_no + '个分片上传成功')
                            else:
                                Transfer_CMD.insert('', 'end', values='\n分片' + chunk_file + '上传失败，错误：' + response.json())
                            chunk_no += 1
                        Transfer_CMD.insert('', 'end', values='\n文件' + file_name + '上传成功')
                except Exception as e:
                    dialogs.Messagebox.show_error(message='上传失败，错误：' + e)
                    print(e)
            elif Upload_Type == "onedrive":
                try:
                    with open(file_path, 'rb') as file:
                        for i in range(0, file_size, chunk_size):
                            start = i
                            end = min(i + chunk_size, file_size) - 1
                            log = '\n准备上传文件 ' + file_name + '的第' + str(i) + '个分片'
                            Transfer_CMD.insert(END, log)
                            Uploader = session.put(
                                UploadFile_URL,
                                headers={
                                    'Content-Type': 'application/octet-stream',
                                    'Content-Range': f'bytes {start}-{end}/{file_size}',
                                },
                                data=file.read(chunk_size),
                            )
                        log = "\n" + file_name + '的第' + str(i) + '个分片上传成功'
                        Transfer_CMD.insert(END, log)
                    log = '\n文件' + file_name + '服务端处理中……'
                    Transfer_CMD.insert(END, log)
                    session.post(CallbackURL, json={})
                    Transfer_CMD.insert(END, '\n文件' + file_name + '上传成功')
                except Exception as e:
                    print("上传失败，错误：", e)
                GetDirList(RealAddress)
    else:
        print("未选择文件")

# 下载文件事件
def DownloadFile():
    select_ID = fileList.focus()
    selected_item_values = fileList.item(select_ID)['values']
    print(selected_item_values)
    fileID = selected_item_values[4]
    Download_Require = URL + router["fileDownload"] + fileID
    cookies = ReadCookies()
    session = requests.Session()
    session.keep_alive = False
    session.cookies = cookies
    response = session.put(Download_Require)
    Download_Path = response.json()['data']
    if Download_Path.startswith(router["fileDownload"]):
        Download_URL = URL + response.json()['data']
    else:
        Download_URL = response.json()['data']
    webbrowser.open(Download_URL)


# 刷新用户容量函数
def RefrushStorage():
    Require_URL = URL + router["userStorage"]
    cookies = ReadCookies()
    session = requests.Session()
    session.keep_alive = False
    session.cookies = cookies
    response = session.get(Require_URL)
    Storage = json.loads(response.text)
    used = convert_size(Storage['data']['used'])
    total = convert_size(Storage['data']['total'])
    accountText = config.get('account', 'nickname') + ' ' + used + '/' + total
    accountInfo.config(text=accountText)

# 搜索文件事件
def SearchVideo():
    SearchFile(Type='video')

def SearchAudio():
    SearchFile(Type='audio')

def SearchImage():
    SearchFile(Type='image')

def SearchDoc():
    SearchFile(Type='doc')

def SearchFile(Keywords='', Type='None'):
    if Keywords[0] == '/':      # 如果搜索关键词是路径
        try:
            GetDirList(Keywords)
        except Exception as e:
            print("未知错误：", e)
            return 0
        return 0
    if Type == 'None' and Keywords == '':
        dialogs.Messagebox.show_error(message='请输入搜索关键词或路径')
        return 0
    elif Type == 'None' and Keywords != '':
        Search_URL = URL + router["searchKeywords"] + Keywords
    elif Type == 'video':
        Search_URL = URL + router["searchVideo"]
    elif Type == 'audio':
        Search_URL = URL + router["searchAudio"]
    elif Type == 'image':
        Search_URL = URL + router["searchImage"]
    elif Type == 'doc':
        Search_URL = URL + router["searchDoc"]
    cookies = ReadCookies()
    session = requests.Session()
    session.keep_alive = False
    session.cookies = cookies
    response = session.get(Search_URL)
    if response.text == '404 page not found':
        dialogs.Messagebox.show_error(message='这里有个Bug，搜索功能暂时无法使用')
        return 0
    status_code = response.json()['code']
    if status_code == 0:
        fileList.delete(*fileList.get_children())  # 清空文件列表
        fileList.insert("", '0', values=('../', '', '上级目录', ''))
        AddressBar.delete(0, END)
        app.title('搜索结果 - ' + Cloud_name)
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
            if type == 'file':
                name = "📄 " + name
            elif type == 'dir':
                name = "📁 " + name
            date = obj.get('date', '').replace('T', ' ').split('.')[0]
            FileID = obj.get('id', '')
            objects_list.append((name, str(size), type, date, str(FileID)))
        for itm in objects_list:
            fileList.insert("", 'end', values=itm)
    else:
        dialogs.Messagebox.show_error(message='未知错误：' + response.text)

# 从文件预览中返回
def filePreview_Back():
    title = RealAddress
    title = title + " - " + Cloud_name
    app.title(title)
    FilePreview_Frame.pack_forget()
    Home_Frame.pack(fill=BOTH, expand=YES)
    TextPreview_textbox.delete(1.0, END)

# 处理密码框与验证码框回车即登录事件
def Entry_on_enter_pressed(event):
    login()

# 处理OTP框回车即登录事件
def OTP_Entry_on_enter_pressed(event):
    loginOTP()

# 右键刷新事件
def ReFrush():
    GetDirList(path=RealAddress)
    RefrushStorage()

# 新建文件事件
def MakeFile():
    FileName = dialogs.Querybox.get_string(title='新建文件', prompt='请输入文件名称')
    if FileName != '':
        MakeDir_URL = URL + router["MakeFile"]
        data = {
            'path': RealAddress + "/" + FileName
        }
        cookies = ReadCookies()
        session = requests.Session()
        session.keep_alive = False
        session.cookies = cookies
        response = session.post(MakeDir_URL, json=data)
        if response.status_code == 200:
            status_code = response.json()['code']
            if status_code == 0:
                GetDirList(path=RealAddress)
            else:
                dialogs.Messagebox.show_error(message='未知错误：' + response.text)
    else:
        dialogs.Messagebox.show_error(message='文件名不能为空')

# 新建文件夹事件
def MakeDir():
    DirName = dialogs.Querybox.get_string(title='新建文件夹', prompt='请输入文件夹名称')
    if DirName != '':
        MakeDir_URL = URL + router["MakeDir"]
        DirPath = RealAddress + '/' + DirName
        data = {'path': DirPath}
        cookies = ReadCookies()
        session = requests.Session()
        session.keep_alive = False
        session.cookies = cookies
        response = session.put(MakeDir_URL, json=data)
        if response.status_code == 200:
            status_code = response.json()['code']
            if status_code == 0:
                GetDirList(path=RealAddress)
            else:
                dialogs.Messagebox.show_error(message='未知错误：' + response.text)
    else:
        dialogs.Messagebox.show_error(message='文件夹名不能为空')

# 删除文件相关
def DeleteFile():
    DeleteURL = URL + router["DeleteFileDir"]
    select_ID = fileList.focus()
    PreDeleteFileID = fileList.item(select_ID)['values'][4]
    PreDeleteFileName = fileList.item(select_ID)['values'][0].replace('📄 ', '')
    message = '您确定要删除 ' + PreDeleteFileName + ' 吗？'
    RealDelete = dialogs.Messagebox.yesno(message=message, title='删除对象')
    if RealDelete == '确认' or RealDelete == 'Yes':
        data = {
            'items': [PreDeleteFileID]}
        cookies = ReadCookies()
        session = requests.Session()
        session.keep_alive = False
        session.cookies = cookies
        response = session.delete(DeleteURL, data=json.dumps(data))
        if response.status_code == 200:
            status_code = response.json()['code']
            if status_code == 0:
                pass
            else:
                print(response.text)
                dialogs.Messagebox.show_error(message='未知错误：' + response.text)
        else:
            dialogs.Messagebox.show_error(message='文件夹名不能为空')
        GetDirList(path=RealAddress)
        RefrushStorage()

# 删除文件夹相关
def DeleteDir():
    DeleteURL = URL + router["DeleteFileDir"]
    select_ID = fileList.focus()
    PreDeleteDirID = fileList.item(select_ID)['values'][4]
    PreDeleteDirName = fileList.item(select_ID)['values'][0].replace('📁 ', '')
    message = '您确定要删除 ' + PreDeleteDirName + ' 吗？'
    RealDelete = dialogs.Messagebox.yesno(message=message, title='删除对象')
    if RealDelete == '确认' or RealDelete == 'Yes':
        data = {
            'dirs': [PreDeleteDirID]}
        cookies = ReadCookies()
        session = requests.Session()
        session.keep_alive = False
        session.cookies = cookies
        response = session.delete(DeleteURL, data=json.dumps(data))
        if response.status_code == 200:
            status_code = response.json()['code']
            if status_code == 0:
                pass
            else:
                print(response.text)
                dialogs.Messagebox.show_error(message='未知错误：' + response.text)
        else:
            dialogs.Messagebox.show_error(message='文件夹名不能为空')
        GetDirList(path=RealAddress)
        RefrushStorage()

# WebDAV页面
def WebDAVPage():
    def task():
        ProgressBar.pack(fill=ttk.X)

        app.title("连接 - " + Cloud_name)
        Home_Frame.pack_forget()
        WebDAV_Settings_Frame.pack(fill=BOTH, expand=YES)
        WebDAV_URL = URL + router["webdavAccount"]
        cookies = ReadCookies()
        session = requests.Session()
        session.keep_alive = False
        session.cookies = cookies
        response = session.get(WebDAV_URL)
        status_code = response.json()['code']
        if status_code == 0:
            # 网络请求完成后，安排一个回调函数在主线程中执行
            app.after(0, update_gui, response)

    def update_gui(response):
        WebDAV_List.delete(*WebDAV_List.get_children())
        WebDAVList = json.loads(response.text)
        objects = WebDAVList['data']['accounts']
        objects_List = []
        objects = WebDAVList.get('data', {}).get('accounts', [])
        for obj in objects:
            Name = obj.get('Name', '')
            Password = obj.get('Password', '')
            Root = obj.get('Root', '')
            CreatedAt = obj.get('CreatedAt', '').replace('T', ' ').split('.')[0]
            objects_List.append([Name, Password, Root, CreatedAt])
        for itm in objects_List:
            WebDAV_List.insert('', 'end', values=itm)

        ProgressBar.pack_forget()

    threading.Thread(target=task).start()

# 进入WebDAV账户创建页面
def CreateWebDAVAccount():
    WebDAV_Settings_Frame.pack_forget()
    CreateWebDAVAccount_Frame.pack(fill=BOTH, expand=YES)

# 创建WebDAV账户事件
def CreateWebDAVAccountOnClick():
    WebDAV_Name = entry_WebDAV_Name.get()
    WebDAV_Path = entry_WebDAV_Path.get()
    if WebDAV_Name == '' or WebDAV_Path == '':
        dialogs.Messagebox.show_error(message='请填写完整信息')
    else:
        CreateWebDAVAccount_URL = URL + router["webdavAccount"]
        data = {
            'Name': WebDAV_Name,
            'Path': WebDAV_Path
        }
        cookies = ReadCookies()
        session = requests.Session()
        session.keep_alive = False
        session.cookies = cookies
        response = session.post(CreateWebDAVAccount_URL, json=data)
        if response.status_code == 200:
            status_code = response.json()['code']
            if status_code == 0:
                dialogs.Messagebox.show_info(message='创建成功，重新进入WebDAV页面即可看到新账户')
                ExitCreateWebDAVAccount()
            else:
                dialogs.Messagebox.show_error(message='未知错误：' + response.text)
        else:
            dialogs.Messagebox.show_error(message='未知错误：' + response.text)
        entry_WebDAV_Name.delete(0, END)
        entry_WebDAV_Path.delete(0, END)
        GetDirList(path=RealAddress)
        RefrushStorage()

# 退出WebDAV账户创建页面
def ExitCreateWebDAVAccount():
    CreateWebDAVAccount_Frame.pack_forget()
    WebDAV_Settings_Frame.pack(fill=BOTH, expand=YES)
    entry_WebDAV_Name.delete(0, END)
    entry_WebDAV_Path.delete(0, END)

# 处理WebDAV右键按下的事件
def WebDAV_List_Click(event):
    select_ID = WebDAV_List.focus()
    selected_item_values = WebDAV_List.item(select_ID)['values']
    if selected_item_values != '':
        WebDAV_Menu.post(event.x + app.winfo_rootx(), event.y + app.winfo_rooty())
        app.update()

# 处理WebDAV复制密码事件
def CopyWebDAVPassword():
    select_ID = WebDAV_List.focus()
    selected_item_values = WebDAV_List.item(select_ID)['values']
    try:
        pyperclip.copy(str(selected_item_values[1]))
        dialogs.Messagebox.show_info(message='复制密码成功')
    except:
        dialogs.Messagebox.show_error(message='未选择任何项目')

# 处理连接iOS客户端事件
def MobileConnect():
    WebDAV_Settings_Frame.pack_forget()
    ConnectMobileFrame.pack(fill=BOTH, expand=YES)
    threading.Thread(target=generate_qr_code).start()

# 生成手机端能扫描的QRCode
def generate_qr_code():
    QRCode_require_URL = URL + router["session"]
    cookies = ReadCookies()
    session = requests.Session()
    session.keep_alive = False
    session.cookies = cookies
    response = session.get(QRCode_require_URL)
    status_code = response.json()['code']
    if status_code == 0:
        QRCode = response.json()['data']
        # 生成二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=4,
        )
        qr.add_data(QRCode)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        # 将PIL图像转换为Tkinter可以显示的图片
        tk_img = ImageTk.PhotoImage(img)

        # 显示二维码
        ConnectMobile_QRCode.config(image=tk_img)
        ConnectMobile_QRCode.image = tk_img  # 需要保持对图片的引用，否则图片会被垃圾回收
    else:
        dialogs.Messagebox.show_error(message='未知错误：\n' + response.text)

# 从连接手机端返回到WebDAV页面
def ConnectMobile_Back():
    ConnectMobileFrame.pack_forget()
    WebDAV_Settings_Frame.pack(fill=BOTH, expand=YES)

def TransferList():
    Home_Frame.pack_forget()
    Transfer_List_Frame.pack(fill='both', expand=True)

# 个人设置页面
def Personal_Settings():
    Home_Frame.pack_forget()
    Personal_Settings_Frame.pack(fill=BOTH, expand=YES)

# APP设置启动
def AppSettings():
    Home_Frame.pack_forget()
    AppSettings_Frame.pack(fill=BOTH, expand=YES)
    ServerURL_Entry.delete(0, END)
    ServerURL_Entry.insert(0, URL)
    UserName_Entry.delete(0, END)
    try:
        UserName_Entry.insert(0, localaccount)
    except:
        pass
    Theme_Entry.delete(0, END)
    try:
        Theme_Entry.insert(0, config['settings']['theme'])
    except:
        Theme_Entry.insert(0, 'Light')

# 保存APP设置
def SaveAppSettings():
    try:
        if ServerURL_Entry.get() != URL:
            dialogs.Messagebox.show_warning(message='更改服务器地址需要重新登录')
            # 删除文件同目录下的HFsession
            try:
                os.remove('HFsession')
            except:
                pass
        config['account']['url'] = ServerURL_Entry.get()
        config['account']['username'] = UserName_Entry.get()
        try:
            config['settings']['theme'] = Theme_Entry.get()
        except:
            config.add_section('settings')
            config['settings']['theme'] = Theme_Entry.get()
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        dialogs.Messagebox.show_info(message='保存成功，即将重启程序')
        pid = os.getpid()
        os.execl(os.path.abspath(__file__), *sys.argv)
    except Exception as e:
        dialogs.Messagebox.show_error(message='保存失败，错误：' + str(e) + "\n如果你未打包该程序，这是正常现象，请手动重启程序。\n如果你使用单文件程序，则修改无法生效。\n本程序将会尝试自动关闭。")
        exit()

# 关于程序
def About():
    Home_Frame.pack_forget()
    app.title('关于 HFR-Cloud Desktop')
    About_Frame.pack(fill=BOTH, expand=YES)

def BackToHome():
    WebDAV_Settings_Frame.pack_forget()
    Personal_Settings_Frame.pack_forget()
    FilePreview_Frame.pack_forget()
    AppSettings_Frame.pack_forget()
    Transfer_List_Frame.pack_forget()
    Transfer_List_Frame.pack_forget()
    About_Frame.pack_forget()
    Home_Frame.pack(fill=BOTH, expand=YES)
    app.title(RealAddress + " - " + Cloud_name)

# 退出APP执行的内容
def ExitAPP():
    sys.exit()

"""
======================================
以下是前端相关
======================================
"""

app = ttk.Window(title='HFR-Cloud Desktop')
app.geometry("350x200")
app.place_window_center()
app.attributes('-alpha', 0.9)  # 设置窗口半透明
app.protocol("WM_DELETE_WINDOW", ExitAPP)
app.tk.call('tk', 'scaling', ScaleFactor / 75)

app_style = ttk.Style()
app_style.theme_use(theme['Theme'])

try:
    app.iconbitmap('favicon.ico')
    app.wm_iconbitmap('favicon.ico')
except:
    pass

ProgressBar = ttk.Progressbar(app, mode='indeterminate')
ProgressBar.start(25)

Launch_Frame = ttk.Frame(app)
Launch_Frame.pack(fill=BOTH, expand=YES)

Launching_Label = ttk.Label(Launch_Frame, text=locales['launching'], font=(Fonts, 16), wraplength=400)
Launching_Label.place(relx=0.5, rely=0.5, anchor=ttk.CENTER)

# 登录页布局
Login_Frame = ttk.Frame(app)

loginFrame = ttk.Frame(Login_Frame)
loginFrame.pack(side=ttk.LEFT, fill=BOTH, expand=YES)

LoginAppName = '登录 ' + Cloud_name
label_APPNAME = ttk.Label(loginFrame, text=LoginAppName, font=(Fonts, 24))
label_APPNAME.pack(pady=10)

"""
LoginConfigMenu = ttk.Menu(LoginAppName, relief='raised')
LoginConfigMenu.add_command(label="编辑配置文件", font=(Fonts, 10))
LoginConfigMenu.add_command(label="清除所有配置", font=(Fonts, 10))
LoginAppName.config(menu=LoginConfigMenu)
"""

errorCode = ttk.StringVar()
loginErrorCode = ttk.Label(loginFrame, bootstyle="danger", font=(Fonts, 12), textvariable=errorCode)

frame_username = ttk.Frame(loginFrame)
frame_username.pack(pady=5)

frame_password = ttk.Frame(loginFrame)
frame_password.pack(pady=5)

frame_captcha = ttk.Frame(loginFrame)
if Login_captcha:
    frame_captcha.pack(pady=5)

frame_OTP = ttk.Frame(loginFrame)

frame_button = ttk.Frame(loginFrame)
frame_button.pack(pady=5)

label_username = ttk.LabelFrame(frame_username, text=" 用 户 名 ")
label_username.pack(side=ttk.LEFT)

entry_username = ttk.Entry(label_username, width=30)
try:
    entry_username.insert(0, localaccount)
except:
    pass
entry_username.pack(padx=10, pady=10)

label_password = ttk.LabelFrame(frame_password, text=" 密 码 ")
label_password.pack(side=ttk.LEFT)

entry_password = ttk.Entry(label_password, show="•", width=30)
entry_password.pack(padx=10, pady=10)
entry_password.bind('<Return>', Entry_on_enter_pressed)

label_captcha = ttk.LabelFrame(frame_captcha, text="验 证 码")
label_captcha.pack(side=ttk.LEFT)

entry_captcha = ttk.Entry(label_captcha, width=30)
entry_captcha.pack(padx=10, pady=10)
entry_captcha.bind('<Return>', Entry_on_enter_pressed)

label_captcha_Pic = ttk.Label(loginFrame)
label_captcha_Pic.pack(pady=5)
label_captcha_Pic.bind("<Button-1>", RefrushCaptcha)

label_OTP = ttk.Labelframe(frame_OTP, text="验 证 码")
label_OTP.pack(side=ttk.LEFT)
entry_OTP = ttk.Entry(label_OTP, width=30)
entry_OTP.pack(padx=10, pady=10)
entry_OTP.bind('<Return>', OTP_Entry_on_enter_pressed)

button_login = ttk.Button(frame_button, text="登录", command=login)
button_login.pack(side=ttk.LEFT, ipadx=20, padx=5)

# 注册按钮相关
button_register = ttk.Button(frame_button, text="注册", bootstyle="outline", command=SignUP)
button_register.pack(side=ttk.LEFT, ipadx=20, padx=5)

# 忘记密码相关
button_forget = ttk.Button(frame_button, text="忘记密码", bootstyle="link", command=forgetPassword)
button_forget.pack(side=ttk.LEFT, padx=10)

# 两步验证返回按钮
button_BackToLogin = ttk.Button(frame_button, text="返回", bootstyle="outline", command=BackToLogin)

# 两步验证登录按钮
button_TwoStepLogin = ttk.Button(frame_button, text="登录", command=loginOTP)

# 登录页布局结束,云盘主页布局开始

Home_Frame = ttk.Frame(app)

MenuBar = ttk.Frame(Home_Frame)
MenuBar.pack(side=ttk.TOP, fill=ttk.X)

fileMenuButton = ttk.Menubutton(MenuBar, text="📁 文件", bootstyle=theme['Menu'])
fileMenuButton.pack(side=ttk.LEFT)

AddressBar = ttk.Entry(MenuBar)
AddressBar.insert(0, '/')
AddressBar.bind('<Return>', ListNewDir)
AddressBar.pack(side=ttk.LEFT, fill=ttk.X, padx=10, ipadx=120, expand=True)

accountInfo = ttk.Menubutton(MenuBar, text="信息加载中……", bootstyle=theme['Menu'])
accountInfo.pack(side=ttk.RIGHT)

FileMenu = ttk.Menu(fileMenuButton, relief='raised')
FileMenu.add_command(label="📁      全部文件", font=(Fonts, 10), command=GetDirList)  # /api/v3/directory/
FileMenu.add_command(label="🎞️视频", font=(Fonts, 10), command=SearchVideo)  # /api/v3/file/search/video/internal
FileMenu.add_command(label="🖼️图片", font=(Fonts, 10), command=SearchImage)  # /api/v3/file/search/image/internal
FileMenu.add_command(label="🎵      音乐", font=(Fonts, 10), command=SearchAudio)  # /api/v3/file/search/audio/internal
FileMenu.add_command(label="📄      文档", font=(Fonts, 10), command=SearchDoc)  # /api/v3/file/search/doc/internal
FileMenu.add_separator()
FileMenu.add_command(label='上传文件', font=(Fonts, 10), command=UploadLocalFile)
FileMenu.add_command(label='传输队列', font=(Fonts, 10), command=TransferList)
FileMenu.add_separator()
FileMenu.add_command(label='连接与挂载', font=(Fonts, 10), command=WebDAVPage)
fileMenuButton.config(menu=FileMenu)

UserMenu = ttk.Menu(accountInfo, relief='raised')
UserMenu.add_command(label="个人设置", font=(Fonts, 10), command=Personal_Settings)
UserMenu.add_command(label="APP设置", font=(Fonts, 10), command=AppSettings)
UserMenu.add_command(label="管理面板", font=(Fonts, 10))
UserMenu.add_command(label="退出登录", font=(Fonts, 10), command=LogOut)
UserMenu.add_separator()
UserMenu.add_command(label="关于 HeyCloud Desktop", font=(Fonts, 10), command=About)
accountInfo.config(menu=UserMenu)

fileListFrame = ttk.Frame(Home_Frame)
fileListFrame.pack(side=ttk.BOTTOM, fill=ttk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(fileListFrame, orient=VERTICAL, bootstyle="round")
scrollbar.pack(side='right', fill='y')
fileList = ttk.Treeview(fileListFrame, columns=["名称", "大小", "类型", "修改日期", 'id'], show="headings",
                        yscrollcommand=scrollbar.set)
fileList.column("名称", width=200, )
fileList.column("大小", width=50)
fileList.column("类型", width=0, stretch=False, anchor="center")
fileList.heading('类型')
fileList.column("修改日期", anchor="center")
fileList.column("id", width=0, stretch=False)
fileList.heading("名称", text="名称")
fileList.heading("大小", text="大小")
fileList.heading("类型", text="类型")
fileList.heading("修改日期", text="修改日期")
fileList.heading("id", text="id")
filelistStyle = ttk.Style()
filelistStyle.configure("Treeview", font=(Fonts, 12))
filelistStyle.configure("Treeview", rowheight=35)
fileList.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=True)
fileList.bind("<Button-1>", LeftKeyOnclick)
fileList.bind("<Double-Button-1>", filelistonclick)
fileList.bind("<Button-3>", filelistonrightclick)
scrollbar.config(command=fileList.yview)

fileList_Menu_No_Select = ttk.Menu(app)
fileList_Menu_No_Select.add_command(label="刷新", font=(Fonts, 10), command=ReFrush)
fileList_Menu_No_Select.add_separator()
fileList_Menu_No_Select.add_command(label="离线下载", font=(Fonts, 10))
fileList_Menu_No_Select.add_separator()
fileList_Menu_No_Select.add_command(label="📁 创建文件夹", font=(Fonts, 10), command=MakeDir)
fileList_Menu_No_Select.add_command(label="📄 创建文件", font=(Fonts, 10), command=MakeFile)

fileList_Menu_Select_dir = ttk.Menu(app)
fileList_Menu_Select_dir.add_command(label="进入", font=(Fonts, 10), command=RightKeyClickOpenDir)
fileList_Menu_Select_dir.add_separator()
fileList_Menu_Select_dir.add_command(label="下载", font=(Fonts, 10))
fileList_Menu_Select_dir.add_command(label="打包下载", font=(Fonts, 10))
fileList_Menu_Select_dir.add_command(label="批量获取外链", font=(Fonts, 10))
fileList_Menu_Select_dir.add_command(label='创建分享链接', font=(Fonts, 10))
fileList_Menu_Select_dir.add_command(label="详细信息", font=(Fonts, 10))
fileList_Menu_Select_dir.add_separator()
fileList_Menu_Select_dir.add_command(label="重命名", font=(Fonts, 10))
fileList_Menu_Select_dir.add_command(label="复制", font=(Fonts, 10))
fileList_Menu_Select_dir.add_command(label="移动", font=(Fonts, 10))
fileList_Menu_Select_dir.add_separator()
fileList_Menu_Select_dir.add_command(label="删除", font=(Fonts, 10), command=DeleteDir)

fileList_Menu_Select_file = ttk.Menu(app)
fileList_Menu_Select_file.add_command(label="打开", font=(Fonts, 10), command=RightKeyClickOpenFile)
fileList_Menu_Select_file.add_command(label="下载", font=(Fonts, 10), command=DownloadFile)
fileList_Menu_Select_file.add_separator()
fileList_Menu_Select_file.add_command(label="压缩", font=(Fonts, 10))
fileList_Menu_Select_file.add_command(label="创建分享链接", font=(Fonts, 10))
fileList_Menu_Select_file.add_command(label="详细信息", font=(Fonts, 10))
fileList_Menu_Select_file.add_separator()
fileList_Menu_Select_file.add_command(label="重命名", font=(Fonts, 10))
fileList_Menu_Select_file.add_command(label="复制", font=(Fonts, 10))
fileList_Menu_Select_file.add_command(label="移动", font=(Fonts, 10))
fileList_Menu_Select_file.add_separator()
fileList_Menu_Select_file.add_command(label="删除", font=(Fonts, 10), command=DeleteFile)

# 主页布局结束，文件预览界面开始

FilePreview_Frame = ttk.Frame(app)

FilePreview_title = ttk.Label(FilePreview_Frame, text="untitled.txt", font=(Fonts, 18))
FilePreview_title.pack(anchor='nw', padx=20, pady=20)

TextPreview_textbox = ttk.ScrolledText(FilePreview_Frame, font=("Consolas", 10))
TextPreview_textbox.pack(fill=ttk.BOTH, expand=True)

FilePreview_Button_Frame = ttk.Frame(FilePreview_Frame)
FilePreview_Button_Frame.pack(side=ttk.BOTTOM, anchor="se", padx=20, pady=20)

FilePreview_Save_button = ttk.Button(FilePreview_Button_Frame, text="保存 ( 暂不支持 )", state='disabled')
FilePreview_Save_button.pack(side=ttk.LEFT, padx=10, ipadx=20)

FilePreview_Cancel_button = ttk.Button(FilePreview_Button_Frame, text="取消", bootstyle='outline', command=filePreview_Back)
FilePreview_Cancel_button.pack(side=ttk.LEFT, padx=10, ipadx=20)

# 文件预览界面结束，WebDAV配置页布局开始

WebDAV_Settings_Frame = ttk.Frame(app)

WebDAV_Title_Frame = ttk.Frame(WebDAV_Settings_Frame)
WebDAV_Title_Frame.pack(anchor='n', fill=ttk.X)

WebDAV_title = ttk.Label(WebDAV_Title_Frame, text="连接", font=(Fonts, 18))
WebDAV_title.pack(side=ttk.LEFT, padx=20, pady=20)

WebDAV_Cancel_button = ttk.Button(WebDAV_Title_Frame, text="取消", bootstyle='outline', command=BackToHome)
WebDAV_Cancel_button.pack(side=ttk.RIGHT, padx=20, ipadx=20)

WebDAV_Add_button = ttk.Button(WebDAV_Title_Frame, text="添加", command=CreateWebDAVAccount)
WebDAV_Add_button.pack(side=ttk.RIGHT, padx=20, ipadx=20)

MobileConnect = ttk.Button(WebDAV_Title_Frame, text="iOS 客户端", command=MobileConnect)
MobileConnect.pack(side=ttk.RIGHT, padx=20, ipadx=20)

WebDAV_List = ttk.Treeview(WebDAV_Settings_Frame, columns=["备注名", "密码", "相对根目录", "创建日期"], show=HEADINGS)
WebDAV_List.column('备注名', width=150)
WebDAV_List.column('密码', width=350)
WebDAV_List.column('相对根目录', width=100)
WebDAV_List.column('创建日期', width=100)
WebDAV_List.heading("备注名", text="备注名")
WebDAV_List.heading("密码", text="密码")
WebDAV_List.heading("相对根目录", text="相对根目录")
WebDAV_List.heading("创建日期", text="创建日期")
WebDAV_List.bind("<Button-3>", WebDAV_List_Click)
WebDAV_List.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=True)

WebDAV_Menu = ttk.Menu(app)
WebDAV_Menu.add_command(label="复制密码", command=CopyWebDAVPassword)
WebDAV_Menu.add_command(label="开启 / 关闭只读")
WebDAV_Menu.add_command(label="开启 / 关闭反代")
WebDAV_Menu.add_command(label="删除")

# WebDAV配置页布局结束,iOS客户端连接页面开始

ConnectMobileFrame = ttk.Frame(app)

ConnectMobile_title = ttk.Label(ConnectMobileFrame, text="iOS 客户端", font=(Fonts, 18))
ConnectMobile_title.pack(anchor='nw', padx=20, pady=20)

ConnectMobile_Label = ttk.Label(ConnectMobileFrame, text="请在App Store下载“Cloudreve”应用程序，然后打开应用，并扫描以下二维码：", font=(Fonts, 12))
ConnectMobile_Label.pack(anchor="nw", padx=40)

ConnectMobile_QRCode = ttk.Label(ConnectMobileFrame)
ConnectMobile_QRCode.pack(anchor="nw", padx=40, pady=20)

ConnectMobile_Cancel = ttk.Button(ConnectMobileFrame, text="完成", command=ConnectMobile_Back)
ConnectMobile_Cancel.pack(side=ttk.RIGHT, padx=30, pady=30, ipadx=20)

# iOS客户端连接页面结束，创建WebDAV账户开始

CreateWebDAVAccount_Frame = ttk.Frame(app)

CreateWebDAVAccount_title = ttk.Label(CreateWebDAVAccount_Frame, text="创建WebDAV账户", font=(Fonts, 18))
CreateWebDAVAccount_title.pack(anchor="nw", padx=20, pady=20)

WebDAV_Name_Frame = ttk.Frame(CreateWebDAVAccount_Frame)
WebDAV_Name_Frame.pack(pady=5)

WebDAV_Path_Frame = ttk.Frame(CreateWebDAVAccount_Frame)
WebDAV_Path_Frame.pack(pady=5)

WebDAV_Button_Frame = ttk.Frame(CreateWebDAVAccount_Frame)
WebDAV_Button_Frame.pack(padx=10, pady=10)

label_WebDAV_Name = ttk.LabelFrame(WebDAV_Name_Frame, text=" 备 注 名 ")
label_WebDAV_Name.pack(side=ttk.LEFT, padx=5)

entry_WebDAV_Name = ttk.Entry(label_WebDAV_Name, width=30)
entry_WebDAV_Name.pack(padx=10, pady=10)

label_WebDAV_Path = ttk.LabelFrame(WebDAV_Name_Frame, text=" 相 对 根 目 录 ")
label_WebDAV_Path.pack(side=ttk.LEFT, padx=5)

entry_WebDAV_Path = ttk.Entry(label_WebDAV_Path, width=30)
entry_WebDAV_Path.pack(padx=10, pady=10)

WebDAV_Save = ttk.Button(WebDAV_Button_Frame, text="确定", command=CreateWebDAVAccountOnClick)
WebDAV_Save.pack(side=ttk.LEFT, padx=10, pady=10)

WebDAV_Cancel = ttk.Button(WebDAV_Button_Frame, text="取消", bootstyle="outline", command=ExitCreateWebDAVAccount)
WebDAV_Cancel.pack(side=ttk.LEFT, padx=10, pady=10)

# 创建WebDAV账户结束，传输列表页布局开始

Transfer_List_Frame = ttk.Frame(app)

Transfer_List_Title_Frame = ttk.Frame(Transfer_List_Frame)
Transfer_List_Title_Frame.pack(anchor='n', fill=ttk.X)

Transfer_List_title = ttk.Label(Transfer_List_Title_Frame, text="传输列表", font=(Fonts, 18))
Transfer_List_title.pack(side=ttk.LEFT, padx=20, pady=20)

Transfer_List_Done = ttk.Button(Transfer_List_Title_Frame, text="完成", bootstyle="outline", command=BackToHome)
Transfer_List_Done.pack(side=ttk.RIGHT, padx=20, ipadx=20, pady=20)

Transfer_CMD = ttk.ScrolledText(Transfer_List_Frame, font=(Fonts, 10))
Transfer_CMD.pack(fill=ttk.BOTH, expand=True)

# 传输列表布局结束，个人设置页布局开始

Personal_Settings_Frame = ttk.Frame(app)

Personal_Settings_title = ttk.Label(Personal_Settings_Frame, text="个人设置(待开发)", font=(Fonts, 18))
Personal_Settings_title.pack(anchor="nw", padx=20, pady=20)

Personal_Settings_info = ttk.Label(Personal_Settings_Frame, text="个人资料", font=(Fonts, 12))
Personal_Settings_info.pack(anchor="nw", padx=40)

Personal_Settings_Button_Frame = ttk.Frame(Personal_Settings_Frame)
Personal_Settings_Button_Frame.pack(padx=10, pady=10)

Personal_Avatar_Frame = ttk.Frame(Personal_Settings_Frame)
Personal_Settings_Button_Frame.pack(padx=10, pady=10)

Personal_Avatar_Pic = ttk.Label(Personal_Avatar_Frame)
Personal_Avatar_Pic.pack(side=ttk.LEFT, padx=10, pady=5)

Personal_Avatar_Name = ttk.Label(Personal_Avatar_Frame, text="头像", font=(Fonts, 10))
Personal_Avatar_Name.pack(side=ttk.LEFT, padx=10, pady=5)

Personal_Settings_Save = ttk.Button(Personal_Settings_Button_Frame, text="保存", state="disabled")
Personal_Settings_Save.pack(side=ttk.LEFT, padx=10, pady=10)

Personal_Settings_Cancel = ttk.Button(Personal_Settings_Button_Frame, text="取消", bootstyle="outline", command=BackToHome)
Personal_Settings_Cancel.pack(side=ttk.LEFT, padx=10, pady=10)

# 个人设置页布局结束，App设置页布局开始

AppSettings_Frame = ttk.Frame(app)

AppSettings_title = ttk.Label(AppSettings_Frame, text="APP 设置 (请谨慎填写，否则可能出现问题)", font=(Fonts, 18))
AppSettings_title.pack(anchor="nw", padx=20, pady=20)

ServerURL_Label = ttk.Label(AppSettings_Frame, text="服务器地址", font=(Fonts, 14))
ServerURL_Label.pack(anchor="nw", padx=40)

ServerURL_SubLabel = ttk.Label(AppSettings_Frame, text="注意前面要带http://或者https://，且结尾不需要加/", font=(Fonts, 10))
ServerURL_SubLabel.pack(anchor="nw", padx=60)

ServerURL_Entry = ttk.Entry(AppSettings_Frame, width=30)
ServerURL_Entry.pack(anchor="nw", padx=60)

UserName_Label = ttk.Label(AppSettings_Frame, text="用户名", font=(Fonts, 14))
UserName_Label.pack(anchor="nw", padx=40)

UserName_SubLabel = ttk.Label(AppSettings_Frame, text="此处保存的用户名将会在无法自动登录时自动填写", font=(Fonts, 10))
UserName_SubLabel.pack(anchor="nw", padx=60)

UserName_Entry = ttk.Entry(AppSettings_Frame, width=30)
UserName_Entry.pack(anchor="nw", padx=60)

Theme_Label = ttk.Label(AppSettings_Frame, text="主题", font=(Fonts, 14))
Theme_Label.pack(anchor="nw", padx=40)

Theme_SubLabel = ttk.Label(AppSettings_Frame, text="可以填写Light与Dark来切换", font=(Fonts, 10))
Theme_SubLabel.pack(anchor="nw", padx=60)

Theme_Entry = ttk.Entry(AppSettings_Frame, width=30)
Theme_Entry.pack(anchor="nw", padx=60)

AppSettings_Button_Frame = ttk.Frame(AppSettings_Frame)
AppSettings_Button_Frame.pack(padx=10, pady=10)

AppSettings_Save_Button = ttk.Button(AppSettings_Button_Frame, text="保存 (需要重启程序)", command=SaveAppSettings, state='disabled')
AppSettings_Save_Button.pack(side=ttk.LEFT, padx=10, pady=10, ipadx=20)

AppSettings_Cancel = ttk.Button(AppSettings_Button_Frame, text="取消", bootstyle="outline", command=BackToHome)
AppSettings_Cancel.pack(side=ttk.LEFT, padx=10, pady=10, ipadx=20)

# App设置页布局结束,管理面板页布局开始
Manage_Panel_Frame = ttk.Frame(app)

Manage_Panel_title = ttk.Label(Manage_Panel_Frame, text="管理面板(待开发)", font=(Fonts, 18))
Manage_Panel_title.pack(anchor="nw", padx=20, pady=20)

# 管理面板页布局结束，APP关于页布局开始

About_Frame = ttk.Frame(app)

About_title = ttk.Label(About_Frame,text="关于 HFR-Cloud Desktop",font=(Fonts, 18))
About_title.pack(anchor="nw",padx=20,pady=20)

About_info = ttk.Label(About_Frame,text="什么是HFR-Cloud Desktop？这是HFR-Cloud的PC端开源客户端，\n支持连接HFR-Cloud Server的网盘部分，并兼容Cloudreve v3。\n已测试的HFR-Cloud Server域名：\nhttps://i.xiaoqiu.in(目前不可用）\n\n已测试的Cloudreve域名:\nhttps://pan.xiaoqiu.in\nhttps://pan.ilisuo.cn\nHFR-Cloud在此对这些服务商表示衷心感谢。\n\n开发者：\n于小丘：HFR-Cloud Desktop整体框架，是本程序的主要开发者\n暗之旅者：对HFR-Cloud Desktop进行调试，提出相关问题的解决思路",font=(Fonts, 12))
About_info.pack(anchor="nw",padx=40)

About_info_Done = ttk.Button(About_Frame, text="完成", bootstyle="outline", command=BackToHome)
About_info_Done.pack(side=ttk.RIGHT, padx=10, ipadx=20, pady=20)

# APP布局结束

# 程序初始化线程
init_thread = threading.Thread(target=init)
init_thread.start()

# 程序主循环
app.mainloop()