import requests
import json
import time
# import shutil
import socket
import os
import re
import redis
from threading import Thread
from vm.vm_error import File_upload_error,mysql_conn
from vm.upload import upload_fdfs ,\
    upload_mydb,mk_meta_data,connection,download_fdfs,mk_meta_data_leader,mk_meta_data_zip,download_fdfs_file,mk_meta_data_lower
from vm.file_uilts import File_utils
from watchdog.observers import Observer
from vm.working import FileEventHandler
from flask import current_app
from vm.vm_error_backup import lastzip_add_redis,foo
from win32gui import EnumWindows
from vm.vm_error_backup import sumbit_redis_list,sumbit_redis_lower,setWallPaper





class Vmare():
    """
    客户每次登陆虚拟机，必须带着token,里面是各种信息。 要用。从前端，发过来，我去解析，然后拿到数据，
    数据格式是json字典形式。
    """
    PATH = 'C:\\Users\\worker\\Desktop\\我的办公桌'

    # PATH = 'C:\\Users\\admin\\Desktop\\我的办公桌'
    #  工作区绝对路径地址



    def __new__(cls, *args, **kwargs):

        Vmare._instance = object.__new__(cls)
        return Vmare._instance


    def __init__(self,payload:dict,user_id,user_name) :
        '''接到用户后，需要去做的工作。解析负载过来的数据,需要什么数据，就去字典里面拿'''
        self.role = payload.get('role')  #这个里面现在就是业务, 一次只能一个业务
        self.user_id = user_id
        self.job_id = payload.get('job_id')
        self.user_name = user_name
        # self.business = payload.get('business')  没有业务字段

        self.department= payload.get('department') #部门也是这一个
        self.level =  payload.get("level")  # company ,group ,project   todo 调度端也要加上。
        #这里的话，如果传入的参数发生了改变，我自己写的中端需要改变，前端要改，前端要多传入参数，到了中端验证一下
        #中端转发到虚拟机上。目前中台和前端没有这个字段，所以暂时注释掉，

        # self.templ = templater  #模板的编号，用来区分切换虚拟机的页面。暂未启用，可以为空，

        #这里换成了部门
        self.db_name = str(self.user_id) + ":" + self.user_name + ":" + str(self.job_id) + ":" + self.department


        self.payload = payload
        self.db1 = redis.Redis('172.16.13.1', 6379, 5) # 报
        self.db2 = redis.Redis('172.16.13.1', 6379, 6) # 发
        # self.initpath ='group1/M00/03/C1/rBANAV4B0QuAPQfVAAABylN4jIc348.zip'  #初始化工作区，用户有，就用自己的，没有用这个空的。
        self.filelist = []  # 用来存放更改过的文件。



        self.lead_name = payload.get('leader_name')  # 变成了一个列表，下面3个都是

        self.lead_id = payload.get('leader_id')   # 列表

        self.lead_role = payload.get('leader_role')  # 列表这个字段没啥用,仍然保留但是不用

        self.lead_job_id = payload.get('leader_job_id')     #列表

        self.leader_db_name = []

        self.lower_name = payload.get("lower_name")
        self.lower_id = payload.get("lower_id")
        self.lower_job_id = payload.get("lower_job_id")
        self.lower_role = payload.get("lower_role")   # 列表这个字段没啥用,仍然保留但是不用

        self.lower_db_name = []

        if self.lead_id:
            for i in range(len(self.lead_id)):
                self.leader_db_name.append(str(self.lead_id[i]) + ":" + str(self.lead_name[i])
                                           + ":" + str(self.lead_job_id[i]) +":"+ str(self.department))

        # if all ([payload.get('leader_id'),payload.get('leader_name'),payload.get('leader_job_id'),payload.get('leader_role')]):
        #
        #     self.leader_db_name = str(payload.get("leader_id")) + ":"+ payload.get('leader_name')+\
        #                           ":" + str(payload.get('leader_job_id')) + ":"+ str(payload.get('leader_role')) #拼出领导的库名

        else:
            self.leader_db_name = None



        if self.lower_id:
            for i in range(len(self.lower_id)):
                self.lower_db_name.append(str(self.lower_id[i]) + ":" + str(self.lower_name[i])
                                           + ":" + str(self.lower_job_id[i]) +":"+ str(self.department))

        else:
            self.lower_db_name = None


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
        3.25这个接口要重启，逻辑是根据业务查自己的库有没有数据，如果有就下载，如果没有
        就去模板库里面下载，先不考虑，调岗的问题。
        :param :
        :return:
        """

        try:
            # todo 判断一下，路径在不在，如果有就再次清理，因为是注销之后第一次登录，是可以清理的。
            if os.path.exists(self.PATH):
                os.system("rd/s/q  C:\\Users\\worker\\Desktop\\我的办公桌")
                # os.system("rd/s/q  C:\\Users\\Admin\\Desktop\\我的办公桌")

            os.mkdir(self.PATH)
            # address,port= connection('db')
            address = "172.16.13.1"
            port = 5002
            d = {"role":self.role}
            resp = requests.post("http://" + str(address) + ":" + str(port) + "/mysql/" + self.db_name + "/excel/find",json=d)
            #查询有无该业务，最后一次的登录文件。如果有，就下载。
            # print(resp)
            path = json.loads(resp.text)
            # print(path)

            if path :
                # path = path.encode()

                #下载，解压，
                download_fdfs(path)


                File_utils.unzip()

                #这里的逻辑是，查找下级给上级报送的文件，目前这里不用了，因为已经改成了实时报送，redis.
                #所以这个接口没有什么用。
                # resp = requests.post(
                #     "http://" + str(address) + ":" + str(port) + "/mysql/" + self.db_name + "/excel/find/submit",
                #     json=d)
                #
                # path = json.loads(resp.text)
                # if path:
                #     for file in path:
                #         name = file[0]
                #         filepath = file[1]
                #         # work_id = file[2]
                #         # date_id = file[3]
                #         # download_fdfs_file(filepath, name, work_id, date_id)
                #         download_fdfs_file(filepath, name)
                # else:
                #     print("没有上报来的文件，继续工作")
            else:
                #如果没有，就下载初始化的业务模板，这里建一张mysql吧，把mysql,
                try:
                    # todo 去表里面查，然后拿到向应业务的初始化模板，这里有个步骤拿到表，连接数据库
                    self.initpath = mysql_conn(self.role,self.department,self.level)

                    download_fdfs(self.initpath)
                    File_utils.unzip()
                except Exception as e:
                    print(e)



                #已经改成实时报送了， 所以不需要，下载了，redis里面把这个事情就干了。
                # resp = requests.post(
                #     "http://" + str(address) + ":" + str(port) + "/mysql/" + self.db_name + "/excel/find/submit",
                #     json=d)
                #
                # path = json.loads(resp.text)
                # if path:
                #     for file in path:
                #         name = file[0]
                #         filepath = file[1]
                #         # work_id = file[2]
                #         # date_id = file[3]
                #         # download_fdfs_file(filepath, name, work_id, date_id)
                #         download_fdfs_file(filepath, name)
                # else:
                #     print("没有任何文件，已经系统初始化完成")


        except Exception as e:
            print("我是start，我有问题:{0}".format(e))


# todo 4.2暂时更新到这里.明天继续

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

            # service = connection('db')
            service = ("172.16.13.1",5002)
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

            # service = connection('db')
            # service = ("127.0.0.1",5001)
            service = ("172.16.13.1", 5002)
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

            # service = connection('db')
            # service = ("127.0.0.1", 5001)
            service = ("172.16.13.1", 5002)
            resp = upload_mydb(data, *service, self.db_name,type='delete')
            if resp.status_code == 200:
                return 0
            else:
                return 1
        else:
            return 1


    def move_name(self,path):
        """
        对应改名的操作，如果用户对文件名做了更改，我们的程序会有怎样的反应。
        :param path:
        :return:
        """
        dat = {}
        # dat["work"] = path.split('\\')[-4]
        # dat["date"] = path.split('\\')[-3]
        dat["status"] = path.split('\\')[-2]
        dat["filename"] = path.split('\\')[-1]
        dat["dbname"] = self.db_name
        # address,port=connection('db')

        address = "172.16.13.1"
        port = 5002

        resp = requests.post("http://" + str(address) + ":" + str(port) + "/db"  + "/excel/movename",
                             json=dat)

        return resp.status_code

    def upload_lower(self,file):
        """
        下发文件，进入下面人的数据库里面管起来

        :param file:
        :return:
        """
        ret = upload_fdfs(file)

        if ret:
            lower = [i + ":" + self.role for i in self.lower_db_name]
            sumbit_redis_lower(lower, ret)

            print(ret)
            data = mk_meta_data_lower(ret, self.payload, self.user_id, self.user_name)

            # service = connection('db')
            # service = ("127.0.0.1",5001)
            service = ("172.16.13.1", 5002)
            for i in self.lower_db_name:
                resp = upload_mydb(data, *service, i, type='lower')

            return 1


    def upload_leader(self,file):
        """
        上报领导
        :param file:
        :return:
        """
        ret = upload_fdfs(file)


        if ret:
            leader = [i +":"+ self.role for i in self.leader_db_name]  # 在原有基础加上业务去标识出来这个字段.
            sumbit_redis_list(leader,ret)

            print(ret)
            data = mk_meta_data_leader(ret, self.payload,self.user_id,self.user_name)   #这里没改,就是业务字段便了

            # service = connection('db')
            # service = ("127.0.0.1",5001)
            service = ("172.16.13.1",5002)
            for i in self.leader_db_name:
                resp = upload_mydb(data, *service, i,type='leader')

            return 1




    def _3389(self,ip):



        # print(ip)
        current_app.logger.error("监控ip")
        output = os.popen("netstat -ano | findstr {0}:3389".format(ip))
        a = str(output.read())
        print(a)
        current_app.logger.error("监控ip")
        if a:
            ab = re.compile('ESTABLISHED')
            lis = re.findall(ab, a)
            print(lis)
            if  not lis:
                self.WORK = False


        else:
            print("挂断")
            self.WORK = False

        # time.sleep(3)


    def working(self):
        """
        实时监控文件，替用户完成草报副拉的文件功能
        :return:
        """


        #下面的代码是控制桌面壁纸的切换 ，增加了壁纸切换的功能 ，暂时没有启用这个功能，所以注销掉了
        #根据不同的编号，设置不同的壁纸，这个编号是前端点击时候传过来的，需要，这里可以留着以后，云调度的时候
        #可以每个人分不同的模板时候用，1到16个模板，点击哪个，前端传回来哪个，就下载哪个模板。当然前端也可以不
        #传，留一个空的字段。


        # if self.templ:
        #     判断前端传回来的模板，调取不同的壁纸，和模板。
        #     if self.templ == 1:
        #         setWallPaper(1)
        #     elif self.templ ==2:
        #         setWallPaper(2)
        #     elif self.templ ==3:
        #         setWallPaper(3)


        # os.system("start explorer C:\\Users\\Admin\\Desktop\\我的办公桌")
        os.system("start explorer C:\\Users\\worker\\Desktop\\我的办公桌")
        # todo 这里还要根据不同的权限，弹出不同的页面。这里目前好实现，一会直接一并改写出来得了。先空着，这里还没有具体落地。

        observer = Observer()
        event_handler = FileEventHandler(self)
        observer.schedule(event_handler, self.PATH, recursive=True)
        observer.start()
        addrs = socket.getaddrinfo(socket.gethostname(), None)
        ip = [item[4][0] for item in addrs if ':' not in item[4][0]][0]
        # t =  Thread(target=self._3389,args=(ip,))
        # t.start()

        while self.WORK:
            # d = {"user_id": self.user_id, "user_name": self.user_name}
            # 找报送上来的文件放到收里，存在就不放，不存在就放。

            current_app.logger.error("我在循环中不断寻找redis")
            # path = self.db1.hget(self.role,"path")
            #
            # name = self.db1.hget(self.role,"name")
            myredis = self.db_name + ":" + self.role
            #todo 这里不用动,但是实际上role里面不再是岗位,而是变成了别的东西,或者说暂时先不动.
            teps = self.db1.rpop(myredis)
            fa = self.db2.rpop(myredis)


            print(11111111,teps,222222,fa)


            if teps:
                tepl = teps.decode().split(",")

                path = tepl[0]
                name = tepl[1]


                download_fdfs_file(path,name)

            if fa:
                fal = fa.decode().split(",")

                path = fal[0]
                name = fal[1]

                download_fdfs_file(path, name)


            # self._3389(ip)
            print(self.WORK)
            time.sleep(2)
            # a = input("input:")
            # if a == 'quit':
            #     self.WORK= False

        observer.stop()
        observer.join()
        # self.exit()




    def exit(self):
        '''用户退出时，要做的工作。
        替用户保存好数据，两路，一个是单独，一个是打包'''
        # self.WORK = False

        current_app.logger.error("启动退出程序,开始退出")
        #首先关闭所有占用的窗口，特别是文件

        # try:
        #
        #     EnumWindows(foo, 0)
        # except Exception as e:
        #     print(e)



        zippath = File_utils.mk_package(self.PATH)
        lastzip_add_redis(self.user_id, self.user_name, zippath)  #打包后第一时间记录redis,防止丢失,这是重点.



        self.filelist = list(set(self.filelist))
        if self.filelist: # 空的就是没改过，就不用管了
            # files = File_utils.get_all_file() 之前是遍历所有，现在就不用了只去操作改动过的就行。
            print(self.filelist)
            for file in self.filelist:

                if os.path.exists(file):  #判断文件是否存在。
                    if  file.split('\\')[-2] in [ '我的办公桌','收','报',"发"]:
                        # 注意发送,也是发到对方的收里面
                            #如果符合条件就开始上传到数据库端，数据库再去做比对。不符合条件，就不管。
                        try:

                            self.upload_exit(file)
                            # time.sleep(2)
                            # print("失败继续")

                            print("file upload OK")
                        except Exception as e:
                            print(e, "记录日志那个文件没有保存成功，程序可以继续运行。")
                            raise File_upload_error(e)


                            #记录日志，那个用户的那个文件没有上传成功。



        self.upload_zip(zippath,type='zip')

        print("zip upload OK")
        os.remove(self.PATH+'.zip') # 上传完，清理掉


        # time.sleep(2)
        # todo“给程序一些时间释放占用资源，然后再删除”
        # shutil.rmtree(self.PATH)
        # todo  如果这里毕工是直接恢复镜像的话，就不用删除了，让毕工直接恢复就行,下面这部可以省略
        os.system("rd/s/q  C:\\Users\\worker\\Desktop\\我的办公桌")
        #
        # os.system("rd/s/q  C:\\Users\\Admin\\Desktop\\我的办公桌")



        #todo 毕工可以实现镜像，就不用考虑这个文件残留问题。有错误就捕获启动处理程序就行
        # if  not os.path.exists(self.PATH):
        # 这段代码是用来更改状态的，虚拟机状态。
        try:
            addrs = socket.getaddrinfo(socket.gethostname(), None)
            ip = [item[4][0] for item in addrs if ':' not in item[4][0]][0]
            data = {'ip':ip}
            #这里还需要拿到ip,去关闭对应的ip
            resp = requests.post("http://172.16.13.1:5001/vm/status",json = data)
            print(resp.text)
        except Exception as e:
            print(e)


        #todo 然后注销一下，然后就不用管了。可以每次登录的时候可以再删一次。

        # os.system("shutdown -c")
        #我的程序死了也没事，毕工会吊起来我






        # else:
        #     print("有残留文件，通知运维检查机器，删除掉残留文件，不能给别人用这个。需要删除掉原有残留文件。")
        #
        #     current_app.logger.error(" def_exit: 用户退出，文件夹没有删除干净")
        #     raise File_exists_error('有残留文件')

























