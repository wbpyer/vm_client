import os
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from fdfs_client.client import get_tracker_conf,Fdfs_client

"""wangyuqing"""

TRCKER_CONF = 'C:\\Users\\Admin\\Desktop\\client0.conf'  # fdfs 配置文件

class FileEventHandler(FileSystemEventHandler):
    """
    文件监控类，用来监控各种的文件操作行为
    """


    filelist = [] #测试用

    def __init__(self):

        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        """
        只有改名才会走这个接口
        :param event:
        :return:
        """
        if not event.is_directory:
            print("文件改名src:{0},des:{1}".format(event.src_path,event.dest_path))
            self.filelist.append(event.dest_path) # 目标文件存起来，最后统一做处理。


    def on_created(self, event):
        """
        重点监控，报这个文件夹，做两件事情。一旦有新的创建，立刻放到上个人的领导，同时把这个移动到副里面
        :param event:
        :return:
        """
        if not event.is_directory:
            print("文件创建{0}".format(event.src_path))

            self.filelist.append(event.src_path)


    def on_deleted(self, event):
        if not event.is_directory:
            print("file deleted:{0}".format(event.src_path))
            self.filelist.append(event.src_path+"\\del")


    def on_modified(self, event):
        #文件在不同文件夹中移动走的是这个通道。更改数据内容也走这个通道。
        if not event.is_directory:

            print("文件修改{0}".format(event.src_path))
            self.filelist.append(event.src_path)



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





def working(path:str):
    """
    实时监控文件夹，无限度循环
    :return:
    """
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    WORK = True
    while WORK:
        time.sleep(1)
        a = input("input:")
        if a == 'quit':
            WORK = False
        observer.stop()
        observer.join()


def process():
    """
    处理过程，对实时监控的文件进行最终分类处理
    :return: dict
    """

    print(FileEventHandler.filelist)
    # print(list(set(FileEventHandler.filelist)))
    l = list(set(FileEventHandler.filelist))
    d1 = {}
    d2 = {}
    d3 = {}
    d4 = {}
    d5 = {}
    dic = {}

    for i in l:
        if os.path.exists(i):


            if i.split('\\')[-2] == '垃':
                ret = upload_fdfs(i)
                path = ret.get("Remote file_id")
                filename = i.split('\\')[-1]
                d1[filename] = path
            elif i.split('\\')[-2] == '收':
                ret = upload_fdfs(i)
                path = ret.get("Remote file_id")
                filename = i.split('\\')[-1]
                d2[filename] = path
            elif i.split('\\')[-2] == '报':
                ret = upload_fdfs(i)
                path = ret.get("Remote file_id")
                filename = i.split('\\')[-1]
                d3[filename] = path
            elif i.split('\\')[-2] == 'test':
                ret = upload_fdfs(i)
                path = ret.get("Remote file_id")
                filename = i.split('\\')[-1]
                d4[filename] = path
        else:
            if i.split('\\')[-1] == 'del':
                filename = i.split('\\')[-2]
                d5[filename] = 'delete'

    dic["垃"] = d1
    dic["收"] = d2
    dic["报"] = d3
    dic["草"] = d4
    dic["删"] = d5
    return  dic




if __name__ == '__main__':
    working('C:\\Users\\Admin\\Desktop\\test')
