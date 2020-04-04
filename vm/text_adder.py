"""
模板加载器，加载到mysql里面，但是有一点，你不需要建库。
改一次，路径，存一次，就行，写出这种效果的全自动加载器
"""

from vm.file_uilts import File_utils
from vm.upload import upload_fdfs
import sqlalchemy
from vm.vm_error import All_Texts
from sqlalchemy.orm import sessionmaker


def adder(path:str,department,level,business):
    print(111111111111)
    host = '172.16.13.1'
    user = 'root'
    password = '123456'
    port = 3306
    database = "manage_table"
    conn_str = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(user, password, host, port, database)
    engine = sqlalchemy.create_engine(conn_str, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    tpath = File_utils.mk_package(path)
    print(tpath)
    ret  = upload_fdfs(tpath)
    if ret:
        file_name = ret.get('Local file name')
        file_name = file_name.split('\\')[-1]

        # mysql_date['path'] = "http://" + ret.get("Storage IP").decode() + "/" + ret.get('Remote file_id').decode()  # 最终路径
        path = ret.get('Remote file_id').decode()
        file_ip = ret.get('Storage IP').decode()

        print(path)
        s1 =All_Texts(textname=file_name,path = path,department=department,business=business,level=level)
        try :
            # session.add_all([s,s1,s2,s3,s4,d1,d2,d3,d4,d5,d6,d7,w1,w2,w3,w4])
            session.add(s1)
            session.commit()


        except Exception as e:
            session.rollback()
            print(e,"记录日志")



if __name__ == "__main__":
    #现在有了一个文件，先测试，然后再测试的基础上，在增加。

    adder("C:\\Users\\Admin\\Desktop\\我的办公桌","安全部","project","特殊工种")

