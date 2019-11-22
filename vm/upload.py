from fdfs_client.client import *
import requests
import json
"""这里面的方法，可以考虑封装成类。上传类，里面有各种方法，这个思路好。封装成类方法，而不是实例"""




def mk_meta_data(ret:dict):
    """
    创建sql前的数据准备，这里有两方面考虑
    一是上传文件成功之后，返回的数据
    二是token 里的用户数据。 但是这个目前我还想不到解析方式，暂时再说，先用上面的把程序跑通。

    :param ret:字典
    :return:
    字典
    """

# todo这里还要加上领导的数据，给报这个功能去用。

    payload = {}
    file_name = ret.get('Local file name')
    payload['file_name'] = file_name.split('\\')[-1]
    # 'D:\\test\\人\\日\\报\\新建文本文档.txt'
    payload['path'] = "http://" + ret.get("Storage IP").decode() + "/" + ret.get('Remote file_id').decode()  # 最终路径

    status_id= file_name.split('\\')[-2]
    date_id = file_name.split('\\')[-3]
    work_id = file_name.split('\\')[-4]
    payload['status_id'] = status_id
    payload['date_id'] = date_id
    payload['work_id'] = work_id
    payload['leader'] = 'leader'

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
    return payload




def upload_fdfs(path:str):
    """
    #上传FDFS，api
    :param path:文件的绝对路径
    :return: 上传后FDFS返回的信息
    """

    trackers = get_tracker_conf(r'C:\Users\Admin\Desktop\client.conf')
    client = Fdfs_client(trackers)
    ret = client.upload_by_filename(path)
    if ret.get('Status') == 'Upload successed.':

        return ret
    return



def upload_mydb(payload:dict,address,port,dbname:str):
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
    resp = requests.post("http://"+ str(address) +":"+str(port)+"/db/"+ dbname + "/excel/add", data=payload)


    return resp



def download_fdfs(path:str):
    """
    #下载FDFS，api
    :param path:文件的下载路径
    :return: 下载后FDFS返回的信息
    """
    PATH = 'C:\\Users\\Admin\\Desktop\\工作区.zip' # 下到本机后变成什么。
    trackers = get_tracker_conf(r'C:\Users\Admin\Desktop\client.conf')
    client = Fdfs_client(trackers)
    ret = client.download_to_file(PATH, path)
    return ret





def connection(service:str):
    """
    万用连接器，连接主服务器，请求子服务的地址。
    :param server:
    :return:
    """
    main_list = ['http://127.0.0.1:5000/service/'+ service, 'http://127.0.0.1:5000/service/'+ service]
    server = random.choice(main_list)
    resp = requests.get(server)
    #这里主服务已经做健康检查了，如果这也不行，那证明服务器全挂了，直接抛异常就行，下载不了，也上传不了。
    if resp.status_code != 200:
        raise Exception("无法连接服务器")

    resp = json.loads(resp.text)
    address = resp.get('address')
    port = resp.get('port')
    return address,port



