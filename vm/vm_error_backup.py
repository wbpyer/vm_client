import redis
import win32gui
from vm.upload import upload_fdfs
from win32.lib import win32con
from win32gui import IsWindow,IsWindowEnabled,IsWindowVisible,GetWindowText


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