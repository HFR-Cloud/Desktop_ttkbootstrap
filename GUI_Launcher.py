# -*- coding: utf-8 -*-

# HeyCloud Desktop 作者：于小丘 / Debug：暗之旅者

# 填充程序信息
App_Version = "0.1.7"

# 填充国际化信息
zh_CN = {"login":"登录","username":"用户名：","password":"密    码：","captcha":"验证码：","OTP":"OTP验证码"}
zh_TW = {"login":"登錄","username":"用戶名：","password":"密    碼：","captcha":"驗證碼：","OTP":"OTP驗證碼"}
en_US = {"login":"Login","username":"Username","password":"Password","captcha":"Captcha","OTP":"OTP Code"}

#导入必要库
import ttkbootstrap as ttk              #ttkbootstrap   开源许可:MIT
from ttkbootstrap import dialogs        #ttkbootstrap   开源许可:MIT
from ttkbootstrap.constants import *    #ttkbootstrap   开源许可:MIT
from tkinter import filedialog          #tkinter        开源许可:Python Software Foundation License
from PIL import Image, ImageTk          #Pillow         开源许可:Python Imaging Library License
import os                               #Python         开源许可:Python Software Foundation License
import requests                         #requests       开源许可:Apache License 2.0
import json                             #Python         开源许可:Python Software Foundation License
import math                             #Python         开源许可:Python Software Foundation License
import http.cookiejar                   #Python         开源许可:Python Software Foundation License
import webbrowser                       #Python         开源许可:Python Software Foundation License
import sys                              #Python         开源许可:Python Software Foundation License
import threading                        #Python         开源许可:Python Software Foundation License
import windnd                           #windnd         开源许可:MIT
import pyotp                            #pyotp          开源许可:MIT
import base64                           #Python         开源许可:Python Software Foundation License
import io                               #Python         开源许可:Python Software Foundation License
import pyperclip                        #pyperclip      开源许可:MIT
from configparser import ConfigParser   #Python         开源许可:Python Software Foundation License
import ctypes                           #Python         开源许可:Python Software Foundation License
import qrcode                           #qrcode         开源许可:MIT

# 高分屏优化(Alpha测试)
ctypes.windll.shcore.SetProcessDpiAwareness(1)
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)

# Cookie与配置文件准备
cookie_jar = http.cookiejar.CookieJar()
config = ConfigParser()
config.read('config.ini')

# 主题配置文件预载（如果配置文件不存在则预载浅色模式）
try:
    if config['settings']['theme'] == 'light':
        theme = {'Theme':"cosmo",'Menu':'light'}
    else:
        theme = {'Theme':"darkly",'Menu':'secondary'}
except:
    theme = {'Theme':"litera",'Menu':'light'}

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

# 设置配置文件中目标Cloudreve的地址，没有则默认连接本机Cloudreve
try:
    URL = config['account']['url']
except:
    URL = "http://127.0.0.1:5212"

# 设置配置文件中的字体，没有则默认使用思源黑体，如果系统未安装思源黑体则使用默认字体
try:
    Fonts = config['settings']['fonts']
except:
    Fonts = "思源黑体"

# 从本机中读取账号密码，这一功能在后续会添加加密读取
try:
    localaccount = config.get('account','username')
    otp_key = pyotp.TOTP(config.get('account','OTPKey'))
except:
    pass

# 带验证码的登录事件
def captcha_Login():
    CAPTCHA_GET_URL = URL + '/api/v3/site/captcha' 
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

# 获取云盘信息
try:
    Cloud_Info = requests.get(URL + "/api/v3/site/config")
    if Cloud_Info.status_code == 200:
        Cloud_Info = Cloud_Info.json()
        Cloud_name = Cloud_Info['data']['title']
        captcha_Type = Cloud_Info['data']['captcha_type']
        Login_captcha = Cloud_Info['data']['loginCaptcha']
        if captcha_Type == 'recaptcha' and Login_captcha == True:
            dialogs.Messagebox.show_error(message='暂不支持登录reCaptcha的服务端')
            sys.exit()
        elif captcha_Type == 'tcaptcha' and Login_captcha == True:
            dialogs.Messagebox.show_error(message='暂不支持登录腾讯云验证码的服务端')
            sys.exit()
    # Cloud_Version = requests.get(URL + "/api/v3/site/ping").json()['data']
except:
    dialogs.Messagebox.show_error(message='程序出现错误或无法连接到服务端')
    sys.exit()

# 初始化软件服务
def init():
    entry_username.config(state='disabled')
    entry_password.config(state='disabled')
    button_login.config(state='disabled')
    errorCode.set('正在自动登录……')
    loginErrorCode.pack()
    
    # 自动登录
    try:
        SuccessLogin('',True)
    except:
        entry_username.config(state='normal')
        entry_password.config(state='normal')
        button_login.config(state='normal')
        ProgressBar.pack_forget()
        Launch_Frame.pack_forget()
        errorCode.set('自动登录失败，请手动登录')
        Home_Frame.pack_forget()
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

# 读取Cookies
def ReadCookies():
    cookies_txt = open('cookies.txt', 'r')          #以reader读取模式，打开名为cookies.txt的文件
    cookies_dict = json.loads(cookies_txt.read())   #调用json模块的loads函数，把字符串转成字典
    cookies = requests.utils.cookiejar_from_dict(cookies_dict)  #把转成字典的cookies再转成cookies本来的格式
    return cookies

# 注册与忘记密码跳转网页
def SignUP():
    SignUP_URL = URL + "/signup"
    webbrowser.open(SignUP_URL)

def forgetPassword():
    forget_URL = URL + "/forget"
    webbrowser.open(forget_URL)

# 登录成功后执行
def SuccessLogin(response,WhenStart=False):
    if WhenStart:
        AutoLoginURL = URL + "/api/v3/site/config"
        cookies = ReadCookies()
        session = requests.Session()
        session.keep_alive = False
        session.cookies = cookies
        response = session.get(AutoLoginURL)
    if not WhenStart:
        cookies_dict = requests.utils.dict_from_cookiejar(response.cookies) #把cookies转化成字典
        cookies_str = json.dumps(cookies_dict)                              #调用json模块的dumps函数，把cookies从字典再转成字符串。
        cookieWriter = open('cookies.txt', 'w')             #创建名为cookies.txt的文件，以写入模式写入内容
        cookieWriter.write(cookies_str)
        cookieWriter.close()
    if WhenStart:
            config.set('account', 'id', response.json()['data']['user']['id'])
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
        config.set('account', 'id', response.json()['data']['id'])
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
    Launch_Frame.pack_forget()
    Login_Frame.pack_forget()
    Home_Frame.pack(fill=ttk.BOTH, expand=True)
    app.geometry('800x600')
    app.place_window_center()
    TitleShow = '/ - ' + Cloud_name
    app.title(TitleShow)
    GetDirList()
    RefrushStorage()

# 刷新验证码
def RefrushCaptcha(event):
    CAPTCHA_GET_URL = URL + '/api/v3/site/captcha'  
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
        #写入Cookies
        cookies_dict = requests.utils.dict_from_cookiejar(response.cookies) #把cookies转化成字典
        cookies_str = json.dumps(cookies_dict)                              #调用json模块的dumps函数，把cookies从字典再转成字符串。
        cookieWriter = open('cookies.txt', 'w')             #创建名为cookies.txt的文件，以写入模式写入内容
        cookieWriter.write(cookies_str)
        cookieWriter.close()

# OTP登录
def loginOTP():
    entry_OTP.config(state='disabled')
    button_TwoStepLogin.config(state='disabled')
    button_BackToLogin.config(state='disabled')
    threading.Thread(target=loginOTP_Process).start()

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
                    entry_OTP.config(state='normal')
                    button_TwoStepLogin.config(state='normal')
                    button_BackToLogin.config(state='normal')
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
    LOGIN_URL = URL + '/api/v3/user/session'
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
            try:
                otp_code = otp_key.now()
                entry_OTP.insert(0,otp_code)
                loginOTP()
            except:
                pass
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
    button_login.pack(side=ttk.LEFT,ipadx=20,padx=5)
    button_register.pack(side=ttk.LEFT,ipadx=20,padx=5)
    button_forget.pack(side=ttk.LEFT,padx=10)
    frame_button.pack(pady=5)
    loginErrorCode.pack_forget()
    entry_username.config(state='normal')
    entry_password.config(state='normal')
    button_login.config(state='normal')

# 退出登录相关
def LogOut():
    # 创建新线程来处理退出登录过程
    fileList.delete(*fileList.get_children())   #清空文件列表
    ROOTPATH_URL = URL + '/api/v3/user/session'
    cookies = ReadCookies()
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

# 处理单击取消选中事件
def LeftKeyOnclick(event):
    selected_items = fileList.selection()
    for item in selected_items:
        fileList.selection_remove(item)

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
                Preview_Url = URL + "/api/v3/file/content/" + str(selected_item_values[4])
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
def GetDirList(path="%2F",WhenStart=False):
    def task():
        ProgressBar.pack(fill=ttk.X)

        ROOTPATH_URL = URL + '/api/v3/directory' + path
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
    
    # 利用线程防止卡GUI
    def update_gui(response):
        fileList.delete(*fileList.get_children())   #清空文件列表
        path2 = path.replace('%2F','/')
        if path2 != '/':
            fileList.insert("",'0',values=('../', '', '上级目录', ''))
        AddressBar.delete(0, END)
        AddressBar.insert(0, path2)
        global DirID
        DirID = response.json()['data']['parent']
        global RealAddress
        RealAddress = AddressBar.get()
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
            if type == 'file':
                name = "📄 " + name
            elif type == 'dir':
                name = "📁 " + name
            date = obj.get('date', '').replace('T', ' ').split('.')[0]
            FileID = obj.get('id', '')
            objects_list.append((name, str(size), type, date,str(FileID)))
        for itm in objects_list:
            fileList.insert("",'end',values=itm)
        if WhenStart:
            Login_Frame.pack_forget()
            Home_Frame.pack()
        
        ProgressBar.pack_forget()

    threading.Thread(target=task).start()

# 处理地址栏更改后刷新文件列表事件
def ListNewDir(event):
    Address = AddressBar.get()
    if Address == '/':
        GetDirList(RealAddress.replace('/', '%2F'))
    else:
        SearchFile(Address)

# 处理文件拖入窗口上传事件
def Dragged_Files(files):
    msg = '\n'.join((item.decode('utf-8') for item in files))
    msg = '您拖放的文件：\n' + msg
    dialogs.Messagebox.show_info(message=msg)

# 切换主题
def SwitchTheme():
    if app.theme == 'superhero':
        app.set_theme('litera')
    elif app.theme == 'litera':
        app.set_theme('superhero')

# 上传文件事件
def UploadFile():
    filename = filedialog.askopenfilename()
    if filename != "":
        UploadApp = ttk.Window(title='上传文件',themename=theme['Theme'])
        UploadApp.geometry('400x200')
        UploadApp.resizable(0,0)

        fileNameFrame = ttk.Frame(UploadApp)
        filePath = ttk.Label(fileNameFrame, text=filename)

# 下载文件事件
def DownloadFile():
    select_ID = fileList.focus()
    selected_item_values = fileList.item(select_ID)['values']
    fileID = selected_item_values[4]
    Download_Require = URL + '/api/v3/file/download/' + fileID
    cookies = ReadCookies()
    session = requests.Session()
    session.keep_alive = False
    session.cookies = cookies
    response = session.put(Download_Require)
    Download_Path = response.json()['data']
    if Download_Path.startswith('/api/v3/file/download/'):
        Download_URL = URL + response.json()['data']
    else:
        Download_URL = response.json()['data']
    webbrowser.open(Download_URL)

# 刷新用户容量函数
def RefrushStorage():
    Require_URL = URL + '/api/v3/user/storage'
    cookies = ReadCookies()
    session = requests.Session()
    session.keep_alive = False
    session.cookies = cookies
    response = session.get(Require_URL)
    Storage = json.loads(response.text)
    used = convert_size(Storage['data']['used'])
    total = convert_size(Storage['data']['total'])
    accountText = config.get('account','nickname') + ' ' + used + '/' + total
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

def SearchFile(Keywords='',Type='None'):
    if Type == 'None' and Keywords == '':
        dialogs.Messagebox.show_error(message='请输入搜索关键词或路径')
        return 0
    elif Type == 'None' and Keywords != '':
        Search_URL = URL + '/api/v3/file/search/keywords/' + Keywords
    elif Type == 'video':
        Search_URL = URL + '/api/v3/file/search/video/internal'
    elif Type == 'audio':
        Search_URL = URL + '/api/v3/file/search/audio/internal'
    elif Type == 'image':
        Search_URL = URL + '/api/v3/file/search/image/internal'
    elif Type == 'doc':
        Search_URL = URL + '/api/v3/file/search/doc/internal'
    cookies = ReadCookies()
    session = requests.Session()
    session.keep_alive = False
    session.cookies = cookies
    response = session.get(Search_URL)
    status_code = response.json()['code']
    if status_code == 0:
        fileList.delete(*fileList.get_children())   #清空文件列表
        fileList.insert("",'0',values=('../', '', '上级目录', ''))
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
            objects_list.append((name, str(size), type, date,str(FileID)))
        for itm in objects_list:
            fileList.insert("",'end',values=itm)
    else:
        dialogs.Messagebox.show_error(message='未知错误：' + response.text)

# 从文件预览中返回
def filePreview_Back():
    title = RealAddress
    title = title + " - " + Cloud_name
    app.title(title)
    FilePreview_Frame.pack_forget()
    Home_Frame.pack(fill=BOTH, expand=YES)
    TextPreview_textbox.delete(1.0,END)

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
        MakeDir_URL = URL + '/api/v3/file/create'
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
        MakeDir_URL = URL + '/api/v3/directory'
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

# TODO:删除文件相关
def DeleteFile():
    DeleteURL = URL + "/api/v3/object"
    select_ID = fileList.focus()
    FileID = fileList.item(select_ID)['values'][4]
    data = {
        'item': FileID}
    cookies = ReadCookies()
    session = requests.Session()
    session.keep_alive = False
    session.cookies = cookies
    response = session.delete(DeleteURL,data=json.dumps(data))
    if response.status_code == 200:
            status_code = response.json()['code']
            if status_code == 0:
                dialogs.Messagebox.show_info(message='删除成功')
                GetDirList(path=RealAddress)
            else:
                dialogs.Messagebox.show_error(message='未知错误：' + response.text)
    else:
        dialogs.Messagebox.show_error(message='文件夹名不能为空')

# WebDAV页面
def WebDAVPage():
    def task():
        ProgressBar.pack(fill=ttk.X)

        app.title("连接 - " + Cloud_name)
        Home_Frame.pack_forget()
        WebDAV_Settings_Frame.pack(fill=BOTH, expand=YES)
        WebDAV_URL = URL + '/api/v3/webdav/accounts'
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

# 处理WebDAV右键按下的事件
def WebDAV_List_Click(event):
    select_ID = WebDAV_List.focus()
    selected_item_values = fileList.item(select_ID)['values']
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
    print('TODO:连接iOS客户端')

# 从WebDAV返回到文件列表页
def WebDAVPage_Back():
    app.title(RealAddress + " - " + Cloud_name)
    WebDAV_Settings_Frame.pack_forget()
    Home_Frame.pack(fill=BOTH, expand=YES)

# 个人设置页面
def Personal_Settings():
    Home_Frame.pack_forget()
    Personal_Settings_Frame.pack(fill=BOTH, expand=YES)

# 从个人设置返回到文件列表页
def Personal_Settings_Back():
    Personal_Settings_Frame.pack_forget()
    Home_Frame.pack(fill=BOTH, expand=YES)

# APP设置启动
def AppSettings():
    config = open('config.ini', 'r', encoding='gb18030')
    APPSettingstextbox.insert(1.0,config.readlines())
    config.close()
    Home_Frame.pack_forget()
    AppSettings_Frame.pack(fill=BOTH, expand=YES)

def AppSettings_Save():
    config = open('config.ini', 'w', encoding='gb18030')
    config.write(APPSettingstextbox.get(1.0,END))
    config.close()
    dialogs.Messagebox.show_info(message='保存成功')
    AppSettings_Back()

# App设置返回
def AppSettings_Back():
    AppSettings_Frame.pack_forget()
    Home_Frame.pack(fill=BOTH, expand=YES)

def BuyPro():
    Home_Frame.pack_forget()
    APP_VIP_Frame.pack(fill=BOTH,expand=YES)

# 退出APP执行的内容
def ExitAPP():
    sys.exit()

"""
======================================
以下是前端相关
======================================
"""

app = ttk.Window(title='HeyCloud Desktop')
app.geometry("300x200")
app.place_window_center()
app.resizable(0,0) #禁止窗口缩放
app.attributes('-alpha',0.9) #设置窗口透明
app.protocol("WM_DELETE_WINDOW", ExitAPP)
app.tk.call('tk', 'scaling', ScaleFactor/75)

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

Launching_Label = ttk.Label(Launch_Frame, text='正在启动……',font=(Fonts,16))
Launching_Label.place(relx=0.5, rely=0.5, anchor=ttk.CENTER)

#登录页布局
Login_Frame = ttk.Frame(app)
# Login_Frame.pack(anchor=ttk.CENTER,fill=BOTH)

loginFrame = ttk.Frame(Login_Frame)
loginFrame.pack(side=ttk.LEFT,fill=BOTH, expand=YES)

LoginAppName = '登录 ' + Cloud_name
label_APPNAME = ttk.Label(loginFrame, text=LoginAppName,font=(Fonts,24))
label_APPNAME.pack(pady=10)

errorCode = ttk.StringVar()
loginErrorCode = ttk.Label(loginFrame, bootstyle="danger",font=(Fonts,12),textvariable=errorCode)

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

entry_username = ttk.Entry(label_username,width=30)
try:
    entry_username.insert(0,localaccount)
except:
    pass
entry_username.pack(padx=10,pady=10)

label_password = ttk.LabelFrame(frame_password, text=" 密 码 ")
label_password.pack(side=ttk.LEFT)

entry_password = ttk.Entry(label_password, show="•",width=30)
entry_password.pack(padx=10,pady=10)
entry_password.bind('<Return>', Entry_on_enter_pressed)

label_captcha = ttk.LabelFrame(frame_captcha, text="验 证 码")
label_captcha.pack(side=ttk.LEFT)

entry_captcha = ttk.Entry(label_captcha,width=30)
entry_captcha.pack(padx=10,pady=10)
entry_captcha.bind('<Return>', Entry_on_enter_pressed)

label_captcha_Pic = ttk.Label(loginFrame)
label_captcha_Pic.pack(pady=5)
label_captcha_Pic.bind("<Button-1>", RefrushCaptcha)

label_OTP = ttk.Labelframe(frame_OTP, text="验 证 码")
label_OTP.pack(side=ttk.LEFT)
entry_OTP = ttk.Entry(label_OTP,width=30)
entry_OTP.pack(padx=10,pady=10)
entry_OTP.bind('<Return>', OTP_Entry_on_enter_pressed)

button_login = ttk.Button(frame_button, text="登录", command=login)
button_login.pack(side=ttk.LEFT,ipadx=20,padx=5)

#注册按钮相关
button_register = ttk.Button(frame_button, text="注册",bootstyle="outline",command=SignUP)
button_register.pack(side=ttk.LEFT,ipadx=20,padx=5)

#忘记密码相关
button_forget = ttk.Button(frame_button, text="忘记密码",bootstyle="link",command=forgetPassword)
button_forget.pack(side=ttk.LEFT,padx=10)

#两步验证返回按钮
button_BackToLogin = ttk.Button(frame_button, text="返回",bootstyle="outline",command=BackToLogin)

#两步验证登录按钮
button_TwoStepLogin = ttk.Button(frame_button, text="登录",command=loginOTP)

#登录页布局结束,云盘主页布局开始

Home_Frame = ttk.Frame(app)

MenuBar = ttk.Frame(Home_Frame)
MenuBar.pack(side=ttk.TOP,fill=ttk.X)

fileMenuButton = ttk.Menubutton(MenuBar, text="📁 文件",bootstyle=theme['Menu'])
fileMenuButton.pack(side=ttk.LEFT)

AddressBar = ttk.Entry(MenuBar)
AddressBar.insert(0,'/')
AddressBar.bind('<Return>', ListNewDir)
AddressBar.pack(side=ttk.LEFT,fill=ttk.X,padx=10,ipadx=120)

accountInfo = ttk.Menubutton(MenuBar, text="信息加载中……",bootstyle=theme['Menu'])
accountInfo.pack(side=ttk.RIGHT)

FileMenu = ttk.Menu(fileMenuButton,relief='raised')
FileMenu.add_command(label="📁      全部文件",font=(Fonts,10),command=GetDirList)  #/api/v3/directory/
FileMenu.add_command(label="🎞️视频",font=(Fonts,10),command=SearchVideo)      #/api/v3/file/search/video/internal
FileMenu.add_command(label="🧩       图片",font=(Fonts,10),command=SearchImage)      #/api/v3/file/search/image/internal
FileMenu.add_command(label="🎵       音乐",font=(Fonts,10),command=SearchAudio)      #/api/v3/file/search/audio/internal
FileMenu.add_command(label="📄       文档",font=(Fonts,10),command=SearchDoc)      #/api/v3/file/search/doc/internal
FileMenu.add_separator()
FileMenu.add_command(label="🔺 上传文件",font=(Fonts,10))
FileMenu.add_command(label="🔺 上传文件夹",font=(Fonts,10))
FileMenu.add_separator()
FileMenu.add_command(label='连接',font=(Fonts,10),command=WebDAVPage)
fileMenuButton.config(menu=FileMenu)

UserMenu = ttk.Menu(accountInfo,relief='raised')
UserMenu.add_command(label="个人设置",font=(Fonts,10),command=Personal_Settings)
UserMenu.add_command(label="APP设置",font=(Fonts,10),command=AppSettings)
UserMenu.add_command(label="管理面板",font=(Fonts,10))
UserMenu.add_command(label="退出登录",font=(Fonts,10),command=LogOut)
UserMenu.add_separator()
UserMenu.add_command(label="购买 HeyCloud Desktop Pro",font=(Fonts,10),command=BuyPro)
accountInfo.config(menu=UserMenu)

fileListFrame = ttk.Frame(Home_Frame)
fileListFrame.pack(side=ttk.BOTTOM,fill=ttk.BOTH,expand=True)

scrollbar = ttk.Scrollbar(fileListFrame, orient=VERTICAL, bootstyle="round")
scrollbar.pack(side='right', fill='y')
fileList = ttk.Treeview(fileListFrame,columns=["名称","大小","类型","修改日期",'id'],show="headings",yscrollcommand=scrollbar.set)
fileList.column("名称",width=200)
fileList.column("大小",width=50)
fileList.column("类型",width=0,stretch=False)
fileList.heading('类型')
fileList.column("id",width=0,stretch=False)
fileList.heading('id')
filelistStyle = ttk.Style()
filelistStyle.configure("Treeview",font=(Fonts,12))
filelistStyle.configure("Treeview",rowheight=35)
fileList.pack(side=ttk.LEFT,fill=ttk.BOTH,expand=True)
fileList.bind("<Button-1>",LeftKeyOnclick)
fileList.bind("<Double-Button-1>",filelistonclick)
fileList.bind("<Button-3>",filelistonrightclick)
windnd.hook_dropfiles(fileList, func=Dragged_Files)
scrollbar.config(command=fileList.yview)

fileList_Menu_No_Select = ttk.Menu(app)
fileList_Menu_No_Select.add_command(label="刷新",font=(Fonts,10),command=ReFrush)
fileList_Menu_No_Select.add_separator()
fileList_Menu_No_Select.add_command(label="上传文件",font=(Fonts,10),command=UploadFile)
fileList_Menu_No_Select.add_command(label="上传目录",font=(Fonts,10))
fileList_Menu_No_Select.add_command(label="离线下载",font=(Fonts,10))
fileList_Menu_No_Select.add_separator()
fileList_Menu_No_Select.add_command(label="📁 创建文件夹",font=(Fonts,10),command=MakeDir)
fileList_Menu_No_Select.add_command(label="📄 创建文件",font=(Fonts,10),command=MakeFile)

fileList_Menu_Select_dir = ttk.Menu(app)
fileList_Menu_Select_dir.add_command(label="进入",font=(Fonts,10),command=RightKeyClickOpenDir)
fileList_Menu_Select_dir.add_separator()
fileList_Menu_Select_dir.add_command(label="下载",font=(Fonts,10))
fileList_Menu_Select_dir.add_command(label="打包下载",font=(Fonts,10))
fileList_Menu_Select_dir.add_command(label="批量获取外链",font=(Fonts,10))
fileList_Menu_Select_dir.add_command(label='创建分享链接',font=(Fonts,10))
fileList_Menu_Select_dir.add_command(label="详细信息",font=(Fonts,10))
fileList_Menu_Select_dir.add_separator()
fileList_Menu_Select_dir.add_command(label="重命名",font=(Fonts,10))
fileList_Menu_Select_dir.add_command(label="复制",font=(Fonts,10))
fileList_Menu_Select_dir.add_command(label="移动",font=(Fonts,10))
fileList_Menu_Select_dir.add_separator()
fileList_Menu_Select_dir.add_command(label="删除",font=(Fonts,10))

fileList_Menu_Select_file = ttk.Menu(app)
fileList_Menu_Select_file.add_command(label="打开",font=(Fonts,10),command=RightKeyClickOpenFile)
fileList_Menu_Select_file.add_command(label="下载",font=(Fonts,10),command=DownloadFile)
fileList_Menu_Select_file.add_separator()
fileList_Menu_Select_file.add_command(label="压缩",font=(Fonts,10))
fileList_Menu_Select_file.add_command(label="创建分享链接",font=(Fonts,10))
fileList_Menu_Select_file.add_command(label="详细信息",font=(Fonts,10))
fileList_Menu_Select_file.add_separator()
fileList_Menu_Select_file.add_command(label="重命名",font=(Fonts,10))
fileList_Menu_Select_file.add_command(label="复制",font=(Fonts,10))
fileList_Menu_Select_file.add_command(label="移动",font=(Fonts,10))
fileList_Menu_Select_file.add_separator()
fileList_Menu_Select_file.add_command(label="删除 (暂不可用，显示删除成功也无效)",font=(Fonts,10),command=DeleteFile)

# 主页布局结束，文件预览界面开始

FilePreview_Frame = ttk.Frame(app)

FilePreview_title = ttk.Label(FilePreview_Frame,text="untitled.txt",font=(Fonts, 18))
FilePreview_title.pack(anchor='nw',padx=20,pady=20)

TextPreview_textbox = ttk.ScrolledText(FilePreview_Frame,font=("Consolas",10))
TextPreview_textbox.pack(fill=ttk.BOTH,expand=True)

FilePreview_Button_Frame = ttk.Frame(FilePreview_Frame)
FilePreview_Button_Frame.pack(side=ttk.BOTTOM,anchor="se",padx=20,pady=20)

FilePreview_Save_button = ttk.Button(FilePreview_Button_Frame,text="保存 ( 暂不支持 )",state='disabled')
FilePreview_Save_button.pack(side=ttk.LEFT,padx=10,ipadx=20)

FilePreview_Cancel_button = ttk.Button(FilePreview_Button_Frame,text="取消",bootstyle='outline',command=filePreview_Back)
FilePreview_Cancel_button.pack(side=ttk.LEFT,padx=10,ipadx=20)

# 文件预览界面结束，WebDAV配置页布局开始

WebDAV_Settings_Frame = ttk.Frame(app)

WebDAV_Title_Frame = ttk.Frame(WebDAV_Settings_Frame)
WebDAV_Title_Frame.pack(anchor='n',fill=ttk.X)

WebDAV_title = ttk.Label(WebDAV_Title_Frame,text="连接",font=(Fonts, 18))
WebDAV_title.pack(side=ttk.LEFT,padx=20,pady=20)

WebDAV_Cancel_button = ttk.Button(WebDAV_Title_Frame,text="取消",bootstyle='outline',command=WebDAVPage_Back)
WebDAV_Cancel_button.pack(side=ttk.RIGHT,padx=20,ipadx=20)

WebDAV_Save_button = ttk.Button(WebDAV_Title_Frame,text="保存 ( 暂不支持 )",state='disabled')
WebDAV_Save_button.pack(side=ttk.RIGHT,padx=10,ipadx=20)

WebDAV_Add_button = ttk.Button(WebDAV_Title_Frame,text="添加 ( 暂不支持 )",state='disabled')
WebDAV_Add_button.pack(side=ttk.RIGHT,padx=20,ipadx=20)

MobileConnect = ttk.Button(WebDAV_Title_Frame,text="iOS 客户端",command=MobileConnect)
MobileConnect.pack(side=ttk.RIGHT,padx=20,ipadx=20)

WebDAV_List = ttk.Treeview(WebDAV_Settings_Frame,columns=["备注名","密码","相对根目录","创建日期"],show=HEADINGS)
WebDAV_List.column('备注名',width=150)
WebDAV_List.column('密码',width=350)
WebDAV_List.column('相对根目录',width=100)
WebDAV_List.column('创建日期',width=100)
WebDAV_List.bind("<Button-3>",WebDAV_List_Click)
WebDAV_List.pack(side=ttk.LEFT,fill=ttk.BOTH,expand=True)

WebDAV_Menu = ttk.Menu(app)
WebDAV_Menu.add_command(label="复制密码",command=CopyWebDAVPassword)
WebDAV_Menu.add_command(label="开启 / 关闭只读")
WebDAV_Menu.add_command(label="开启 / 关闭反代")
WebDAV_Menu.add_command(label="删除")

# iOS客户端连接页面

ConnectMobileFrame = ttk.Frame(app)

ConnectMobile_title = ttk.Label(ConnectMobileFrame,text="iOS 客户端",font=(Fonts, 18))
ConnectMobile_title.pack(side=ttk.LEFT,padx=20,pady=20)

ConnectMobile_Label = ttk.Label(ConnectMobileFrame,text="请在App Store下载“Cloudreve”应用程序，然后打开应用，并扫面以下二维码：",font=(Fonts, 12))
ConnectMobile_Label.pack(anchor="nw",padx=40)

# WebDAV配置页布局结束，个人设置页布局开始

Personal_Settings_Frame = ttk.Frame(app)

Personal_Settings_title = ttk.Label(Personal_Settings_Frame,text="个人设置(待开发)",font=(Fonts, 18))
Personal_Settings_title.pack(anchor="nw",padx=20,pady=20)

Personal_Settings_info = ttk.Label(Personal_Settings_Frame,text="个人资料",font=(Fonts, 12))
Personal_Settings_info.pack(anchor="nw",padx=40)

Personal_Settings_Button_Frame = ttk.Frame(Personal_Settings_Frame)
Personal_Settings_Button_Frame.pack(padx=10,pady=10)

Personal_Avatar_Frame = ttk.Frame(Personal_Settings_Frame)
Personal_Settings_Button_Frame.pack(padx=10,pady=10)

Personal_Avatar_Pic = ttk.Label(Personal_Avatar_Frame)
Personal_Avatar_Pic.pack(side=ttk.LEFT,padx=10,pady=5)

Personal_Avatar_Name = ttk.Label(Personal_Avatar_Frame,text="头像",font=(Fonts, 10))
Personal_Avatar_Name.pack(side=ttk.LEFT,padx=10,pady=5)

Personal_Settings_Save = ttk.Button(Personal_Settings_Button_Frame,text="保存",state="disabled")
Personal_Settings_Save.pack(side=ttk.LEFT,padx=10,pady=10)

Personal_Settings_Cancel = ttk.Button(Personal_Settings_Button_Frame,text="取消",bootstyle="outline",command=Personal_Settings_Back)
Personal_Settings_Cancel.pack(side=ttk.LEFT,padx=10,pady=10)

# 个人设置页布局结束，App设置页布局开始

AppSettings_Frame = ttk.Frame(app)

AppSettings_title = ttk.Label(AppSettings_Frame,text="APP 设置 (不懂请勿修改)",font=(Fonts, 18))
AppSettings_title.pack(anchor='nw',padx=20,pady=20)

APPSettingstextbox = ttk.ScrolledText(AppSettings_Frame,font=("Consolas",10))
APPSettingstextbox.pack(fill=ttk.BOTH,expand=True)

AppSettings_Button_Frame = ttk.Frame(AppSettings_Frame)
AppSettings_Button_Frame.pack(side=ttk.BOTTOM,anchor="se",padx=20,pady=20)

AppSettings_Save_button = ttk.Button(AppSettings_title,text="保存",state='disabled',command=AppSettings_Save)
AppSettings_Save_button.pack(side=ttk.RIGHT,padx=10,ipadx=20)

AppSettings_Cancel_button = ttk.Button(AppSettings_title,text="取消",bootstyle='outline',command=AppSettings_Back)
AppSettings_Cancel_button.pack(side=ttk.RIGHT,padx=10,ipadx=20)

# App设置页布局结束,管理面板页布局开始
Manage_Panel_Frame = ttk.Frame(app)

Manage_Panel_title = ttk.Label(Manage_Panel_Frame,text="管理面板(待开发)",font=(Fonts, 18))
Manage_Panel_title.pack(anchor="nw",padx=20,pady=20)

# 管理面板页布局结束，APP会员购买页开始

APP_VIP_Frame = ttk.Frame(app)

APP_VIP_title = ttk.Label(APP_VIP_Frame,text="购买 HeyCloud Desktop Pro",font=(Fonts, 18))
APP_VIP_title.pack(anchor="nw",padx=20,pady=20)

APP_VIP_info = ttk.Label(APP_VIP_Frame,text="什么是HeyCloud Desktop Pro？你可以选择支持我们的开发，作为回报获得HeyCloud Desktop的\n加强版本，即HeyCloud Desktop Pro。捐助后，你将获得以下内容：\n\n- 文件上传与下载\n- 文件预览\n- 文件同步\n- 未来的更多功能……\n\n截至2024年3月21日，捐助版的价格为个人用户3元/月，30元/年；站点授权为98元/永久。\n如果你是个人用户，请前往https://buy.xiaoqiu.in/s?item=HeyCloudDesktoppro&code=1Qy9Uz97Ynj810kTylc8D\n(点击链接可直接前往网站进行捐助)\n购买完成后请重启本程序，程序会自动获取授权信息\n\n如果你是站长，使用的是HeyCloud，可直接前往HeyCloud后台进行购买；\n若是Cloudreve，请您先证明您拥有Cloudreve Pro的信息给buypro@xiaoqiu.in，后续对接将由邮箱\n联系进行。",font=(Fonts, 12))
APP_VIP_info.pack(anchor="nw",padx=40)

# APP布局结束

# 程序初始化线程
init_thread = threading.Thread(target=init)
init_thread.start()

# 程序主循环
app.place_window_center()
app.mainloop()