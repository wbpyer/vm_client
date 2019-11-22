import requests
import json
import time
from vm.upload import upload_fdfs ,upload_mydb,mk_meta_data,connection,download_fdfs
from vm.file_uilts import File_utils
from watchdog.observers import Observer
from vm.working import FileEventHandler


"""目前想到用FLASK接受请求。然后解析出来，今天不写了，业务基本完成，明天写接受服务器的请求解析。"""


class Vmare():
    """
    客户每次登陆虚拟机，必须带着token,里面是各种信息。 要用。从前端，发过来，我去解析，然后拿到数据，
    数据格式是json字典形式。
    """
    PATH =r'D:/test'  # 工作区绝对路径地址


    def __init__(self,payload:dict,user_id,user_name):
        '''接到用户后，需要去做的工作。解析负载过来的数据,需要什么数据，就去字典里面拿'''
        self.role = payload.get('role')
        self.user_id = user_id
        self.work_id = payload.get('work_id')
        self.user_name = user_name
        self.db_name = str(self.user_id) + str(self.work_id) + self.user_name + self.role
        # self.depart = payload.get('depart')


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
        except Exception as e:
            print(e)


    def upload(self,file,dbname):
        """
        替用户上传文件
        :param file:
        :return:
        """
        ret = upload_fdfs(file)
        if ret:
            data = mk_meta_data(ret)

            service = connection('sun')
            resp = upload_mydb(data, *service,dbname)
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
        event_handler = FileEventHandler()
        observer.schedule(event_handler, r'D:/test', recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


    def exit(self):
        '''用户退出时，要做的工作。
        替用户保存好数据，两路，一个是单独，一个是打包，考虑用线程'''
        files = File_utils.get_all_file()
        for file in files:
            if len(file.split('\\')) > 4 and file.split('\\')[-2] in ['草', '报', '副', '垃']:
                #如果符合条件就开始上传。不符合条件，就不管。
                try:

                    while self.upload(file):
                        print("失败继续")

                    print("file upload OK")
                except Exception as e:
                    print(e)
                    print("放在redis中")
                #记录日志，那个用户的那个文件没有上传成功。
        try:
            zippath = File_utils.mk_package()
            while self.upload(zippath):
                print("失败继续")
            print("zip upload OK")
        except Exception as e:
            print(e)
            print("放在redis中")


        print("全部执行完毕，可以清屏")





