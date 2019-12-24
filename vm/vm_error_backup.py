import redis
from vm.upload import upload_fdfs

db = redis.Redis('172.16.13.1',6379,1)



def lastzip_add_redis(user_id,user_name,file):
    """
    把用户的文件包放在redis里面做备份。以后还原用。
    :param user_id:
    :param user_name:
    :param file:
    :return:
    """
    ret = upload_fdfs(file)

    path = ret.get('Remote file_id')
    k =  str(user_id)+":"+ user_name
    if db.set(k,path):
        return True

