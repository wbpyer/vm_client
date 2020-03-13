import win32api, win32gui, win32con


def setWallPaper(pic):
    """
    照片地址
    :param pic:
    :return:
    """
    #成功利用这段代码，就可以给虚拟机换皮，这里应该是根据，对方的角色来换皮的。
    # open register
    regKey = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(regKey, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    win32api.RegSetValueEx(regKey, "TileWallpaper", 0, win32con.REG_SZ, "0")
    # refresh screen
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, pic, win32con.SPIF_SENDWININICHANGE)


setWallPaper('C:\\Users\\Admin\\Desktop\\Figure_1.png')



"""
3.13开发日志
虚拟机根据前端传回来的数据，自动切换页面功能，同时打开它的模板，这里我是这么想的，
要实现这个功能，前端必须穿参数给我，我接到参数后，然后切换相应的页面，到相应的模板上。
实现这个功能必要有，虚拟机的正确配置才行，理论上，我觉得应该是一个公司一个部门一个虚拟机
一个项目部一个部们一个虚拟机，
一个工区配置一台虚拟机，在上面干不同的活，按照这个原型去设计。

实现很好实现，这里还是要考虑很多逻辑，比如如果你采取动态虚拟机的话，这里考虑的是先下载文件，然后再去
改变壁纸，如果是静态虚拟机的话，直接改变壁纸就行了，
可以先做一个小demo,只在一台机器上实验
只需要一个参数，就是一个小编号。不同的编号映射不同的功能，给与不同的壁纸"""

