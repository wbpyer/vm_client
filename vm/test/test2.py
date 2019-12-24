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

addrs = socket.getaddrinfo(socket.gethostname(), None)
print([item[4][0] for item in addrs if ':' not in item[4][0]][0])
# for item in addrs:
#     print(item)

# 仅获取当前IPV4地址


