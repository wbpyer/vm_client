"""

异常处理集合类

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