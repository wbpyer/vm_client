import requests
import json
import time
import shutil
import os
from vm.upload import upload_fdfs ,\
    upload_mydb,mk_meta_data,connection,download_fdfs,mk_meta_data_leader,mk_meta_data_zip,download_fdfs_file
from vm.file_uilts import File_utils
from watchdog.observers import Observer
from vm.working import FileEventHandler






class Vmare():
    """
    客户每次登陆虚拟机，必须带着token,里面是各种信息。 要用。从前端，发过来，我去解析，然后拿到数据，
    数据格式是json字典形式。
    """
    PATH ='C:\\Users\\Admin\\Desktop\\test'  # 工作区绝对路径地址



    def __new__(cls, *args, **kwargs):

        Vmare._instance = object.__new__(cls)
        return Vmare._instance


    def __init__(self,payload:dict,user_id,user_name) :
        '''接到用户后，需要去做的工作。解析负载过来的数据,需要什么数据，就去字典里面拿'''
        self.role = payload.get('role')
        self.user_id = user_id
        self.job_id = payload.get('job_id')
        self.user_name = user_name
        self.db_name = str(self.user_id) + ":" + self.user_name + ":" + str(self.job_id) + ":" + self.role

        self.payload = payload
        self.initpath = b'group1/M00/00/27/wKgdgV3Fg9mAU5ooAABCJiDT1GQ030.zip'  #初始化工作区，用户有，就用自己的，没有用这个空的。
        self.filelist = []  # 用来存放更改过的文件。
        if all ([payload.get('leader_id'),payload.get('leader_name'),payload.get('leader_job_id'),payload.get('leader_role')]):

            self.leader_db_name = str(payload.get("leader_id")) + ":"+ payload.get('leader_name')+\
                                  ":" + str(payload.get('leader_job_id')) + ":"+ str(payload.get('leader_role')) #拼出领导的库名

        else:
            self.leader_db_name = None

        self.WORK = True       #用来控制工作区监控的开闭

        #todo 测试已经成功，单元1，第一步

    def start(self):
        """

        替用户下载好数据
        先查MYSQL的路径
        然后下载，
        然后解压 ,如果下不到，证明客户没有数据。那就让他继续工作就行。这里不能让程序崩溃掉。
        下载时候要考虑两点，一个是自己的最后一次文件包，而是有没有别人给报送上来的表，要去查出来
        放到自己的草里面。相对应的人机无法，日周月年，都需要放到草里面。做两方面考虑。
        :param :
        :return:
        """

        try:
            os.mkdir(self.PATH)
            address,port= connection('db')
            # address = "127.0.0.1"
            # port = 5000
            d = {"user_id": self.user_id,"user_name":self.user_name}
            resp = requests.post("http://" + str(address) + ":" + str(port) + "/mysql/" + self.db_name + "/excel/find")

            path = json.loads(resp.text)

            if path :
                path = path.encode()
                download_fdfs(path)
                File_utils.unzip()
                resp = requests.post(
                    "http://" + str(address) + ":" + str(port) + "/mysql/" + self.db_name + "/excel/find/submit",
                    json=d)

                path = json.loads(resp.text)
                if path:
                    for file in path:
                        name = file[0]
                        filepath = file[1].encode()
                        work_id = file[2]
                        date_id = file[3]
                        download_fdfs_file(filepath, name, work_id, date_id)
                else:
                    print("没有上报来的文件，继续工作")
            else:
                download_fdfs(self.initpath)
                File_utils.unzip()
                resp = requests.post(
                    "http://" + str(address) + ":" + str(port) + "/mysql/" + self.db_name + "/excel/find/submit",
                    json=d)

                path = json.loads(resp.text)
                if path:
                    for file in path:
                        name = file[0]
                        filepath = file[1].encode()
                        work_id = file[2]
                        date_id = file[3]
                        download_fdfs_file(filepath, name, work_id, date_id)
                else:
                    print("没有任何文件，已经系统初始化完成")


        except Exception as e:
            print("我是start，我有问题:{0}".format(e))



    def upload_exit(self,file,type=None):
        """
        在用户退出时替用户上传文件
        :param file:
        :return:
        """
        ret = upload_fdfs(file)
        #都得存 因为这里都是变动过的，存完之后发送到数据库那面，查数据库，如果有就更新path，没有就新建一条mysql，这个业务合适

        if ret:
            data = mk_meta_data(ret,self.payload,self.user_id,self.user_name)
            print(data)

            service = connection('db')
            # service = ("127.0.0.1",5000)
            resp = upload_mydb(data, *service,self.db_name,type)
            if resp.status_code == 200:
                return 0
            else:
                return 1
        else:
            return 1

    def upload_zip(self,file,type="zip"):
        """
        在用户退出时替用户上传文件
        :param file:
        :return:
        """
        ret = upload_fdfs(file)

        if ret:
            data = mk_meta_data_zip(ret,self.payload,self.user_id,self.user_name)
            print(data)

            service = connection('db')
            # service = ("127.0.0.1",5000)
            resp = upload_mydb(data, *service,self.db_name,type)
            if resp.status_code == 200:
                return 0
            else:
                return 1
        else:
            return 1

    def upload_garbage(self,file):
        """
        垃圾文件夹处理，先存，然后存的时候，标注成逻辑删除。
        :param file:
        :return:
        """

        ret = upload_fdfs(file)
        if ret:
            data = mk_meta_data(ret, self.payload,self.user_id,self.user_name)

            service = connection('db')
            # service = ("127.0.0.1", 5000)
            resp = upload_mydb(data, *service, self.db_name,type='delete')
            if resp.status_code == 200:
                return 0
            else:
                return 1
        else:
            return 1


    def move_name(self,path):
        dat = {}
        dat["work"] = path.split('\\')[-4]
        dat["date"] = path.split('\\')[-3]
        dat["status"] = path.split('\\')[-2]
        dat["filename"] = path.split('\\')[-1]
        dat["dbname"] = self.db_name
        address,port=connection('db')
        resp = requests.post("http://" + str(address) + ":" + str(port) + "/db"  + "/excel/movename",
                             json=dat)

        return resp.status_code




    def upload_leader(self,file):
        """
        上报领导
        :param file:
        :return:
        """
        ret = upload_fdfs(file)
        print(ret)
        if ret:
            data = mk_meta_data_leader(ret, self.payload,self.user_id,self.user_name)

            service = connection('db')
            # service = ("127.0.0.1",5000)
            resp = upload_mydb(data, *service, self.leader_db_name,type='leader')
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
            print(self.WORK)
            time.sleep(2)
            # a = input("input:")
            # if a == 'quit':
            #     self.WORK= False

        observer.stop()
        observer.join()



    def exit(self):
        '''用户退出时，要做的工作。
        替用户保存好数据，两路，一个是单独，一个是打包'''
        self.WORK = False

        self.filelist = list(set(self.filelist))
        if self.filelist: # 空的就是没改过，就不用管了
            # files = File_utils.get_all_file() 之前是遍历所有，现在就不用了只去操作改动过的就行。
            for file in self.filelist:
                if os.path.exists(file):  #判断文件是否存在。
                    if len(file.split('\\')) > 4 and file.split('\\')[-2] in ['草', '副','收']:
                        #如果符合条件就开始上传到数据库端，数据库再去做比对。不符合条件，就不管。
                        try:

                            while self.upload_exit(file):
                                time.sleep(2)
                                print("失败继续")

                            print("file upload OK")
                        except Exception as e:

                            print(e,"记录日志那个文件没有保存成功，程序可以继续运行。")
                        #记录日志，那个用户的那个文件没有上传成功。
        try:
            zippath = File_utils.mk_package(self.PATH)
            while self.upload_zip(zippath,type='zip'):
                print("失败继续")
            print("zip upload OK")
            os.remove(self.PATH+'.zip') # 上传完，清理掉

        except Exception as e:

            print(e,"放在redis中备份起来，不要让他崩掉，程序继续执行")

        shutil.rmtree(self.PATH)

        # 全部搞定，清理掉文件。
        print("全部执行完毕，可以通知运维清屏,我可以用remove清理掉文件，")



