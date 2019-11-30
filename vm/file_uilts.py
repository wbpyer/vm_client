
import os
import zipfile


class File_utils():
    """
    工作区文件处理类。完成工作区文件遍历，打包。
    """
    PATH = 'D:\\test'  #工作区常量，
    path_list = []
    @classmethod
    def get_all_file(cls,path= PATH,path_list= path_list):
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
    def mk_package(cls,start_dir:str = PATH):
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
    def unzip(cls,path = 'D:\\test\\'):
        """

        :param path: 工作去路径
        :return:
        """
        file_list = os.listdir(path)

        for file_name in file_list:
            # print(file_name)
            if os.path.splitext(file_name)[-2] == 'test':
                print(file_name)

                file_zip = zipfile.ZipFile(path + file_name, 'r')
                for file in file_zip.namelist():
                    file_zip.extract(file, path)
                file_zip.close()
                os.remove(path + file_name)




if __name__ == '__main__':
    File_utils.mk_package("D:\\test")