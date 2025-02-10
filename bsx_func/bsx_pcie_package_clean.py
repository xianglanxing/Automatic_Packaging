'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2025-01-02 10:46:42
LastEditors: bobo.bsx 2286362745@qq.com
LastEditTime: 2025-02-10 09:55:21
FilePath: \auto_package\clean.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import shutil

def delete_folder(folder_path):
    """
    删除指定文件夹及其内容。
    """
    if not os.path.exists(folder_path):
        print(f"文件夹 {folder_path} 不存在")
        return
    try:
        shutil.rmtree(folder_path)
        print(f"文件夹 {folder_path} 及其内容已成功删除")
    except Exception as e:
        print(f"删除文件夹时发生错误: {e}")

def delete_file(file_path):
    """
    删除指定文件。
    """
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在")
        return
    try:
        os.remove(file_path)
        print(f"文件 {file_path} 已成功删除")
    except Exception as e:
        print(f"删除文件时发生错误: {e}")

folders = ["./7新包", "./Temp_unzip"]

# 删除文件夹
for folder in folders:
    delete_folder(folder)

# 删除文件
log_file = "./autopkg_output.log"
delete_file(log_file)
