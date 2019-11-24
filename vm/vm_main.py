import requests
import json
import time
import os
from vm.vm.upload import upload_fdfs ,upload_mydb,mk_meta_data,connection,download_fdfs,mk_meta_data_leader
from vm.vm.file_uilts import File_utils
from watchdog.observers import Observer
from vm.vm.working import FileEventHandler





class Vmare():
    """
    客户每次登陆虚拟机，必须带着token,里面是各种信息。 要用。从前端，发过来，我去解析，然后拿到数据，
    数据格式是json字典形式。
    """
    PATH =r'D:/test'  # 工作区绝对路径地址
    WORK = True #用来控制工作区监控的开闭


    def __init__(self,payload:dict,user_id,user_name) :
        '''接到用户后，需要去做的工作。解析负载过来的数据,需要什么数据，就去字典里面拿'''
        self.role = payload.get('role')
        self.user_id = user_id
        self.work_id = payload.get('work_id')
        self.user_name = user_name
        self.db_name = str(self.user_id) + str(self.work_id) + self.user_name + self.role
        # self.depart = payload.get('depart')
        self.payload = payload
        if payload.get('leader_id') != None:

            self.leader_db_name = payload.get('role') + payload.get('leader_work_id')  #拼出领导的库名
        self.WORK = True       #用来控制工作区监控的开闭



    def start(self):
        """
        替用户下载好数据
        先查MYSQL的路径
        然后下载，
        然后解压
        :param :
        :return:
        """

        try:

            address,port= connection('db')
            resp = requests.post("http://" + str(address) + ":" + str(port) + "/mysql/" + self.db_name + "/excel/find")
            path = json.loads(resp.text)
            if download_fdfs(path):

                File_utils.unzip(self.PATH)
            else:
                raise Exception("无法通过FDFS正常下载")

        except Exception as e:
            print("无法正常下载，通知运维检查服务器")


    def upload_exit(self,file):
        """
        替用户上传文件
        :param file:
        :return:
        """
        ret = upload_fdfs(file)
        if ret:
            data = mk_meta_data(ret,self.payload)

            service = connection('db')
            resp = upload_mydb(data, *service,self.db_name)
            if resp.status_code == 200:
                return 0
            else:
                return 1
        else:
            return 1



    def upload_leader(self,file):
        """

        :param file:
        :return:
        """
        ret = upload_fdfs(file)
        if ret:
            data = mk_meta_data_leader(ret, self.payload)

            service = connection('db')
            resp = upload_mydb(data, *service, self.leader_db_name)
            if resp.status_code == 200:
                return 0
            else:
                return 1
        else:
            return 1




    def working(self):
        """
        实时监控文件，替用户完成草报副拉的文件功能
        :return:
        """
        observer = Observer()
        event_handler = FileEventHandler(self)
        observer.schedule(event_handler, self.PATH, recursive=True)
        observer.start()

        while self.WORK:
            time.sleep(1)

        observer.stop()
        observer.join()


    def exit(self):
        '''用户退出时，要做的工作。
        替用户保存好数据，两路，一个是单独，一个是打包，考虑用线程'''
        self.WORK = False
        files = File_utils.get_all_file()
        for file in files:
            if len(file.split('\\')) > 4 and file.split('\\')[-2] in ['草', '报', '副', '垃']:
                #如果符合条件就开始上传。不符合条件，就不管。
                try:

                    while self.upload_exit(file):
                        print("失败继续")

                    print("file upload OK")
                except Exception as e:

                    print(e,"记录日志那个文件没有保存成功")
                #记录日志，那个用户的那个文件没有上传成功。
        try:
            zippath = File_utils.mk_package()
            while self.upload_exit(zippath):
                print("失败继续")
            print("zip upload OK")
        except Exception as e:

            print(e,"放在redis中备份起来")


        os.remove(self.PATH)
        print("全部执行完毕，可以通知运维清屏,我可以用remove清理掉文件，")












