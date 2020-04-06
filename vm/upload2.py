import requests



def download_fdfs2(path,name):
    """
    #下载FDFS，api
    :param path:文件的下载路径
    :return: 下载后FDFS返回的信息
    """

    # PATH = 'C:\\Users\\admin\\Desktop\\我的办公桌\\我的办公桌.zip'    # 下到本机后变成什么。
    # PATH = 'C:\\Users\\worker\\Desktop\\我的办公桌\\我的办公桌.zip'
    # path = "C:\\Users\\worker\\Desktop\\我的办公桌\\"+str(name)+"的办公桌.zip"
    # path = str(path)+str(name)+"的办公桌.zip"
    localpath="C:\\Users\\worker\\Desktop\\"+str(name)+"的办公桌.zip"
    print('######################################')
    print(path)
    # print(name)
    fdfs_url = "http://172.16.240.1:8888/" + path
    print(fdfs_url)
    req = requests.get(fdfs_url)
    print(req)

    with open(localpath, 'wb') as fobj:
        fobj.write(req.content)
        print("dowload over")


def download_fdfs3(path,name):
    """
    #下载FDFS，api
    :param path:文件的下载路径
    :return: 下载后FDFS返回的信息
    """

    # PATH = 'C:\\Users\\admin\\Desktop\\我的办公桌\\我的办公桌.zip'    # 下到本机后变成什么。
    # PATH = 'C:\\Users\\worker\\Desktop\\我的办公桌\\我的办公桌.zip'
    # path = "C:\\Users\\worker\\Desktop\\我的办公桌\\"+str(name)+"的办公桌.zip"
    # path = str(path)+str(name)+"的办公桌.zip"
    localpath="C:\\Users\\worker\\Desktop\\我的办公桌\\"+str(name)+"的办公桌.zip"
    print('######################################')
    print(path)
    # print(name)
    fdfs_url = "http://172.16.240.1:8888/" + path
    print(fdfs_url)
    req = requests.get(fdfs_url)
    print(req)

    with open(localpath, 'wb') as fobj:
        fobj.write(req.content)
        print("dowload over")
    # try:
    #     # print(zipfile.ZipFile.namelist(r"C:\\Users\\Admin\\Desktop\\我的办公桌.zip"))
    #     with zipfile.ZipFile("C:\\Users\\Admin\\Desktop\\我的办公桌\\我的办公桌.zip", mode="a") as f:
    #         f.write(localpath)  # 追加写入压缩文件
    # except Exception as e:
    #     print("异常对象的类型是:%s" % type(e))
    #     print("异常对象的内容是:%s" % e)
    # finally:
    #     f.close()
