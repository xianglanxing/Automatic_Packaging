import os_func as f
import logging

CONFIG = {
    "src_pkg_path": r".\1原始包\PCIE",
    "new_pkg_path": r".\7新包",
    "temp_unzip_path": r".\Temp_unzip",
    "checklist_path": r".\6检查记录\checklist.xlsx",
    "password": "1234",
}

class DataManager:
    def __init__(self):
        self.data = None  # 存储数据

    def save_data(self, value):
        self.data = value  # 保存数据

    def use_data(self):
        if self.data is not None:
            print(f"使用的数据: {self.data}")
        else:
            print("没有保存数据")

PC_K1_MPTOOL_dict = {}
PC_K2_MPTOOL_dict = {}
MT2_ini_dict = {}
MT2_cfg_dict = {}

K1_target_list = ["K1", "RDT", "K1-Buner", "Buner", "BNR"]
K2_target_list = ["K2", "MPT", "MT1"]

en_check_para = 0

excel_path = r".\5需求文件\生产软件包自动打包需求表格.xlsx"
excel_data = f.parse_excel(excel_path)

logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别
    format="%(asctime)s - %(levelname)s - %(message)s",  # 日志格式
    filename=r".\autopkg_output.log",  # 保存到文件
    filemode="a"  # 文件模式为追加（append）
)