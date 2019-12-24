from fdfs_client.client import get_tracker_conf,Fdfs_client
from vm.file_uilts import File_utils
import requests
import json
import random
import os


TRCKER_CONF = 'C:\\Users\\Admin\\Desktop\\client0.conf' # FDFS配置文件
# TRCKER_CONF = 'C:\\programdata\\client0.conf'





"""这里面的方法，可以考虑封装成类。上传类，里面有各种方法，这个思路好。封装成类方法，而不是实例"""

def mk_meta_data_zip(ret:dict,payload:dict,user_id,user_name) -> dict :
    """
    创建sql前的数据准备，这里有两方面考虑
    一是上传文件成功之后，返回的数据
    二是token 里的用户数据。 但是这个目前我还想不到解析方式，暂时再说，先用上面的把程序跑通。

    :param ret:字典
    :return:
    字典
    """

# todo这里还要加上领导的数据，给报这个功能去用。

    mysql_date = {}
    file_name = ret.get('Local file name')
    mysql_date['file_name'] = file_name.split('\\')[-1]

    # mysql_date['path'] = "http://" + ret.get("Storage IP").decode() + "/" + ret.get('Remote file_id').decode()  # 最终路径
    mysql_date['path'] = ret.get('Remote file_id').decode()
    mysql_date['file_ip'] = ret.get('Storage IP').decode()


    mysql_date['department_id'] = payload.get('department_id') # 需要什么数据，去负载里面求出来即可。
    mysql_date['department'] = payload.get('department')
    mysql_date['role'] = payload.get('role')
    mysql_date["role_id"] = payload.get('role_id')

    mysql_date["user_id"] = user_id
    mysql_date["user_name"] = user_name

    return mysql_date



def mk_meta_data_leader(ret:dict,payload:dict,user_id,user_name) -> dict:
    """

    :param ret:
    :param payload:
    :return:
    """


    mysql_date = {}
    file_name = ret.get('Local file name')
    mysql_date['file_name'] = file_name.split('\\')[-1]

    # mysql_date['path'] = "http://" + ret.get("Storage IP").decode() + "/" + ret.get('Remote file_id').decode()  # 最终路径
    mysql_date['path'] = ret.get('Remote file_id').decode()
    mysql_date['file_ip'] = ret.get('Storage IP').decode()
    status_id = file_name.split('\\')[-2] #草，报，收，垃
    # date_id = file_name.split('\\')[-3]
    # work_id = file_name.split('\\')[-4]
    mysql_date['status_id'] = status_id
    # mysql_date['date_id'] = date_id
    # mysql_date['work_id'] = work_id
    mysql_date['role'] = payload.get('role')
    mysql_date["role_id"] = payload.get('role_id')

    mysql_date["user_id"] = user_id
    mysql_date["user_name"] = user_name

    mysql_date['department_id'] = payload.get('department_id')  # 需要什么数据，去负载里面求出来即可。
    mysql_date['department'] = payload.get('department')
    # 需要什么数据，去负载里面求出来即可。
    #上报领导的其他数据，如果和这个人相等，就直接拿，或者去token里，或者就留空。
    print(mysql_date)
    return mysql_date

def mk_meta_data(ret:dict,payload:dict,user_id,user_name) -> dict :
    """
    创建sql前的数据准备，这里有两方面考虑
    一是上传文件成功之后，返回的数据
    二是token 里的用户数据。 但是这个目前我还想不到解析方式，暂时再说，先用上面的把程序跑通。

    :param ret:字典
    :return:
    字典
    """

# todo这里还要加上领导的数据，给报这个功能去用。

    mysql_date = {}
    file_name = ret.get('Local file name')
    mysql_date['file_name'] = file_name.split('\\')[-1]

    # mysql_date['path'] = "http://" + ret.get("Storage IP").decode() + "/" + ret.get('Remote file_id').decode()  # 最终路径
    mysql_date['path'] = ret.get('Remote file_id').decode()
    mysql_date['file_ip'] = ret.get('Storage IP').decode()
    status_id= file_name.split('\\')[-2]
    # date_id = file_name.split('\\')[-3]
    # work_id = file_name.split('\\')[-4]
    mysql_date['status_id'] = status_id
    # mysql_date['date_id'] = date_id
    # mysql_date['work_id'] = work_id
    mysql_date['department_id'] = payload.get('department_id') # 需要什么数据，去负载里面求出来即可。
    mysql_date['department'] = payload.get('department')
    mysql_date['role'] = payload.get('role')
    mysql_date["role_id"] = payload.get('role_id')

    mysql_date["user_id"] = user_id
    mysql_date["user_name"] = user_name

                                                                                                                                                                                     

    # if status_id in ['草','报','副','垃']:
    #
    #     payload['status_id'] = status_id
    # else:
    #     payload['status_id'] = "无"
    # if date_id in ['日','周','月','年']:
    #     payload['date_id'] =  date_id
    # else:
    #     payload['date_id'] = "无"
    # if work_id in  ['人','机','物','法']:
    #     payload['work_id'] = work_id
    # else:
    #     payload['work_id'] = '无'
    return mysql_date





def upload_fdfs(path:str):
    """
    #上传FDFS，api
    :param path:文件的绝对路径
    :return: 上传后FDFS返回的信息
    """

    trackers = get_tracker_conf(TRCKER_CONF)
    client = Fdfs_client(trackers)
    ret = client.upload_by_filename(path)
    if ret.get('Status') == 'Upload successed.':

        return ret
    return



def upload_mydb(payload:dict,address,port,dbname:str,type):
    """
    上传mysql
    api,向数据库端发送请求，把数据打过去就行，接受数据端的返回就可以。
    :param payload:  入库所需要的数据。
    :param address: 数据库端地址。
    :param port:
    :return:
    """
    # print(payload)
    # print("http://"+ str(address) +":"+str(port)+"/db/"+ dbname + "/excel/add")

    if type == "zip":
        resp = requests.post("http://"+ str(address) +":"+str(port)+"/db/"+ dbname + "/vm_latest/add", json=payload)
    elif type == "leader":

        resp = requests.post("http://" + str(address) + ":" + str(port) + "/db/" + dbname + "/excel/add/leader", json=payload)
    elif type == "delete":
        resp = requests.post("http://"+ str(address) +":"+str(port)+"/db/"+ dbname + "/excel/delete", json=payload)


    else:
        resp = requests.post("http://"+ str(address) +":"+str(port)+"/db/"+ dbname + "/excel/add", json=payload)

    return resp




def download_fdfs(path):
    """
    #下载FDFS，api
    :param path:文件的下载路径
    :return: 下载后FDFS返回的信息
    """

    PATH = 'C:\\Users\\admin\\Desktop\\我的办公桌\\我的办公桌.zip'# 下到本机后变成什么。
    # PATH = 'C:\\Users\\worker\\Desktop\\我的文件\\我的文件.zip'
    fdfs_url = "http://172.16.13.1:8080/" + path
    req = requests.get(fdfs_url)

    with open(PATH, 'wb') as fobj:
        fobj.write(req.content)
        print("dowload over")



# def download_fdfs_file(path:str,name,work_id,date_id):
def download_fdfs_file(path:str,name):
    """
    下载别人上报的数据
    :param path:  下载路径
    :param name:  文件名
    :param work_id:  项目id
    :param date_id:  日期id
    :return:
    """
     # 下到本机后变成什么。

    # if date_id == 1:
    #     date_id = "日"
    # elif date_id == 2:
    #     date_id = "周"
    # elif date_id == 3:
    #     date_id = "旬"
    # elif date_id == 4:
    #     date_id = "月"
    # elif date_id == 5:
    #     date_id = "季"
    # elif date_id == 6:
    #     date_id = "半"
    # elif date_id == 7:
    #     date_id = "年"
    #
    #
    #
    # if work_id == 1:
    #     work_id = "人"
    # elif work_id == 2:
    #     work_id = "机"
    # elif work_id == 3:
    #     work_id = "物"
    # elif work_id == 4:
    #     work_id = "法"

    dest = "C:\\Users\\admin\\Desktop\\我的办公桌\\收\\" + name
    # dest = "C:\\Users\\worker\\Desktop\\我的文件\\收\\" + name
    # dest = "C:\\Users\\worker\\Desktop\\test\\{0}\\{1}\\收\\".format(work_id,date_id)+ name
    if not os.path.exists(dest):
        # todo 这里的逻辑就是，如果存在收的这个文件，就什么都不做，如果不在就下载，证明这个时新报送上来的，这里已经实线了，就这么办。

        url = "http://172.16.13.1:8080/" + path
        req = requests.get(url)

        with open(dest, 'wb') as fobj:
            fobj.write(req.content)
            print("dowload over")

    return







def connection(service:str):
    """
    万用连接器，连接主服务器，请求子服务的地址。
    :param server:
    :return:
    """
    main_list = ['http://172.16.13.1:5001/service/'+ service, 'http://172.16.13.1:5001/service/'+ service]

    server = random.choice(main_list)
    resp = requests.get(server)
    print(resp.status_code)
    #这里主服务已经做健康检查了，如果这也不行，那证明服务器全挂了，直接抛异常就行，下载不了，也上传不了。
    if resp.status_code != 200:
        raise Exception("无法连接服务器")

    resp = json.loads(resp.text)
    data = resp.get("data")
    address = data.get('address')
    port = data.get('port')

    return address,port


if __name__ == "__main__":
    print(connection("db"))
    # print(download_fdfs(b'group1/M00/00/00/rBANAV3pyB-AAhuPAAAD5ApngSo070.zip'))
    # File_utils.unzip()




