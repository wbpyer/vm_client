import win32api,win32con,win32gui

"""测试虚拟机自动换壁纸"""
print(u'正在设置图片:%s为桌面壁纸...')
key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
    "Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
#2拉伸适应桌面,0桌面居中
win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, "./test.bmp", 1+2)
print(u'成功应用图片:%s为桌面壁纸')












