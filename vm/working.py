
import time
import shutil
# from vm.vm_main import Vmare
from watchdog.observers import Observer
from watchdog.events import *

"""watchdog只实现用户上报的功能，其他功能不用管，他也实现不了，这个已经明确稍后开发
文件监控"""
class FileEventHandler(FileSystemEventHandler):

    PATH = "D:/test/副"


    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path, event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path, event.dest_path))

    def on_created(self, event):
        """
        重点监控，报这个文件夹，做两件事情。一旦有新的创建，立刻放到上个人的领导，同时把这个移动到福本里面
        :param event:
        :return:
        """
        if not event.is_directory:
            print(event.src_path)
            if event.src_path.split('\\')[-2] == '报':
                #只有报里的才会管，其他不管，

                try:

                    while Vmare().upload(event.src_path):
                        print("失败继续")

                    print("file upload OK")
                    shutil.move(event.src_path, self.PATH)
                except Exception as e:
                    print(e)
                    print("放在redis中")









    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            # print(event)

            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0}".format(event.src_path))

    # def on_any_event(self, event):
    #     #     print("都会触发")

if __name__ == "__main__":
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



