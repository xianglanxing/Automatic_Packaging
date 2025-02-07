'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2024-12-31 15:48:11
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2024-12-31 17:37:47
FilePath: \auto_package\package.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sys
import os


sys.path.append(os.path.abspath("./bsx_func"))

import Automatic_Packaging.bsx_func.os_func as f

def create_all_dir():
    folder_path = ["2PCIE-分站式SLT包", "3PCIE-一站式SLT包", "4SATA-SLT包", "5需求文件", "6检查记录", "7新包"]
    new_pkg_path = f"./{folder_path[5]}"
    src_pkg_path = "./1原始包"

    file_path = f"{src_pkg_path}/M1P MAS1102 SKV6 64G die Autorobot&normal 120-1024GB lowpower raid_D0_1_07g2_SN19907 mestor 20241220.7z"
    
    for i in folder_path:
        f.create_directory(i)

    f.extract_7z(file_path, new_pkg_path)

    # 2.创建包
    folder_name_tmp = ["产品", "颗粒等级", "FW版本", "非足容", "足容", "HT", "OST", "366B", "20241224"] # 例子
    PC_list = ["CBI", "K1-Burner", "K2-MT1", "K3-Update", "MT2", "SLT-10%", "SLT-100%"]
    OST_list = ["K1-Burner", "K2-MT1", "SLT-10%", "SLT-100%"]

    temp_name = " ".join(folder_name_tmp)
    temp_path = f"{new_pkg_path}/{temp_name}" 
    f.create_directory(temp_path) # 很长那个文件夹
    f.create_directory(f"{temp_path}/OST")
    f.create_directory(f"{temp_path}/PC")

    for i in PC_list:
        f.create_directory(f"{temp_path}/PC/{i}")

    for i in OST_list:
        f.create_directory(f"{temp_path}/OST/{i}")


if __name__ == "__main__":
    create_all_dir()

    





