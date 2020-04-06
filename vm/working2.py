import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from vm.vm_error import change_filename
import requests
import json




class Group_FileEvent(FileSystemEventHandler):


    filelist = [] #测试用

    def __init__(self,vm):
        self.vm = vm
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        """
        只有改名才会走这个接口
        :param event:
        :return:
        """
        if not event.is_directory:
            print("文件改名src:{0},des:{1}".format(event.src_path,event.dest_path))
            self.vm.move_name(event.src_path)
            #todo 改名冗余问题，已经解决

            self.vm.filelist.append(event.dest_path) # 目标文件存起来，最后统一做处理。


    def on_created(self, event):
        """
        重点监控，报这个文件夹，做两件事情。一旦有新的创建，立刻放到上个人的领导，
        :param event:
        :return:
        """
        if not event.is_directory:
            print("文件创建{0}".format(event.src_path))
            print(event.src_path)
            self.vm.filelist.append(event.src_path)


            if event.src_path.split('\\')[-2] in ['报 安全部',"报 物资设备部","报 经营部","报 工程部"]:
                #只有报里的才会管，其他不管，
                 #这里是一个，数据库要重新设计，否则查不到。
                #根据业务查库，找到你要报的人的数据库，然后报。这里需要书库库端的配合

                try:

                    #这里就不在区分工区往下了，只是到了工区就行，就不用再区分是安全，还是工程什么的了
                    department = event.src_path.split('\\')[-2].split(" ")[-1]

                    # business = event.src_path.split('\\')[-3]

                    # dic = {"busines":business,"department":department,"family":self.vm.family}

                    dic = { "department": department, "family": self.vm.family}
                    records = requests.post("http://172.16.13.1:5000/mysql/findbusi",json=dic)
                    #接口过去查
                    records = json.loads(records.text) # 拿到一个列表或者空


                    if records:

                        newpath = change_filename(event.src_path)
                        self.vm.group2project(records,newpath)
                             # 报送之前给文件名字加时间戳，目前只加了报


                        print("file upload leader OK")


                    # file_name = event.src_path.split('\\')[-1]
                    #
                    # src = event.src_path.replace("报", "副")
                    # dest = src.split('\\')[:-1]
                    # des = ""
                    # for i in dest:
                    #     des = des + i + "\\"
                    # dest = des + "(副本)" + file_name
                    #
                    # shutil.move(event.src_path, dest)  #再放到自己的副本



                except Exception as e:
                    print ("报送文件没有上报成功{0}".format(e))
                    print("存入redis做备份")





            if event.src_path.split('\\')[-2] == '回收站':

                try :

                    self.vm.upload_garbage(event.src_path)
                    print("失败继续上传")
                    os.remove(event.src_path)
                except Exception as e:
                    print("需要删除文件没有上报成功{}".format(e))
                    print("存入redis做备份")





    def on_deleted(self, event):
        if not event.is_directory:
            print("file deleted:{0}".format(event.src_path))


    def on_modified(self, event):
        #文件在不同文件夹中移动走的是这个通道。更改数据内容也走这个通道。
        if not event.is_directory:

            print("文件修改{0}".format(event.src_path))
            self.vm.filelist.append(event.src_path)


    # def on_any_event(self, event): 所有对文件的行为，都会在这里被触发掉
    #         print("都会触发")



if __name__ == "__main__":
    #测试用例,只是测试用
    observer = Observer()
    event_handler = Group_FileEvent()
    observer.schedule(event_handler, r'D:/test', recursive=True)
    observer.start()
    work = True
    while work:
        time.sleep(1)
        a = input("input:")
        if a == 'quit':
            work = False
            print(a)
            print(Group_FileEvent.filelist)
            print(list(set(Group_FileEvent.filelist)))
            l = list(set(Group_FileEvent.filelist))
            for i in l:
                if i.split('\\')[-2] in ['草',"副"]:
                    #这里只解决这两个逻辑，就行，上面已经解决了两个。，这样就把用户所有的文件都给管住了。
                    print(i)

    observer.stop()
    observer.join()

