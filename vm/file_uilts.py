
import os
import zipfile


class File_utils():
    """
    工作区文件处理类。完成工作区文件遍历，打包。
    """
    # PATH = 'D:\\test'  #工作区常量，
    path_list = []
    @classmethod
    def get_all_file(cls,path,path_list= path_list):
        """
        遍历工作区API,拿到所有文件
        :param path:  虚拟机工作区路径
        :param path_list:  存放列表
        :return: 工作区所有文件列表
        """
        # path_list = []
        paths = os.listdir(path) # 列出指定路径下的所有目录和文件
        for i in paths:
            com_path = os.path.join(path,i)

            if os.path.isdir(com_path):
                File_utils.get_all_file(com_path) # 如果该路径是目录，则调用自身方法
            elif os.path.isfile(com_path):
                path_list.append(com_path)# 如果该路径是文件，则追加到path_list中
        return path_list

                # print(com_path) #打印所有文件的绝对路径
            # print(com_path) # 打印所有文件和目录的绝对路径


    @classmethod
    def mk_package(cls,start_dir:str ):
        """
        文件夹打包
        :param start_dir:元路径
        :return: 目标文件名,绝对路径
        """
        start_dir = start_dir  # 要压缩的文件夹路径
        file_news = start_dir + '.zip'  # 压缩后文件夹的名字

        z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
        for dir_path, dir_names, file_names in os.walk(start_dir):

            f_path = dir_path.replace(start_dir, '') # 这一句很重要，不replace的话，就从根目录开始复制
            f_path = f_path and f_path + os.sep or ''  # 实现当前文件夹以及包含的所有文件的压缩
            for dir_name in dir_names:
                z.write(os.path.join(dir_path, dir_name), f_path + dir_name)

            for filename in file_names:

                z.write(os.path.join(dir_path, filename), f_path + filename)


        z.close()
        return file_news



    @classmethod
    def unzip(cls,path = 'C:\\Users\\worker\\Desktop\\我的办公桌\\'):
    # def unzip(cls, path='C:\\Users\\Admin\\Desktop\\我的办公桌\\'):
        """
        zip解包裹
        :param path: 工作去路径
        :return:
        """
        file_list = os.listdir(path)

        for file_name in file_list:
            # print(file_name)
            if os.path.splitext(file_name)[-2] == '我的办公桌':
                print(file_name)

                file_zip = zipfile.ZipFile(path + file_name, 'r')
                for file in file_zip.namelist():
                    file_zip.extract(file, path)
                file_zip.close()
                os.remove(path + file_name)



    @classmethod
    # def unzip_file(cls,path = 'C:\\Users\\worker\\Desktop\\我的办公桌.zip\\'):
    def unzip_file(cls, path):
        '''解压zip包'''
        if os.path.exists(path):
            if path.endswith('.zip'):
                z = zipfile.ZipFile(path, 'r')
                # unzip_path = os.path.split(path)[0]
                unzip_path = os.path.split(path)[0] + "\\" + os.path.split(path)[1].split('.')[0]
                print(unzip_path)
                z.extractall(path=unzip_path)
                zip_list = z.namelist()  # 返回解压后的所有文件夹和文件
                for zip_file in zip_list:
                    try:
                        zip_file2 = zip_file.encode('cp437').decode('gbk')
                    except:
                        zip_file2 = zip_file.encode('utf-8').decode('utf-8')
                    old_path = os.path.join(unzip_path, zip_file)
                    new_path = os.path.join(unzip_path, zip_file2)
                    if os.path.exists(old_path):
                        os.renames(old_path, new_path)
                        cls.unzip_file(new_path)
                z.close()
                os.remove(os.path.split(path)[0] + "\\" + os.path.split(path)[1])
            elif os.path.isdir(path):
                for file_name in os.listdir(path):
                    cls.unzip_file(os.path.join(path, file_name))
        else:
            print('the path is not exist!!!')


if __name__ == '__main__':
    # File_utils.unzip()
    File_utils.mk_package('C:\\Users\\Admin\\Desktop\\我的办公桌')
    print("ok")



