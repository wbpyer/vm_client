import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

"""watchdog文件监控体系"""



class FileEventHandler(FileSystemEventHandler):


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
        重点监控，报这个文件夹，做两件事情。一旦有新的创建，立刻放到上个人的领导，同时把这个移动到副里面
        :param event:
        :return:
        """
        if not event.is_directory:
            print("文件创建{0}".format(event.src_path))
            print(event.src_path)
            self.vm.filelist.append(event.src_path)
            if self.vm.leader_db_name:  # 只有你有领导，你才有报送这个功能，这样就不会出错误。没有领导，你拖到报里，什么反应都没有

                if event.src_path.split('\\')[-2] == '报':
                    #只有报里的才会管，其他不管，

                    try:

                        while self.vm.upload_leader(event.src_path):  #先放到领导里面
                            time.sleep(3)
                            print("报送失败，继续报送")

                        print("file upload leader OK")


                        file_name = event.src_path.split('\\')[-1]

                        src = event.src_path.replace("报", "副")
                        dest = src.split('\\')[:-1]
                        des = ""
                        for i in dest:
                            des = des + i + "\\"
                        dest = des + file_name

                        shutil.move(event.src_path, dest)  #再放到自己的副本



                    except Exception as e:
                        print ("报送文件没有上报成功{0}".format(e))
                        print("存入redis做备份")

            if event.src_path.split('\\')[-2] == '垃':

                try :

                    while self.vm.upload_garbage(event.src_path):
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
    event_handler = FileEventHandler()
    observer.schedule(event_handler, r'D:/test', recursive=True)
    observer.start()
    work = True
    while work:
        time.sleep(1)
        a = input("input:")
        if a == 'quit':
            work = False
            print(a)
            print(FileEventHandler.filelist)
            print(list(set(FileEventHandler.filelist)))
            l = list(set(FileEventHandler.filelist))
            for i in l:
                if i.split('\\')[-2] in ['草',"副"]:
                    #这里只解决这两个逻辑，就行，上面已经解决了两个。，这样就把用户所有的文件都给管住了。
                    print(i)

    observer.stop()
    observer.join()
















