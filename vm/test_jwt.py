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
# s = Serializer('fdjsklafjkldsja', expires_in=60000)
# token = s.dumps({'leader_id': "3496",
#                  'leader_name':'chen',
#                  "leader_role":"安全员",
#                     "leader_job_id":'0371',
#                  'role':"安全员","role_id":6,
#                  "job_id":'0012',
#                  "department_id":5,
#                  "department":'安全管理部'}) # user为model中封装过的对象  最新最全，的需要的token 。
#
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
#
B ={'id': 123,'name':'蒋工','role':"安全员"}
# print(B.get('u'))

c =  {"user_name":"bili",
        'payload':{'leader_id': "3496",
                 'leader_name':'chen',
                 "leader_post":"安全员",
                    "leader_job_id":'0371',
                 'post':"安全员","post_id":6,
                 "job_id":'0012',
                 "department_id":5,
                 "department":'安全管理部'},
        "user_id":761,
        }

print(json.dumps(c))

