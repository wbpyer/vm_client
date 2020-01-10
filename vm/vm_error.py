import os
import datetime
"""

异常处理集合类，
改名字方法

"""



class File_exists_error(Exception):  # Exception：所有的异常

    def __init__(self, msg):
        self.message = msg


class File_upload_error(Exception):
    def __init__(self, msg):
        self.message = msg




class Timeout(Exception):
    def __init__(self, msg):
        self.message = msg



def change_filename(srcfile):
    """
    文件加时间戳方法
    :param srcfile:
    :return:
    """
    try:
        print(datetime.datetime.now().strftime(("%Y-%m-%d %H:%M:%S")))
        print(srcfile.split(".")[0])

        timenow = (datetime.datetime.now().strftime(("%Y-%m-%d-%H-%M-%S")))
        dstDir = srcfile.split(".")[0] + str(timenow) + "." + (srcfile.split(".")[1])
        print(dstDir)
        os.rename(srcfile, dstDir)
        return dstDir

    except Exception as e:
        return srcfile




if __name__ == "__main__":


    srcfile = "C:\\Users\\Admin\\Desktop\\资料PDF\\机器学习(算法篇).pdf"
    print(change_filename(srcfile))


