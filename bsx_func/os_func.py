'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2024-12-31 15:54:24
LastEditors: bobo.bsx 2286362745@qq.com
LastEditTime: 2025-02-08 10:59:43
FilePath: \auto_package\bsx_func\os_func.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import py7zr
import shutil
import configparser
import openpyxl
import pyzipper
import subprocess
import time
from pathlib import Path

from collections import defaultdict

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
    with py7zr.SevenZipFile(output_file, mode='w', password=password) as archive:
        archive.writeall(folder_path, arcname=os.path.basename(folder_path))
    print(f"文件夹 {folder_path} 已压缩为 {output_file}，并添加了密码。")


def zip_folder_with_password(folder_path, zip_file_path, password):
    """
    压缩文件夹并添加密码。
    
    :param folder_path: 要压缩的文件夹路径
    :param zip_file_path: 生成的 zip 文件路径
    :param password: 压缩文件的密码
    """
    # 将密码转换为字节
    password_bytes = password.encode('utf-8')
    
    with pyzipper.AESZipFile(zip_file_path, 'w', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zipf:
        zipf.setpassword(password_bytes)
        zipf.setencryption(pyzipper.WZ_AES)
        
        # 遍历文件夹并添加到 zip 文件
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

    print(f"压缩完成，文件保存为: {zip_file_path}")


def get_field_value(header, data, target_field):
    """
    根据字段名称从标题和数据中获取对应的值。

    :param header: 元组或列表，表示标题行
    :param data: 元组或列表，表示数据行
    :param target_field: 字符串，目标字段名称
    :return: 字段对应的值（如果字段存在），否则返回 None
    """
    if target_field in header:
        field_index = header.index(target_field)  # 找到字段对应的索引
        return data[field_index]  # 返回对应的值
    else:
        return None


def parse_excel(file_path):
    """
    解析 Excel 数据

    :param file_path: Excel 文件路径
    :param output_file: 输出文件路径
    """
    # 打开工作簿
    workbook = openpyxl.load_workbook(file_path)
    data = {}  # 用于存储所有工作表的数据

    # 遍历所有工作表
    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
        sheet_data = []

        # 遍历每一行并存储数据
        for row in sheet.iter_rows(values_only=True):
            sheet_data.append(row)
        
        data[sheet_name] = sheet_data
    
    return data

def modify_onlyone_ini_file(file_path, two_para, dst_str):
    """
    修改 ini 文件内容，仅根据配置项（Key）查找并更新值，忽略节名（Section）。
    
    :param file_path: ini 文件路径
    :param two_para: 配置项（Key）
    :param dst_str: 配置值（Value）
    """
    config = configparser.RawConfigParser()
    config.optionxform = str  # 保留选项（键）的大小写

    # 读取 ini 文件
    config.read(file_path, encoding="utf-8")

    key_found = False  # 记录是否找到并修改 Key

    # 遍历所有 Section，查找 `two_para`
    for section in config.sections():
        if two_para in config[section]:
            config[section][two_para] = dst_str
            key_found = True

    # 如果 `two_para` 在任何 Section 中都不存在，则添加到 DEFAULT
    if not key_found:
        if "DEFAULT" not in config:
            config["DEFAULT"] = {}
        config["DEFAULT"][two_para] = dst_str

    # 保存修改后的 ini 文件
    with open(file_path, "w", encoding="utf-8") as configfile:
        config.write(configfile)


def modify_ini_file_old(file_path, one_para, two_para, dst_str):
    """
    修改 ini 文件内容，添加或更新配置，同时保留大小写。
    Tips: 会增加空格
    :param file_path: ini 文件路径
    :param one_para: 节名（Section）
    :param two_para: 配置项（Key）
    :param dst_str: 配置值（Value）
    """
    # 使用 RawConfigParser 禁用大小写转换
    config = configparser.RawConfigParser()
    config.optionxform = str  # 保留选项（键）的大小写

    # 读取 ini 文件
    config.read(file_path, encoding="utf-8")

    # 修改现有值
    if one_para in config:
        config[one_para][two_para] = dst_str
    else:
        config[one_para] = {two_para: dst_str}

    # 保存修改后的 ini 文件
    with open(file_path, "w", encoding="utf-8") as configfile:
        config.write(configfile)


def copy_and_remove_folder(source_folder, target_folder):
    """
    先将 source_folder 复制到 target_folder，然后删除 source_folder。

    :param source_folder: 源文件夹路径（如 "C:/PC/K1"）
    :param target_folder: 目标文件夹路径（如 "C:/PC/DCDC/K1"）
    """
    # 确保源文件夹存在
    if not os.path.exists(source_folder):
        print(f"❌ 源文件夹不存在: {source_folder}")
        return

    # 确保目标父目录存在
    os.makedirs(os.path.dirname(target_folder), exist_ok=True)

    # 复制文件夹
    try:
        shutil.copytree(source_folder, target_folder)
        print(f"✅ 复制完成: {source_folder} -> {target_folder}")
    except FileExistsError:
        print(f"⚠️ 目标文件夹已存在: {target_folder}，跳过复制")
    
    # 删除源文件夹
    try:
        shutil.rmtree(source_folder)
        print(f"🗑️ 已删除原文件夹: {source_folder}")
    except PermissionError as e:
        print(f"❌ 删除失败，文件可能被占用: {e}")


def modify_ini_file(file_path, one_para, two_para, dst_str):
    """
    修改 ini 文件内容，添加或更新配置，同时保留大小写。
    Tips: 会删除空格
    :param file_path: ini 文件路径
    :param one_para: 节名（Section）
    :param two_para: 配置项（Key）
    :param dst_str: 配置值（Value）
    """
    # 使用 RawConfigParser 禁用大小写转换
    config = configparser.RawConfigParser()
    config.optionxform = str  # 保留选项（键）的大小写

    # 读取 ini 文件
    config.read(file_path, encoding="utf-8")

    # 修改现有值
    if one_para in config:
        config[one_para][two_para] = dst_str
    else:
        config[one_para] = {two_para: dst_str}

    # 保存修改后的 ini 文件
    with open(file_path, "w", encoding="utf-8") as configfile:
        for section in config.sections():
            configfile.write(f"[{section}]\n")
            for key, value in config[section].items():
                configfile.write(f"{key}={value}\n")
            configfile.write("\n")


def parse_ini_file(file_path):
    """
    解析指定的 ini 文件并返回其内容。
    
    :param file_path: ini 文件路径
    :return: 一个包含所有 sections 和键值对的字典
    """

    # 使用 RawConfigParser 禁用大小写转换
    config = configparser.RawConfigParser()
    config.optionxform = str  # 保留选项（键）的大小写
    config.read(file_path, encoding="utf-8")

    config_dict = {}
    for section in config.sections():
        config_dict[section] = dict(config.items(section))
    
    return config_dict


def find_file_in_folder(folder_path, file_name):
    """
    在指定文件夹中查找是否存在指定文件名。

    :param folder_path: 要搜索的文件夹路径
    :param file_name: 要查找的文件名
    :return: 如果找到返回文件的完整路径，否则返回 None
    """
    # 遍历文件夹中的文件
    for root, _, files in os.walk(folder_path):
        if file_name in files:
            return os.path.join(root, file_name)
    return None


def get_subfolder_names(folder_path):
    try:
        # 列出文件夹下的所有内容
        all_items = os.listdir(folder_path)
        # 过滤出子文件夹名称
        subfolders = [item for item in all_items if os.path.isdir(os.path.join(folder_path, item))]
        return subfolders
    except Exception as e:
        print(f"Error: {e}")
        return []

def find_strings_in_set(strings, target_set):
    """
    判断字符串列表中哪些字符串存在于集合中，并返回对应的字符串列表。

    :param strings: 字符串列表
    :param target_set: 目标集合
    :return: 存在于集合中的字符串列表
    """
    return [s for s in strings if s in target_set]


def copy_folder_contents(source_folder, target_folder):
    """
    将源文件夹内的所有内容复制到目标文件夹中。
    如果目标文件夹中存在相同的文件或子文件夹，则覆盖。

    :param source_folder: 源文件夹路径
    :param target_folder: 目标文件夹路径
    """
    if not os.path.exists(source_folder):
        raise ValueError(f"源文件夹不存在: {source_folder}")
    
    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)

    # 遍历源文件夹的内容
    for item in os.listdir(source_folder):
        if item == 'Sorting_Log':   # 不处理这个长路径
            continue
        source_item = os.path.join(source_folder, item)
        target_item = os.path.join(target_folder, item)

        if os.path.isdir(source_item):  # 如果是子文件夹
            if os.path.exists(target_item):
                shutil.rmtree(target_item)  # 删除已存在的目标文件夹
            shutil.copytree(source_item, target_item)  # 复制整个文件夹
        else:  # 如果是文件
            shutil.copy2(source_item, target_item)  # 复制文件（覆盖）

        # print(f"已复制: {source_item} -> {target_item}")

def search_files_by_name(directory, search_string):
    # 保存匹配文件的路径
    matching_files = []

    # 遍历指定目录
    for root, _, files in os.walk(directory):
        for file in files:
            # 检查文件名是否包含目标字符串
            if search_string in file:
                matching_files.append(os.path.join(root, file))

    return matching_files

def copy_file_to_folder(source_file, target_folder):
    # 确保目标文件夹存在，不存在则创建
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 获取源文件名并构造目标路径
    file_name = os.path.basename(source_file)
    target_path = os.path.join(target_folder, file_name)

    # 拷贝文件
    shutil.copy2(source_file, target_path)
    print(f"文件已成功拷贝到: {target_path}")

def copy_files(source_folder, target_folder):
    """
    将指定文件夹内的所有文件复制到另一个文件夹中，若已存在则强制覆盖。

    :param source_folder: 源文件夹路径
    :param target_folder: 目标文件夹路径
    """
    if not os.path.exists(source_folder):
        raise ValueError(f"源文件夹不存在: {source_folder}")
    
    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)

    for root, _, files in os.walk(source_folder):
        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_folder, file)
            
            # 复制文件，强制覆盖
            shutil.copy2(source_file, target_file)
            print(f"已复制文件: {source_file} -> {target_file}")



def copy_folder(source_folder, destination_folder):
    """
    拷贝整个文件夹及其所有内容。
    
    :param source_folder: 源文件夹路径
    :param destination_folder: 目标文件夹路径
    """
    if not os.path.exists(source_folder):
        print(f"源文件夹不存在: {source_folder}")
        return

    try:
        shutil.copytree(source_folder, destination_folder)
        print(f"文件夹拷贝完成，从 {source_folder} 到 {destination_folder}")
    except FileExistsError:
        print(f"目标文件夹已存在: {destination_folder}")
    except Exception as e:
        print(f"拷贝文件夹失败: {e}")

def extract_7z(file_path, output_folder):
    """
    解压 .7z 文件到指定目录

    :param file_path: 要解压的 .7z 文件路径
    :param output_folder: 解压到的目标文件夹
    """
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在。")
        return

    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    try:
        with py7zr.SevenZipFile(file_path, mode='r') as archive:
            archive.extractall(path=output_folder)
            print(f"文件已成功解压到 {output_folder}")
    except Exception as e:
        print(f"解压文件时出错: {e}")

def force_copy(src, dst):
    """
    强制复制文件，无论目标文件是否存在。
    :param src: 源文件路径
    :param dst: 目标文件路径
    """
    try:
        # 创建目标目录（如果不存在）
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        
        # 强制复制文件
        shutil.copy2(src, dst)  # 使用 copy2 保留文件元数据
        print(f"文件已成功复制到 {dst}")
    except FileNotFoundError:
        print(f"源文件 {src} 不存在，请检查路径！")
    except Exception as e:
        print(f"复制文件时发生错误：{e}")


def create_directory(path):
    """
    创建文件夹，如果文件夹已存在则不重复创建。

    :param path: 文件夹路径（绝对路径或相对路径）
    :return: 一个字典，包含文件夹路径及状态
             {"status": "created" or "exists", "path": "folder_path"}
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            return {"status": "created", "path": path}
        else:
            return {"status": "exists", "path": path}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def remove_empty_folders(path):
    """
    检查路径下的所有文件夹，如果文件夹为空则删除。
    
    :param path: 要检查的根目录路径
    """
    for root, dirs, files in os.walk(path, topdown=False):  # 从子目录向上遍历
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # 检查文件夹是否为空
                try:
                    os.rmdir(dir_path)  # 删除空文件夹
                    print(f"已删除空文件夹: {dir_path}")
                except Exception as e:
                    print(f"删除文件夹 {dir_path} 时出错: {e}")

def parse_and_group_by_filename(file_path):
    """
    解析 Excel 表格数据，并按文件名分组。
    
    :param file_path: Excel 文件路径
    :return: 按文件名分组的字典
    """
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # 获取标题行
    headers = [cell.value for cell in sheet[1]]  # 第一行标题

    # 初始化分组结果
    grouped_data = defaultdict(list)

    # 遍历数据行
    for row in sheet.iter_rows(min_row=2, values_only=True):  # 从第二行开始
        row_data = dict(zip(headers, row))  # 将行数据与表头映射成字典

        # 根据文件名分组
        filename = row_data.get("文件名")  # 获取 "文件名" 列的值
        if filename:  # 确保文件名不为空
            grouped_data[filename].append(row_data)

    return grouped_data


def delete_file(file_path):
    """
    删除指定路径的文件。

    :param file_path: 文件路径（绝对路径或相对路径）
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)  # 删除文件
            print(f"文件 {file_path} 已成功删除。")
        else:
            print(f"文件 {file_path} 不存在，无需删除。")
    except Exception as e:
        print(f"删除文件 {file_path} 时发生错误: {e}")



def authorize_MPMate(file_path):
    def run_command_with_file(exe_path, file_path):
        try:
            # 构建命令
            command = [exe_path, '-f', file_path]
            
            # 运行命令并捕获输出
            result = subprocess.run(
                command, 
                capture_output=True,  # 捕获标准输出和错误
                text=True,            # 将输出解码为字符串
                check=True            # 如果命令失败会抛出异常
            )
            
            # 打印命令的输出
            # print("授权命令输出:")
            print(result.stdout)
            return result.stdout  # 返回标准输出内容

        except subprocess.CalledProcessError as e:
            print(f"命令运行失败: {e}")
            print(f"错误输出: {e.stderr}")
            raise Exception("授权软件出错")
            return None

    current_path = os.getcwd()
    # print(f"当前路径是: {current_path}")

    MPMate_exe = ".\\3校验工具\MPMateCli-V1.exe"
    file_path = file_path.replace("/", "\\")
    run_command_with_file(MPMate_exe, file_path)
