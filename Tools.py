# 共有的方法类
import configparser
import subprocess
import pandas as pd
import pyzipper
import os
import shutil
from pathlib import Path
import py7zr

class myTools(object):
    def __init__(self):
        pass
    # copy文件
    def copyFile(filePath,destination):
        shutil.copy2(filePath, destination)

    # 功能：用于清楚配置文件中存在的非法关系，比如< 和 > 等
    def clean_config_file(file_path):
        cleaned_lines = []

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # 替换所有的 < 和 > 为 = 号，或者直接删除这行
                # 你可以根据需要选择处理方式
                if '<' in line or '>' in line:
                    # 可以选择替换为 = 号，也可以选择忽略该行
                    cleaned_line = line.replace('<', '=').replace('>', '=')
                    cleaned_lines.append(cleaned_line)
                else:
                    cleaned_lines.append(line)
        # 2. 将清理后的内容写入临时文件
        temp_file_path = 'tmp/cleaned_config.ini'
        with open(temp_file_path, 'w', encoding='utf-8') as f:
            f.writelines(cleaned_lines)
        return temp_file_path
    # 根据路径获取配置文件的数据
    def get_Dict_info(path):
        dicts = {}
        temp_filePath = ''
        config = configparser.RawConfigParser(strict=False, interpolation=None)
        config.optionxform = str
        # 先判断有没有非法数据
        try:
            config.read(path, encoding='utf-8')
        except configparser.ParsingError as e:
            # 有非法数据
            # temp_filePath = clean_config_file(path)
            config.read(temp_filePath, encoding='utf-8')
        for section in config.sections():
            for key, value in config.items(section):
                dicts[key] = value
        if temp_filePath != '':  # 删除零时文件
            os.remove(temp_filePath)
        return dicts
    def modify_Dict_info(path,parametes):
        dicts = {}
        temp_filePath = ''
        config = configparser.RawConfigParser(strict=False, interpolation=None)
        config.optionxform = str
        # 先判断有没有非法数据
        try:
            config.read(path, encoding='utf-8')
        except configparser.ParsingError as e:
            # 有非法数据
            # config.read(temp_filePath, encoding='utf-8')
            print(path+'有非法数据——————————————————————————————————————————')

        for section in config.sections():
            for key, value in config.items(section):
                if key in list(parametes.keys()):
                    # print(path+'修改数据：', key,parametes[key])
                    config.set(section,key,parametes[key])
            # 保存修改后的 ini 文件
        with open(path, "w", encoding="utf-8") as configfile:
            for section in config.sections():
                configfile.write(f"[{section}]\n")
                for key, value in config[section].items():
                    configfile.write(f"{key}={value}\n")
                configfile.write("\n")

        # print('修改内容:',parametes)
        # new_lines = ''
        # parametes_keys = list(parametes.keys())
        # with open(path, 'r+') as f:
        #     contents = f.readlines()
        #
        #     for oneline in contents:
        #         flag = 0
        #         for onekey in parametes_keys:
        #             if onekey in oneline:
        #                 #修改
        #                 itms = oneline.split('=',maxsplit=1)
        #                 flag = 1
        #                 new_lines += itms[0]+'='+parametes[onekey]+'\n'
        #         if flag == 0:
        #             new_lines += oneline
        # with open(path, 'w') as file:
        #     file.writelines(new_lines)

    def copy_folder(src, dst):
        # 如果目标文件夹不存在，则创建
        if not os.path.exists(dst):
            os.makedirs(dst)

        if src.split('/')[-1] in os.listdir(dst):
            pass
        else:
            # 复制文件夹
            shutil.copytree(src, os.path.join(dst, os.path.basename(src)))

    def rename_folder(old_path, new_name):
        # 创建Path对象并调用rename()方法
        path = Path(old_path)
        new_path = path.with_name(new_name)
        path.rename(new_path)
    def creat_folder(path,name):
        # 要在其中创建文件夹的目录路径
        directory = path
        # 要创建的文件夹名称
        folder_name = name
        # 完整的文件夹路径
        full_path = os.path.join(directory, folder_name)
        # 如果文件夹不存在，则创建它
        if not os.path.exists(full_path):
            os.mkdir(full_path)
            # print(f"Folder '{folder_name}' created successfully.")
        else:
            print(f"Folder '{folder_name}' already exists.")
    def jieya(file_path,password):
        print(file_path)
        # 创建7z文件对象
        z = py7zr.SevenZipFile(file_path, mode='r', password=password)
        # 解压到当前目录
        z.extractall(path='.')
        # 关闭文件对象
        z.close()

    def unzip_7z(file_path, extract_path):
        with py7zr.SevenZipFile(file_path, mode='r') as z:
            z.extractall(path=extract_path)

    def copy_and_rename_folder(src_folder_path, dest_folder_path, new_folder_name):
        # 先复制整个文件夹
        shutil.copytree(src_folder_path, os.path.join(dest_folder_path, new_folder_name))
    def delete_directory_contents(directory):
        # 先判断是否存在
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    else:
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
        print('删除失败，因为'+directory+'不存在')

    def zip_folder_with_password(folder_path, zip_file_path, password):
        """
        压缩文件夹并添加密码。
        :param folder_path: 要压缩的文件夹路径
        :param zip_file_path: 生成的 zip 文件路径
        :param password: 压缩文件的密码
        """
        # 将密码转换为字节
        password_bytes = password.encode('utf-8')

        with pyzipper.AESZipFile(zip_file_path, 'w', compression=pyzipper.ZIP_DEFLATED,
                                 encryption=pyzipper.WZ_AES) as zipf:
            zipf.setpassword(password_bytes)
            zipf.setencryption(pyzipper.WZ_AES)

            # 遍历文件夹并添加到 zip 文件
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)

        print(f"压缩完成，文件保存为: {zip_file_path}")

        # # 示例用法
        # folder_to_zip = "./Temp_tools"  # 要压缩的文件夹
        # output_zip_file = "./Temp_tools.zip"  # 输出的压缩文件
        # zip_password = "1234"  # 设置的密码

    def authorize_MPMate(file_path):
        def run_command_with_file(exe_path, file_path):
            try:
                # 构建命令
                command = [exe_path, '-f', file_path]
                print(command)
                # 运行命令并捕获输出
                result = subprocess.run(
                    command,
                    capture_output=True,  # 捕获标准输出和错误
                    text=True,  # 将输出解码为字符串
                    check=True  # 如果命令失败会抛出异常
                )

                # 打印命令的输出
                # print("授权命令输出:")
                print(result.stdout)
                return result.stdout  # 返回标准输出内容5

            except subprocess.CalledProcessError as e:
                print(f"命令运行失败: {e}")
                print(f"错误输出: {e.stderr}")
                raise Exception("授权软件出错")
                return None

        MPMate_exe = ".\\4.1SATA-校验工具\MPMateCli-V1.exe"
        current_path = os.getcwd()
        print(f"当前路径是: {current_path}")
        file_path = file_path.replace("/", "\\")
        run_command_with_file(MPMate_exe, file_path)

    def clearData(paths):

        for onePath in paths:
            if onePath == './5需求文件':
                names = os.listdir('./5需求文件')
                for one in names:
                    if not one.__contains__('需求表格'):
                        print('./5需求文件' + '/' + one)
                        if os.path.exists('./5需求文件' + '/' + one):
                            os.remove('./5需求文件' + '/' + one)
            else:
                #  7新包文件夹是空的 不是空文件则删除下面的文件
                myTools.delete_directory_contents(onePath)

        return 1

    # 点击开始打包前，检查必要的文件是否存在
    def check_dirIsOK(paths,type):

        logs = ''
        # 检查文件是否存在
        for onePath in paths:
            if os.path.isfile(onePath):
                if not os.path.exists(onePath):
                    logs += 'error ' + onePath + '不存在，请检查\n'
            else:
                if len(os.listdir(onePath)) < 1:
                    logs += 'error ' + onePath + '是空文件夹，请检查\n'
        # 检查原始包是符合的

        # path_new = './1原始包/'+type
        # names = os.listdir(path_new) #PC OS
        # if len(names) > 0:
        #     for one in names:
        #         path_next = path_new + '/' + one
        #         for item in os.listdir(path_next):
        #             if item.lower()

        return logs

    # type = 'SATA'和'PCIE'
    def getInfoFromExcelbyone(type):
        indexs = []
        if type == 'SATA':
            indexs = [1, 3, 4, 5, 14, 15]
        else:
            indexs = [1, 3, 8, 4, 14, 15]
        print('获取信息')
        root_path = '.'
        path_need = root_path + '/5需求文件'
        name_excel = '生产软件包自动打包需求表格.xlsx'
        excel_file = pd.ExcelFile(path_need + '/' + name_excel)
        for sheet_name in excel_file.sheet_names:
            if sheet_name == type:
                df = pd.read_excel(excel_file, sheet_name=sheet_name, header=0,
                                   usecols=indexs)  # 从指定行开始读数据
                df_list = df.values.tolist()
                return df_list[1:]
    # 压缩
    def compress(path):
        names = os.listdir(path)
        print('带用过',path,names)
        if len(names) == 0:
            return 'error-打包失败,7新包下无软件包。'
        else:
            for one in os.listdir(path):
                print('one:',one)
                if os.path.isdir(path+'/'+one):
                    print('是文件夹')
                    with py7zr.SevenZipFile('./7新包/'+one + '.7z', mode='w', password='1234') as z:
                        z.writeall('./7新包/'+one,arcname=os.path.basename('./7新包/'+one))
            return 'pass-压缩完成。'

    def compress_folder_to_7z(folder_path, output_file, password):
        """
        将文件夹压缩为 7z 格式并添加密码。

        :param folder_path: 要压缩的文件夹路径
        :param output_file: 输出的 7z 文件路径
        :param password: 压缩密码
        """
        # 确保文件夹路径有效
        if not os.path.isdir(folder_path):
            raise ValueError(f"指定的路径不是有效文件夹: {folder_path}")

        # 使用 py7zr 压缩文件夹
        with py7zr.SevenZipFile(output_file, mode='w', password='1234') as archive:
            archive.writeall(folder_path, arcname=os.path.basename(folder_path))
        print(f"文件夹 {folder_path} 已压缩为 {output_file}，并添加了密码。")

    if __name__ == '__main__':
        path = './7新包'
        compress(path)
        # compress_folder_to_7z('./7新包/S30L S2 SN19907 960GB 1TB 20-45C AT OST 385B 20241230','./7新包/S30L S2 SN19907 960GB 1TB 20-45C AT OST 385B 20241230.7z',1234)
    #     # path = './7新
    #     包/S30L S2 SN19907 960GB 1TB AT OST 385B 20241230/PC/SLT-10%/cfg/SATA.ini'
    #     # authorize_MPMate(path)
    #     # # hello()