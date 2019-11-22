

"""测试文件，没有用"""

# from fdfs_client.client import *
# # # #fdfs 潘森测试,目前删除好使，上传好使，下载
# # #
# trackers = get_tracker_conf(r'C:\Users\Admin\Desktop\client.conf')
# client = Fdfs_client(trackers)
# # ret = client.upload_by_filename(r'C:\Users\Admin\Desktop\珠海发桥123')
# d = b'group1/M00/00/00/wKgdgV23bOyAXEQGAAAFqB-VPWM96.conf'  #传入这个就可以。
# # print(client.get_meta_data(d))
# # print(client.list_all_groups())
#
# # d.find(b'/')
#
# # ret = client.append_by_filename('C:\\Users\\Admin\\Desktop\\new1.txt',d)  #这个方法不行。运转不起来。
# # ret = client.delete_file(d) 这个ok
#
# ret = client.download_to_file('C:\\Users\\Admin\\Desktop\\123',d)  #下载功能已经实现
# print(ret)



import re
# d2 = 'C:\\Users\\Admin\\Desktop\\是的撒范德萨珠海发桥'
# d1='C:\\Users\\Admin\\Desktop\\是的撒范德萨342ABDGS878****珠海发桥123'
# d = 'D:\\test\\人\\日\\报\\新建文本文档.txt'
# d.split('\\')
# d = d.split('\\')
# print(d)




# c = '[\u4e00-\u9fa5]'
# b = re.compile('[\u4e00-\u9fa51-9a-zA-Z]*')
# # r = re.compile('[\u4e00-\u9fa51-9a-zA-Z]*\.')
# obj = re.findall(b,d1)
# print(obj)
# s = ''.join(obj) #注意：引号内有空格
# print(s)

#
# files = File_utils.get_all_file()
# for file in files:
#     if len(file.split('\\')) > 4 and file.split('\\')[-2] in ['草', '报', '副', '垃']:
#         # 如果符合条件就开始上传。不符合条件，就不管。
#         try:
#
#             if upload(file) == 'ok':
#                 return "通知运维真关机"
#         except Exception as e:
#             print(e)
#             self.upload(file)



import zipfile
import os

# file_list = os.listdir(r'D:/test')
#
# for file_name in file_list:
#     # print(file_name)
#     print(os.path.splitext(file_name)[-2])
            # print (file_name)



            # file_zip = zipfile.ZipFile(r'D:/test/' + file_name, 'r')
            # for file in file_zip.namelist():
            #     file_zip.extract(file, r'D:/test')
            # file_zip.close()
            # os.remove(r'D:/test/' + file_name)


# fz = zipfile.ZipFile(zip_src, 'r')
#         for file in fz.namelist():
#             fz.extract(file, dst_dir)
#

