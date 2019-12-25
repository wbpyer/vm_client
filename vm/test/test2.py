#
# class AAA(object):
#
#
#     def __init__(self,username,user_id):
#         self.username = username
#         self.id = user_id
#
#     def aaa(self):
#         print("ccccc")
#         return "1111"
#
#
# import threading
# class Singleton(object):
#     _instance_lock = threading.Lock()
#
#     def __init__(self,username,user_id):
#         self.username = username
#         self.id = user_id
#
#     def aaa(self):
#         print("ccccc")
#         return "1111"
#
#     def __new__(cls, *args, **kwargs):
#
#         Singleton._instance = object.__new__(cls)
#         return Singleton._instance
#
# a = Singleton("WANG",213)
# b= Singleton("WANGg",213)
#
# print(a)
# print(b)
# print(b.username)
# print(Singleton._instance.username)
#
# import  requests,time
#
#
# while 1:
#     resp = requests.get("http://127.0.0.1:5001/vm/health" )
#     print(resp.text)
#     time.sleep(3)

#
# c = "D:\\E\\人\\日\\报\\111报.txt"
# name = c.split('\\')[-1]
#
# src = c.replace("报","副")
# dest = src.split('\\')[:-1]
# print(dest)
#
# cc=""
# for i in dest:
#     cc =  cc  + i+ "\\"
# bb = cc  + name
# print(bb)
# dest =str(dest) + name
#
# print(dest)
import requests
import os



# os.system("rd/s/q  C:\\Users\\admin\\Desktop\\test")
# import os
# os.system("start explorer c:")
#
#
import socket
import json
# addrs = socket.getaddrinfo(socket.gethostname(), None)
# print([item[4][0] for item in addrs if ':' not in item[4][0]][0])
# for item in addrs:
#     print(item)

# 仅获取当前IPV4地址


# res  =  {"data": "b'MTczLjE2LjYuMTAwfDEwMjUzfHdvcmtlcnxQYXNzITIzNA=='"}



# d = {"result": {"code": "200", "data": "MTczLjE2LjYuMTAwfDEwMjUzfHdvcmtlcnxQYXNzITIzNA=="}}
#
# print(d.get("result").get("data"))
# import base64
#
# print(base64.b64decode('MTczLjE2LjYuMTAwfDEwMjUzfHdvcmtlcnxQYXNzITIzNA=='))


import win32gui
from win32.lib import win32con
from win32gui import IsWindow,IsWindowEnabled,IsWindowVisible,GetWindowText,EnumWindows

# 设置无重复的集



def foo(hwnd, mouse):
    titles = set()
    # 判断是不是窗口、是不是可用的、是不是可见的
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        # 把得到的结果赋值给a
        a = win32gui.GetWindowText(hwnd)
        # 打出
        print(win32gui.GetWindowText(hwnd))
        # 不为空时
        if a != '':
            # 当'Program Manager'不在a内时：
            if 'Program Manager' not in a:
                if '开始' not in a:
                    if '管理员' not in a:
                        # 关闭窗口
                        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                        # 最小化窗口
                        # win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        # 把所有的窗口添加到titles集内

        titles.add(GetWindowText(hwnd))
        # lt = [t for t in titles if t]
        # lt.sort()
        # for t in lt:
        #     print(t)

    # 将软件窗口置于最前


# win32gui.SetForegroundWindow(hwnd)

if __name__ == '__main__':
    # 枚举所有窗体，同时调用foo函数
    EnumWindows(foo, 0)



