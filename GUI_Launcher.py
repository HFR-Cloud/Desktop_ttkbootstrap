# -*- coding: utf-8 -*-

#导入必要库
import ttkbootstrap as ttk
from ttkbootstrap import dialogs
from PIL import Image, ImageTk
import os,sys
import requests
import json
import math
import http.cookiejar
import webbrowser
from configparser import ConfigParser

#登录页图片展示准备
current_dir = os.path.dirname(os.path.abspath(__file__))
resources_dir = os.path.join(current_dir, 'Resources')

cookie_jar = http.cookiejar.CookieJar()
config = ConfigParser()
config.read('config.ini')

try:
    URL = config['account']['url']
except:
    URL = "http://localhost:5212"

try:
    localaccount = localpassword = ""
    localaccount = config.get('account','username')
    localpassword = config.get('account','password')
except:
    print('没有保存账号密码')

def SignUP():
    SignUP_URL = URL + "/signup"
    webbrowser.open(SignUP_URL)

def FogetPassword():
    Foget_URL = URL + "/foget"
    webbrowser.open(Foget_URL)

def login():
    username = entry_username.get()
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
            cookies_dict = requests.utils.dict_from_cookiejar(response.cookies) #把cookies转化成字典
            cookies_str = json.dumps(cookies_dict)                              #调用json模块的dumps函数，把cookies从字典再转成字符串。
            cookieWriter = open('cookies.txt', 'w')             #创建名为cookies.txt的文件，以写入模式写入内容
            cookieWriter.write(cookies_str)
            cookieWriter.close()
            config.set('account', 'user_name', response.json()['data']['user_name'])
            config.set('account', 'nickname', response.json()['data']['nickname'])
            config.set('account', 'groupname', response.json()['data']['group']['name'])
            config.set('account', 'AllowShare', str(response.json()['data']['group']['allowShare']))
            config.set('account', 'AllowRemoteDownload', str(response.json()['data']['group']['allowRemoteDownload']))
            config.set('account', 'AllowArchiveDownload', str(response.json()['data']['group']['allowArchiveDownload']))
            config.set('account','AdvanceDelete', str(response.json()['data']['group']['advanceDelete']))
            config.set('account', 'AllowWebDAVProxy', str(response.json()['data']['group']['allowWebDAVProxy']))
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            GetDirList()
            loginErrorCode.pack_forget()
            pictureFrame.pack_forget()
            label.pack_forget()
            loginFrame.pack_forget()
            MenuBar.pack(side=ttk.TOP,fill=ttk.X)
            fileList.pack(side=ttk.LEFT,fill=ttk.BOTH,expand=True)
            screenWidth = app.winfo_screenwidth() # 获取显示区域的宽度
            screenHeight = app.winfo_screenheight() # 获取显示区域的高度
            width = 800 # 设定窗口宽度
            height = 600 # 设定窗口高度
            left = (screenWidth - width) / 2
            top = (screenHeight - height) / 2
            app.geometry("%dx%d+%d+%d" % (width, height, left, top))
        elif status_code == 40001:
            errorCode.set('账号密码不能为空')
        elif status_code == 40017:  #账号被封禁
            errorCode.set('账号被封禁')
        elif status_code == 40018:  #账号尚未激活
            errorCode.set('账号尚未激活，请在邮箱中确认')
        elif status_code == 40020:  #用户名或密码错误
            errorCode.set('用户名或密码错误')
        else:
            raise Exception("未知错误")
        if status_code != 0:
            loginErrorCode.pack()

def LogOut():
    ROOTPATH_URL = URL + '/api/v3/user/session'
    cookies_txt = open('cookies.txt', 'r')          #以reader读取模式，打开名为cookies.txt的文件
    cookies_dict = json.loads(cookies_txt.read())   #调用json模块的loads函数，把字符串转成字典
    cookies = requests.utils.cookiejar_from_dict(cookies_dict)  #把转成字典的cookies再转成cookies本来的格式
    session = requests.Session()
    session.cookies = cookies
    response = session.delete(ROOTPATH_URL)
    if response.status_code == 200:
        status_code = response.json()['code']
        if status_code == 0:        #退出登录成功
            dialogs.Messagebox.ok(message='退出登录成功，重启应用生效')
            sys.exit()

def convert_size(size_bytes):
    if size_bytes == 0:
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s%s" % (s, size_name[i])

def GetDirList(path="%2F"):
    ROOTPATH_URL = URL + '/api/v3/directory' + path
    cookies_txt = open('cookies.txt', 'r')          #以reader读取模式，打开名为cookies.txt的文件
    cookies_dict = json.loads(cookies_txt.read())   #调用json模块的loads函数，把字符串转成字典
    cookies = requests.utils.cookiejar_from_dict(cookies_dict)  #把转成字典的cookies再转成cookies本来的格式
    session = requests.Session()
    session.cookies = cookies
    response = session.get(ROOTPATH_URL)
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
        date = obj.get('date', '').replace('T', ' ').split('.')[0]
        objects_list.append((name, str(size), date))
    for itm in objects_list:
        fileList.insert("",'end',values=itm)
    

def getcookies():
    cookieFiles = open('cookies.txt', 'r')
    return(cookieFiles.readlines())
    
def on_enter_pressed(event):
    login()

app = ttk.Window(themename='superhero')
app.title("海枫云存储")
screenWidth = app.winfo_screenwidth() # 获取显示区域的宽度
screenHeight = app.winfo_screenheight() # 获取显示区域的高度
width = 625 # 设定窗口宽度
height = 350 # 设定窗口高度
left = (screenWidth - width) / 2
top = (screenHeight - height) / 2
app.resizable(0,0) #禁止窗口缩放

#登录页布局

image_path = os.path.join(resources_dir, 'Logo.png')
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)

pictureFrame = ttk.Frame(app)
pictureFrame.pack(side=ttk.LEFT)

label = ttk.Label(pictureFrame, image=photo)
label.pack(side=ttk.RIGHT)

loginFrame = ttk.Frame(app)
loginFrame.pack(side=ttk.LEFT)

iloginFrame = ttk.Frame(loginFrame)
iloginFrame.pack(side=ttk.LEFT)

label_APPNAME = ttk.Label(iloginFrame, text="登录 海枫云存储",font=('思源黑体',24))
label_APPNAME.pack(pady=10)

errorCode = ttk.StringVar()
loginErrorCode = ttk.Label(iloginFrame, bootstyle="danger",font=('思源黑体',12),textvariable=errorCode)

frame_username = ttk.Frame(iloginFrame)
frame_username.pack(pady=5)
frame_password = ttk.Frame(iloginFrame)
frame_password.pack(pady=5)
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

button_login = ttk.Button(frame_button, text="登录", command=login)
button_login.pack(side=ttk.LEFT,ipadx=20,padx=5)

#注册按钮相关
button_register = ttk.Button(frame_button, text="注册",bootstyle="outline",command=SignUP)
button_register.pack(side=ttk.LEFT,ipadx=20,padx=5)

#忘记密码相关
button_forget = ttk.Button(frame_button, text="忘记密码",bootstyle="link",command=FogetPassword)
button_forget.pack(side=ttk.LEFT,padx=10)

#登录页布局结束,云盘主页布局开始

MenuBar = ttk.Frame(app)

fileMenuButton = ttk.Menubutton(MenuBar, text="文件",bootstyle="secondary")
fileMenuButton.pack(side=ttk.LEFT)
EditMenuButton = ttk.Menubutton(MenuBar, text="编辑",bootstyle="secondary")
EditMenuButton.pack(side=ttk.LEFT)
ViewMenuButton = ttk.Menubutton(MenuBar, text="查看",bootstyle="secondary")
ViewMenuButton.pack(side=ttk.LEFT)
HelpMenuButton = ttk.Menubutton(MenuBar, text="帮助",bootstyle="secondary")
HelpMenuButton.pack(side=ttk.LEFT)

accountInfo = ttk.Menubutton(MenuBar, text="读取信息中……",bootstyle="secondary")
accountInfo.pack(side=ttk.RIGHT)

UserMenu = ttk.Menu(accountInfo,relief='raised')
UserMenu.add_command(label="个人主页")
UserMenu.add_command(label="管理面板")
UserMenu.add_command(label="退出登录",command=LogOut)
accountInfo.config(menu=UserMenu)

fileListFrame = ttk.Frame(app)
fileListFrame.pack(side=ttk.BOTTOM,fill=ttk.BOTH,expand=True)

fileList = ttk.Treeview(fileListFrame,show="headings",columns=("名称","大小","修改日期"),displaycolumns="#all")

app.geometry("%dx%d+%d+%d" % (width, height, left, top))
app.mainloop()