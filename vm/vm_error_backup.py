import redis
import win32gui,win32api
from vm.upload import upload_fdfs
from win32.lib import win32con
from win32gui import IsWindow,IsWindowEnabled,IsWindowVisible,GetWindowText



db = redis.Redis('172.16.13.1',6379,1)  # 这是给数据丢失整包恢复用的
db1 = redis.Redis('172.16.13.1',6379,5)  # 这是在收文件时候，快速循环时候用的。去里面查找，有没有别人报送上来的文件。
db2 = redis.Redis('172.16.13.1',6379,6) # 查找有没有人发过来的文件



def sumbit_redis(leader_role,ret):
    """
    向redis提交报送文件，要上报的文件，目前没有启用这个接口。hash类型
    :param user_id:
    :param user_name:
    :param file:
    :return:
    """


    path = ret.get('Remote file_id')
    file_name = ret.get('Local file name')
    file_name = file_name.split('\\')[-1]

    # k = str(l_user_id) + ":" + l_user_name
    for i in range(len(leader_role)):

        db1.hset(name=leader_role[i],key='path',value=path)
        db1.hset(name=leader_role[i],key='name',value=file_name)


def sumbit_redis_lower(lower_role,ret):

    """
    下发文件的时候存入redis中
    :param lower_role:
    :param ret:
    :return:
    """
    path = ret.get('Remote file_id')
    file_name = ret.get('Local file name')

    file_name = file_name.split('\\')[-1]
    print(1111111111111111111, file_name)
    print(1111111111111111111, path)

    # k = str(l_user_id) + ":" + l_user_name
    value = path.decode() + "," + file_name
    print(value)
    for i in range(len(lower_role)):
        db2.lpush(str(lower_role[i]), value)


def sumbit_redis_list(leader_role,ret):
    """
    向redis提交报送文件，要上报的文件，。利用list
    :param leader_role:
    :param ret:
    :return:
    """


    path = ret.get('Remote file_id')
    file_name = ret.get('Local file name')

    file_name = file_name.split('\\')[-1]
    print(1111111111111111111,file_name)
    print(1111111111111111111, path)

    # k = str(l_user_id) + ":" + l_user_name
    value = path.decode()+","+file_name
    print(value)
    for i in range(len(leader_role)):
        db1.lpush(str(leader_role[i]),value)





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


def setWallPaper(pic_num):
    """
    照片地址，更换虚拟机地址，每一个号码，对应一个壁纸。暂未启用
    :param pic:
    :return:
    """
    #成功利用这段代码，就可以给虚拟机换皮，这里应该是根据，对方的角色来换皮的。
    # open register
    pic = " "
    if pic_num == 1:
        pic = 'C:\\programdata\\001.jpg'
    elif pic_num == 2:
        pic = 'C:\\programdata\\002.jpg'
    elif pic_num == 3:
        pic = 'C:\\programdata\\003.jpg'

    regKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(regKey, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    win32api.RegSetValueEx(regKey, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # refresh screen
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, pic, win32con.SPIF_SENDWININICHANGE)



def foo(hwnd, mouse):
    titles = set()
    # 判断是不是窗口、是不是可用的、是不是可见的
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        # 把得到的结果赋值给a
        a = win32gui.GetWindowText(hwnd)
        # 打出
        print(win32gui.GetWindowText(hwnd))
        # 不为空时
        if a != '':
            # 当'Program Manager'不在a内时：
            if 'Program Manager' not in a:
                if '开始' not in a:
                    if '管理员' not in a:
                        # 关闭窗口
                        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                        # 最小化窗口
                        # win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        # 把所有的窗口添加到titles集内
        titles.add(GetWindowText(hwnd))

        # lt = [t for t in titles if t]
        # lt.sort()
        # for t in lt:
        #     print(t)


    # 将软件窗口置于最前


# win32gui.SetForegroundWindow(hwnd)

if __name__ == '__main__':
   # a = (db1.get("test")).decode()
   # print(a)
    # print(db1.scan())
   db1.hset(name=1, key='23', value='path')
   a =  db1.hget(2,"23")
