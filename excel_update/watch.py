import os
import time
import shutil
import pandas as pd
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



"""
watchdog文件监控体系，非正式版本，非线上版本，只是测试版本。
记住一定不要用这个作为部署，这是测试。 未完善的作品。

"""



class FileEventHandler(FileSystemEventHandler):

    role = "一公司"
    filelist = [] #测试用

    def __init__(self):

        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        """
        只有改名才会走这个接口
        :param event:
        :return:
        """
        pass


    def on_created(self, event):
        """
        重点监控，报这个文件夹，做两件事情。一旦有新的创建，立刻放到上个人的领导，同时把这个移动到副里面
        :param event:
        :return:
        """

        if not event.is_directory:
            # print("文件创建{0}".format(event.src_path))
            # print(event.src_path)

            if event.src_path.split('\\')[-2] == '收':
                    #只有报里的才会管，其他不管，
                self.filelist.append(event.src_path)


    def on_deleted(self, event):
        pass
        # if not event.is_directory:
        #     print("file deleted:{0}".format(event.src_path))


    def on_modified(self, event):
        pass
        #文件在不同文件夹中移动走的是这个通道。更改数据内容也走这个通道。
        # if not event.is_directory:
        #
        #     print("文件修改{0}".format(event.src_path))
        #     self.filelist.append(event.src_path)


    def start(self):
        while True:
            try:
                time.sleep(1.5)  #每3秒合一次
                # print(self.filelist)
                if len(self.filelist)>=2:
                    n = set(self.filelist)
                    print("开始合并")
                    print(n)
                    # self.filelist.clear()
                    print(self.filelist)
                    w = n.pop()
                    if os.path.exists(w):
                        df = pd.read_excel(w)
                        # print(df)
                        for i in range(len(n)):
                            k= n.pop()
                            if os.path.exists(k):
                                df.update(pd.read_excel(k))

                        # df = pd.concat(li)  目前这是最成熟的方式，可以拼接多个。已经验证过
                            #path + fname + role定死的
                            #防止重名加一个时间戳
                        timer = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")


                        # path = "C:\\Users\\worker\\Desktop\\我的办公桌\\收\\"+ self.role + "施工进度表" + timer + ".xlsx"
                        path = "C:\\Users\\Admin\\Desktop\\我的办公桌\\收\\"+ self.role + "施工进度表" + timer + ".xlsx"
                        # dest = "C:\\Users\\worker\\Desktop\\我的办公桌\\报\\"+ self.role + " 施工进度表" + timer + ".xlsx"
                        dest = "C:\\Users\\Admin\\Desktop\\我的办公桌\\收\\"+ self.role + "施工进度表" + timer + ".xlsx"
                        df.to_excel(path, index = False)

                        if os.path.exists(path):
                            shutil.move(path,dest)
                                # print(df)

                    self.filelist.clear()
            except Exception as e:
                print(e)



if __name__ == "__main__":
    #测试用例,只是测试用

    observer = Observer()
    event_handler = FileEventHandler()
    # observer.schedule(event_handler, r'C:\\Users\\worker\\Desktop\\我的办公桌', recursive=True)
    observer.schedule(event_handler, r'C:\\Users\\Admin\\Desktop\\我的办公桌', recursive=True)
    observer.start()
    event_handler.start()

    observer.stop()
    observer.join()



















