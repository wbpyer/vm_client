import itsdangerous
import json
import time
# salt='sdaf'#加盐，指定一个盐值，别让别人知道哦，否则就可以解密出来了
# t=itsdangerous.TimedJSONWebSignatureSerializer(salt,expires_in=600)#过期时间600秒
#
# # ==============如何加密==================
# res=t.dumps({'username':'yangfan','user_id':1})# 在t中加入传输的数据
#
#
# token=res.decode()#指定编码格式
#
# print(token)

# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# s = Serializer('fdjsklafjkldsja', expires_in=600)
# token = s.dumps({'id': 123,'name':'蒋工','role':"安全员"}) # user为model中封装过的对象
# token = token.decode()
# print(token)
# d = {}
# time.sleep(2)
# # d['username'] = 'jiang'
# # d['token'] = token
# # print(d)
# s = Serializer('fdjsklafjkldsja123')
# print(s.loads(token))
# dic = json.dumps(d)
# print(dic)

B ={'id': 123,'name':'蒋工','role':"安全员"}
print(B.get('u'))


