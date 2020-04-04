import os
import datetime
import sqlalchemy


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,Text
from sqlalchemy.orm import sessionmaker

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


Base = declarative_base()
class All_Texts(Base):
    '''用户文件表'''
    __tablename__ = 'all_texts'

    id = Column(Integer, primary_key=True)
    textname = Column(String(64), nullable=True)  # 模板名，和业务名字是一样的，都是成套走的。
    path = Column(String(200), nullable=False, unique=True)
    level = Column(String(60),nullable=False)  # 项目部还是公司还是工区
    department = Column(String(60),nullable=False)  # 部门
    business = Column(String(60),nullable=False)  # 业务
    any1 = Column(String(60), nullable=True)
    any2 = Column(String(60), nullable=True)
    any3 = Column(String(60), nullable=True)
    any4 = Column(String(60), nullable=True)
    any5 = Column(String(60), nullable=True)
    # created_date = Column(DateTime, default=datetime.datetime.utcnow)




def mysql_conn(business,department,level):
    """

    :param business: 业务
    :param department: 部门
    :param level:  所属
    :return:  路径地址
    """
    host = '172.16.13.1'
    user = 'root'
    password = '123456'
    port = 3306
    database = "manage_table"
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
    engine = sqlalchemy.create_engine(conn_str, echo=True)


    Session = sessionmaker(bind=engine)
    session = Session()
    name = session.query(All_Texts).filter(All_Texts.level == level).filter(
        All_Texts.business == business).filter(All_Texts.department == department).all()

    if name:
        for i in name:
            # print(i.path)
            return i.path



if __name__ == "__main__":
    host = '172.16.13.1'
    user = 'root'
    password = '123456'
    port = 3306
    database = "manage_table"
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
    engine = sqlalchemy.create_engine(conn_str, echo=True)
    # srcfile = "C:\\Users\\Admin\\Desktop\\资料PDF\\机器学习(算法篇).pdf"
    # print(change_filename(srcfile))


    Base.metadata.create_all(engine)

