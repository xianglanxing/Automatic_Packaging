'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2024-12-31 15:48:11
LastEditors: bobo.bsx 2286362745@qq.com
LastEditTime: 2025-02-07 15:56:51
FilePath: \auto_package\package.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sys
import os
import argparse

sys.path.append(os.path.abspath("./bsx_func"))

import os_func as f
import configparser
import logging

PC_K1_MPTOOL_dict = {}
PC_K2_MPTOOL_dict = {}
MT2_ini_dict = {}
MT2_cfg_dict = {}

en_check_para = 0

# 配置参数
CONFIG = {
    "src_pkg_path": "./1原始包/PCIE",
    "new_pkg_path": "./7新包",
    "temp_unzip_path": "./Temp_unzip",
    "checklist_path": "./6检查记录/checklist.xlsx",
    "password": "1234",
}

logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别
    format="%(asctime)s - %(levelname)s - %(message)s",  # 日志格式
    filename="./autopkg_output.log",  # 保存到文件
    filemode="a"  # 文件模式为追加（append）
)


print("开始打包")
# print(os.getcwd())
excel_path = f"./5需求文件/生产软件包自动打包需求表格.xlsx"
excel_data = f.parse_excel(excel_path)
# excel_data = 0

def create_all_dir():

    folder_path = ["6检查记录", "7新包"]
    for i in folder_path:
        f.create_directory(i)

    if(en_check_para):
        # 解析checklist参数
        f.force_copy("./bsx_func/checklist.xlsx", CONFIG['checklist_path'])
        checklist_data = f.parse_and_group_by_filename(CONFIG['checklist_path'])   
    else:
        checklist_data = None
    

    # 获取产品信息和包数量
    pcie_data = excel_data['PCIE']
    product_name = f.get_field_value(pcie_data[1], pcie_data[2], "产品")
    product_genX = classify_GenX(product_name)
    pkg_cnt = get_excel_len(pcie_data)

    # new_start
    for cur_pkg in range(2, 2+pkg_cnt):
        process_single_package(cur_pkg, pcie_data, product_genX, checklist_data)
    return 'pass-打包完成！'
    # compress_new_packages(CONFIG["new_pkg_path"], CONFIG["password"])
    # new_end

def parse_temp_range(string):
    """
    根据字符串解析出 min 和 max 的值
    :param string: 输入字符串，形式为 "min-max" 或 "value"
    :return: 一个字典，包含 min 和 max 的值
    """
    if "-" in string:
        # 形式为 "min-max"
        parts = string.split("-")
        min_val = int(parts[0])
        max_val = int(parts[1])
    else:
        # 形式为 "value"
        min_val = max_val = int(string)
    
    return min_val, max_val

def parse_config_string(config_str):
    """
    解析形如 'key1=value1;key2=value2' 的字符串为字典
    :param config_str: 输入的配置字符串
    :return: 解析后的字典
    """
    config_dict = {}
    
    for pair in config_str.split(";"):
        if "=" in pair:  # 确保有 `=`
            key, value = pair.split("=", 1)  # 只分割一次，避免值中含有 `=`
            config_dict[key.strip()] = value.strip()  # 去掉空格
    
    return config_dict



def set_custom_func(ini_file, pkg_index):
    # 解析数据
    pcie_data = excel_data['PCIE']
    is_custom = f.get_field_value(pcie_data[1], pcie_data[pkg_index], "是否开启客制化功能")
    temp_thermal = f.get_field_value(pcie_data[1], pcie_data[pkg_index], "锁温")
    is_L1_2 = f.get_field_value(pcie_data[1], pcie_data[pkg_index], "开启低功耗")
    logo = f.get_field_value(pcie_data[1], pcie_data[pkg_index], "品牌")

    # 解析K2其他参数
    other_para = f.get_field_value(pcie_data[1], pcie_data[pkg_index], "K2其他参数")
    other_para_list = parse_config_string(other_para)

    # 修改品牌
    logo_num = sw_logo(logo)
    f.modify_ini_file(ini_file, "FwSetting", "OUITypeIndex", logo_num)

    if(other_para != None):
        for key, value in other_para_list.items():
            f.modify_onlyone_ini_file(ini_file, key, value)

    # 开启低功耗
    if(is_L1_2 == True):
        f.modify_ini_file(ini_file, "FwSetting", "ASPM_Mode", "3")
        f.modify_ini_file(ini_file, "FwSetting", "EnASPM_L1_1", "1")
        f.modify_ini_file(ini_file, "FwSetting", "EnASPM_L1_2", "1")
        logging.info(f"修改{ini_file}开启低功耗模式")
    else:
        f.modify_ini_file(ini_file, "FwSetting", "ASPM_Mode", "0")
        f.modify_ini_file(ini_file, "FwSetting", "EnASPM_L1_1", "0")
        f.modify_ini_file(ini_file, "FwSetting", "EnASPM_L1_2", "0")
        logging.info(f"修改{ini_file}关闭低功耗模式")
    
    if(temp_thermal != None):
        temp_min, temp_max = parse_temp_range(str(temp_thermal))
        f.modify_ini_file(ini_file, "FwSetting", "EnSMARTThermalSetting", "1")
        f.modify_ini_file(ini_file, "FwSetting", "SMARTMinThermal", str(temp_min))
        f.modify_ini_file(ini_file, "FwSetting", "SMARTMaxThermal", str(temp_max))
    else:
        f.modify_ini_file(ini_file, "FwSetting", "EnSMARTThermalSetting", "0")
        f.modify_ini_file(ini_file, "FwSetting", "SMARTMinThermal", "0")
        f.modify_ini_file(ini_file, "FwSetting", "SMARTMaxThermal", "0")
      

def get_number_by_name(name):
    """
    根据名字返回对应的数字编号。
    
    :param name: 输入名字字符串
    :return: 对应的数字编号，如果名字不存在返回 None
    """
    name_to_number = {
        "common": 0,
        "TK1202": 1,
        "TK1602": 2,
        "TK2269": 3,
        "DM5216F": 4,
        "DM5220": 5,
        "RTS5766": 6,
        "DM1602": 7,
        "RTS5772": 8,
    }
    return name_to_number.get(name, None)


def update_teststep(file_path, update_string):
    """
    根据字符串更新 INI 文件的 [TestStep] 部分。
    
    :param file_path: INI 文件路径
    :param update_string: 包含更新信息的字符串，例如 "Step1=2\\nStep2=4"
    """
    # 创建 ConfigParser 对象
    config = configparser.ConfigParser()
    config.optionxform = str  # 保持大小写

    # 读取现有文件
    config.read(file_path)

    # 确保 [TestStep] 部分存在
    if 'TestStep' not in config:
        config['TestStep'] = {}
        logging.error("在配置文件中找不到TestStep元素")

    # 解析更新字符串
    for line in update_string.strip().split('\n'):
        key, value = line.split('=')
        config['TestStep'][key.strip()] = value.strip()

    # 写回文件
    with open(file_path, 'w') as file:
        config.write(file)

def sw_logo(logo_name):
    if(logo_name == "Lexar"):
        return "1"
    elif(logo_name == "Foresee"):
        return "0"
    elif(logo_name == "Other"):
        return "2"
    else:
        return "0"

def set_MT2(data, product, cfg_path, ini_path, data_index):
    # product选PCIE或sata
    deal_data = data[product]
    if deal_data[0][0] == "PCIE-T包信息":
        # target_value = get_field_value(PCIE_data[1], PCIE_data[2], "包名")
        # MT2_test_step = f.get_field_value(deal_data[1], deal_data[2], "MT2测试步骤")
        MT2_test_step = "Step1=9\nStep2=4\nStep3=0\nStep4=0\nStep5=0\nStep6=0\nStep7=0\nStep8=0"
        smart_QC_info3 = f.get_field_value(deal_data[1], deal_data[data_index], "SmartQCInfo3")
        vendor_smart_QC_Info4 = f.get_field_value(deal_data[1], deal_data[data_index], "VendorSmartQCInfo4")
        product_name = f.get_field_value(deal_data[1], deal_data[data_index], "产品")
        crtl_name = f.get_field_value(deal_data[1], deal_data[data_index], "主控")

    # 修改默认ini文件
    f.modify_ini_file(cfg_path, "Config", "FmtPath", "PCIE-MT2.ini")

    # 修改主控
    ctrl_type = get_number_by_name(crtl_name)
    f.modify_ini_file(cfg_path, "System", "CtrlType", str(ctrl_type))
    logging.info(f"修改{cfg_path}的CtrlType为{ctrl_type}")

    # 修改genX
    genX = classify_GenX(product_name)
    genX_str = str(int(genX)-1)
    f.modify_ini_file(ini_path, "QcCfg", "PcieSpec", genX_str)
    logging.info(f"修改{ini_path}的PcieSpec为{genX_str}")

    # 修改MP Board
    f.modify_ini_file(cfg_path, "UserOption", "MpBoard", "2")
    logging.info(f"修改{cfg_path}的MpBoard为USB_4Port")

    # 修改test_step
    update_teststep(cfg_path, MT2_test_step) 
    logging.info(f"修改{cfg_path}的TestStep为{MT2_test_step}")

    # 修改smart
    f.modify_ini_file(ini_path, "QcCfg", "SmartQCInfo3", smart_QC_info3)
    f.modify_ini_file(ini_path, "QcCfg", "VendorSmartQCInfo4", vendor_smart_QC_Info4)
    logging.info(f"修改{ini_path}的SmartQCInfo3为{smart_QC_info3}")
    logging.info(f"修改{ini_path}的VendorSmartQCInfo4为{vendor_smart_QC_Info4}")

def classify_GenX(product):
    if product.startswith("P1"):
        return "3"
    elif product.startswith("P2"):
        return "4"
    else:
        print("其他还没分类\r\n")
        return None


def set_SLT(data, product, cfg_path, ini_path, index, sw_port):
    deal_data = data[product]
    if deal_data[0][0] == "PCIE-T包信息":
        # target_value = get_field_value(PCIE_data[1], PCIE_data[index], "包名")
        product_name = f.get_field_value(deal_data[1], deal_data[index], "产品")
        ctrl_name = f.get_field_value(deal_data[1], deal_data[index], "主控")
        # SLT_test_step = f.get_field_value(deal_data[1], deal_data[index], "SLT测试步骤")
        SLT_test_step = "Step1=3\nStep2=1\nStep3=5\nStep4=2\nStep5=7\nStep6=9"
        stdby_elec = f.get_field_value(deal_data[1], deal_data[index], "待机电流")
        read_elec = f.get_field_value(deal_data[1], deal_data[index], "读电流")
        write_elec = f.get_field_value(deal_data[1], deal_data[index], "写电流")
        read_performance = f.get_field_value(deal_data[1], deal_data[index], "读性能")
        write_performance = f.get_field_value(deal_data[1], deal_data[index], "写性能")
        smart_QC_info = f.get_field_value(deal_data[1], deal_data[index], "SmartQCInfo")
        vendor_smart_QC_Info = f.get_field_value(deal_data[1], deal_data[index], "VendorSmartQCInfo")
        smart_QC_info3 = f.get_field_value(deal_data[1], deal_data[index], "SmartQCInfo3")
        vendor_smart_QC_Info4 = f.get_field_value(deal_data[1], deal_data[index], "VendorSmartQCInfo4")

        stdby_power = f.get_field_value(deal_data[1], deal_data[index], "待机功耗")
        read_power = f.get_field_value(deal_data[1], deal_data[index], "读功耗")
        write_power = f.get_field_value(deal_data[1], deal_data[index], "写功耗")

    # 修改ini
    f.modify_ini_file(cfg_path, "Config", "FmtPath", "PCIE-8port.ini")

    # 判断是genX产品
    genX = classify_GenX(product_name)
    genX_str = str(int(genX)-1)
    f.modify_ini_file(ini_path, "QcCfg", "PcieSpec", genX_str)
    logging.info(f"修改{ini_path}的PcieSpec为{genX_str}")

    # 修改主控
    ctrl_type = get_number_by_name(ctrl_name)
    f.modify_ini_file(cfg_path, "System", "CtrlType", str(ctrl_type))
    logging.info(f"修改{cfg_path}的CtrlType为{ctrl_type}")

    # 修改test_step
    update_teststep(cfg_path, SLT_test_step) 
    logging.info(f"修改{cfg_path}的TestStep为{SLT_test_step}")

    if(sw_port == "PCIE-4port"):
        # 修改电流
        f.modify_ini_file(ini_path, "SSDTEST", "StdbyCurrentMax", str(stdby_elec))
        f.modify_ini_file(ini_path, "SSDTEST", "ReadCurrentMax", str(read_elec))
        f.modify_ini_file(ini_path, "SSDTEST", "WriteCurrentMax", str(write_elec))
        logging.info(f"修改{ini_path}StdbyCurrentMax为{stdby_elec}")
        logging.info(f"修改{ini_path}的ReadCurrentMax为{read_elec}")
        logging.info(f"修改{ini_path}的WriteCurrentMax为{write_elec}")
    elif(sw_port == "PCIE-8port"):
        # 修改功耗
        f.modify_ini_file(ini_path, "SSDTEST", "StdbyCurrentMax", str(stdby_power))
        f.modify_ini_file(ini_path, "SSDTEST", "ReadCurrentMax", str(read_power))
        f.modify_ini_file(ini_path, "SSDTEST", "WriteCurrentMax", str(write_power))
        logging.info(f"修改{ini_path}StdbyCurrentMax为{stdby_power}")
        logging.info(f"修改{ini_path}的ReadCurrentMax为{read_power}")
        logging.info(f"修改{ini_path}的WriteCurrentMax为{write_power}")
    else:
        logging.error("无法识别为genX产品")

    # 修改性能
    f.modify_ini_file(ini_path, "SSDTEST", "MinSeqReadSpeed", str(read_performance))
    f.modify_ini_file(ini_path, "SSDTEST", "MinSeqWriteSpeed", str(write_performance))
    logging.info(f"修改{ini_path}的MinSeqReadSpeed为{SLT_test_step}")
    logging.info(f"修改{ini_path}的MinSeqWriteSpeed为{SLT_test_step}")

    # 修改smart 
    f.modify_ini_file(ini_path, "QcCfg", "SmartQCInfo", smart_QC_info)
    f.modify_ini_file(ini_path, "QcCfg", "VendorSmartQCInfo", vendor_smart_QC_Info)
    f.modify_ini_file(ini_path, "QcCfg", "SmartQCInfo3", smart_QC_info3)
    f.modify_ini_file(ini_path, "QcCfg", "VendorSmartQCInfo4", vendor_smart_QC_Info4)
    logging.info(f"修改{ini_path}的SmartQCInfo为{SLT_test_step}")
    logging.info(f"修改{ini_path}的VendorSmartQCInfo为{SLT_test_step}")
    logging.info(f"修改{ini_path}的SmartQCInfo3为{SLT_test_step}")
    logging.info(f"修改{ini_path}的VendorSmartQCInfo4为{SLT_test_step}")

    # 修改h2比例
    f.modify_ini_file(ini_path, "SSDTEST", "AllSpace", "0")
    logging.info(f"修改{ini_path}的AllSpace为0")

def get_excel_len(data):
    cnt = 0
    for i in data:
        if i[0] == None:
            continue
        else:
            cnt += 1
    return (cnt-2)

def create_OST(src_OST_path, dst_OST_path, data_index, product_gen): # wait..参考PC结构
    OST_list = ["K1-Burner", "K2-MT1", "SLT-100%", "SLT-10%"]
    folder_list = f.get_subfolder_names(src_OST_path)

    # 只单纯复制
    K1_target_name = f.find_strings_in_set(["K1", "RDT", "K1-Buner", "Buner"], folder_list)
    if K1_target_name:
        f.copy_folder_contents(f"{src_OST_path}/{K1_target_name[0]}", f"{dst_OST_path}/OST/{OST_list[0]}")
        logging.info("已完成OST的K1-Burner打包")

    # 复制+修改ini
    K2_target_name = f.find_strings_in_set(["K2", "MPT"], folder_list)
    if K2_target_name:
        f.copy_folder_contents(f"{src_OST_path}/{K2_target_name[0]}", f"{dst_OST_path}/OST/{OST_list[1]}")  
        # 修改ini
        ini_path = f.find_file_in_folder(f"{dst_OST_path}/OST/{OST_list[1]}", "MPTOOL.ini")
        if ini_path:
            cap_ssd = f.get_field_value(excel_data['PCIE'][1], excel_data['PCIE'][data_index], "容量")
            model_num = f"{cap_ssd} SSD"
            f.modify_ini_file(ini_path, "DeviceSetting", "ModelNum", model_num)# wait.. 
            logging.info(f"修改{ini_path}的ModelNum为:{model_num}")
            modify_K2_para(ini_path)
            set_custom_func(ini_path, data_index)
        else:
            return f"Error, OST-K2没有MPTOOL.ini"
            # raise Exception("没有MPTOOL.ini")

    # 复制+修改SLT
    en_SLT_100 = f.get_field_value(excel_data['PCIE'][1], excel_data['PCIE'][data_index], "SLT-100")
    if(en_SLT_100 == True):
        # SLT-100%
        f.copy_folder_contents(f"./3PCIE-一站式SLT包", f"{dst_OST_path}/OST/{OST_list[2]}")
        cfg_path = f"{dst_OST_path}/OST/{OST_list[2]}/cfg/SSDTest.cfg"
        ini_4port_path = f"{dst_OST_path}/OST/{OST_list[2]}/cfg/PCIE-4port.ini" # 到时候改一下这个文件名
        set_SLT(excel_data, "PCIE", cfg_path, ini_4port_path, data_index, "PCIE-4port")

        # OST专属修改
        f.modify_ini_file(cfg_path, "Config", "FmtPath", "PCIE-4port.ini")
        f.modify_ini_file(cfg_path, "UserOption", "MpBoard", "5")
        f.modify_ini_file(cfg_path, "UserOption", "UseKstRemapping", "1")
        f.authorize_MPMate(ini_4port_path)
        f.authorize_MPMate(cfg_path)      

    else:
        logging.info("没有SLT-100%的需求包")

    # SLT-10%，只用在SLT100上修改H2test的值
    en_SLT_10 = f.get_field_value(excel_data['PCIE'][1], excel_data['PCIE'][data_index], "SLT-10")
    if(en_SLT_10 == True):
        f.copy_folder_contents(f"{dst_OST_path}/OST/{OST_list[2]}", f"{dst_OST_path}/OST/{OST_list[3]}")
        f.modify_ini_file(f"{dst_OST_path}/OST/{OST_list[3]}/cfg/PCIE-4port.ini", # 改一下这个路径
                            "SSDTEST", "AllSpace", "2")
        f.authorize_MPMate(f"{dst_OST_path}/OST/{OST_list[3]}/cfg/PCIE-4port.ini")                 

    else:
        logging.info("没有SLT-10%的需求包")


  

def create_PC(src_PC_path, dst_PC_path, data_index, product_gen):
    PC_list = ["K1-Burner", "K2-MT1", "K3-Update", "MT2", "SLT-100%", "SLT-10%", "CBI"] # 按需创建吧

    folder_list = f.get_subfolder_names(src_PC_path)
    
    # K1，只单纯复制
    K1_target_name = f.find_strings_in_set(["RDT", "Buner", "K1"], folder_list)
    if K1_target_name:
        f.copy_folder_contents(f"{src_PC_path}/{K1_target_name[0]}", f"{dst_PC_path}/PC/{PC_list[0]}")
    else:
        print("*****************找不到K1-Burner***********************")
        logging.info("没有K1-Burner的需求包")


    # K2，复制+修改ini
    K2_target_name = f.find_strings_in_set(["MPT", "K2"], folder_list)
    if K2_target_name:
        f.copy_folder_contents(f"{src_PC_path}/{K2_target_name[0]}", f"{dst_PC_path}/PC/{PC_list[1]}")  
        # 修改ini
        ini_path = f.find_file_in_folder(f"{dst_PC_path}/PC/{PC_list[1]}", "MPTOOL.ini")
        if ini_path:
            cap_ssd = f.get_field_value(excel_data['PCIE'][1], excel_data['PCIE'][data_index], "容量")
            model_num = f"{cap_ssd} SSD"
            f.modify_ini_file(ini_path, "DeviceSetting", "ModelNum", model_num)# wait.. 
            logging.info(f"修改{ini_path}的ModelNum为:{model_num}")

            modify_K2_para(ini_path)
            set_custom_func(ini_path, data_index)
        
        else:

            return "Error, PC-K2没有MPTOOL.ini"
            # raise Exception("没有MPTOOL.ini")
    else:
        print("*****************找不到K2-MT1***********************")
        logging.info("没有K2-MT1的需求包")

    # K3
    K3_target_name = f.find_strings_in_set(["update", "Update"], folder_list)
    if K3_target_name:
        f.copy_folder_contents(f"{src_PC_path}/{K3_target_name[0]}", f"{dst_PC_path}/PC/{PC_list[2]}")  
        # 修改ini

    if "CBI" in folder_list:
        f.copy_folder_contents(f"{src_PC_path}/CBI", f"{dst_PC_path}/PC/{PC_list[6]}")  

    # 获取excel中slt数据
    en_SLT_100 = f.get_field_value(excel_data['PCIE'][1], excel_data['PCIE'][data_index], "SLT-100")
    if(en_SLT_100 == True):
        # SLT-100%
        # 8port修改
        f.copy_folder_contents(f"./2PCIE-分站式SLT包", f"{dst_PC_path}/PC/{PC_list[4]}")
        cfg_path = f"{dst_PC_path}/PC/{PC_list[4]}/cfg/SSDTest.cfg"
        ini_8port_path = f"{dst_PC_path}/PC/{PC_list[4]}/cfg/PCIE-8port.ini"
        set_SLT(excel_data, "PCIE", cfg_path, ini_8port_path, data_index, "PCIE-8port")
        f.authorize_MPMate(ini_8port_path)

        # 4port修改
        f.force_copy(f"{dst_PC_path}/PC/{PC_list[4]}/cfg/PCIE-8port.ini", f"{dst_PC_path}/PC/{PC_list[4]}/cfg/PCIE-4port.ini")
        ini_4port_path = f"{dst_PC_path}/PC/{PC_list[4]}/cfg/PCIE-4port.ini"    
        set_SLT(excel_data, "PCIE", cfg_path, ini_4port_path, data_index, "PCIE-4port")       
        f.authorize_MPMate(ini_4port_path)
        f.authorize_MPMate(cfg_path)

    else:
        logging.info("没有SLT-100%的需求包")
        return "Error, PC没有SLT-100%的需求包"
        # raise Exception("没有SLT-100%的需求包")

    # SLT-10%，只用在SLT10上修改H2test的值
    en_SLT_10 = f.get_field_value(excel_data['PCIE'][1], excel_data['PCIE'][data_index], "SLT-10")
    if(en_SLT_10 == True):
        f.copy_folder_contents(f"{dst_PC_path}/PC/{PC_list[4]}", f"{dst_PC_path}/PC/{PC_list[5]}")
        f.modify_ini_file(f"{dst_PC_path}/PC/{PC_list[5]}/cfg/PCIE-4port.ini", # 改一下这个路径
                            "SSDTEST", "AllSpace", "2")
        f.modify_ini_file(f"{dst_PC_path}/PC/{PC_list[5]}/cfg/PCIE-8port.ini", # 改一下这个路径
                            "SSDTEST", "AllSpace", "2")
        f.authorize_MPMate(f"{dst_PC_path}/PC/{PC_list[5]}/cfg/PCIE-4port.ini")                 
        f.authorize_MPMate(f"{dst_PC_path}/PC/{PC_list[5]}/cfg/PCIE-8port.ini")
              
    else:
        logging.info("没有SLT-10%的需求包")   


    if(product_gen == "4"):
        f.delete_file(f"{dst_PC_path}/PC/{PC_list[5]}/cfg/PCIE-4port.ini")
        f.delete_file(f"{dst_PC_path}/PC/{PC_list[4]}/cfg/PCIE-4port.ini")

# 暂时使用这种，后面由checklist接管
def modify_K2_para(ini_path):
    f.modify_ini_file(ini_path, "RDT", "DumpRAWFile", "1")
    f.modify_ini_file(ini_path, "RDSetting", "DumpDebugFile", "1")
    f.modify_ini_file(ini_path, "RDT", "EnECCInfo", "1")
    f.modify_ini_file(ini_path, "FwSetting", "EnD0D3Sleep", "1")
    f.modify_ini_file(ini_path, "FwSetting", "EnFWLEDSetting", "1")
    f.modify_ini_file(ini_path, "Setting", "BarCodeInputMode", "1")
    f.modify_ini_file(ini_path, "Setting", "EnPowerBridge", "1")
    f.modify_ini_file(ini_path, "Setting", "MPVersion", "1")

    


def check_by_excel(ini_path, check_list_data, target_dict):
    """
    通过 Excel 检查配置文件参数并记录检查结果

    :param ini_path: 配置文件路径 (ini 格式)
    :param check_list_data: checklist 数据，包含文件名、节、键、预设值等
    :param target_dict: 用于存储检查值的目标字典
    :return: 错误数，表示未通过检查的条目数量
    """
    # 参数有效性检查
    if not os.path.isfile(ini_path):
        raise FileNotFoundError(f"配置文件路径 {ini_path} 不存在！")
    
    if not isinstance(check_list_data, list) or not check_list_data:
        raise ValueError("check_list_data 应为非空列表！")
    
    if not isinstance(target_dict, dict):
        raise TypeError("target_dict 应为字典！")

    # 解析配置文件
    para = f.parse_ini_file(ini_path)

    error_count = 0  # 错误计数器

    for i in check_list_data:
        try:
            # 检查文件名是否匹配
            if i['文件名'] != check_list_data[0]["文件名"]:
                raise ValueError(f"文件名不匹配: {i['文件名']} 和 {check_list_data[0]['文件名']}")

            # 提取节和键
            section = i.get('节')
            key = i.get('键')
            dst_data = str(i.get('预设值', ''))  # 期望值
            if not section or not key:
                raise ValueError(f"条目 {i} 缺少 '节' 或 '键'！")

            # 检查 INI 文件中是否存在对应节和键
            if section not in para or key not in para[section]:
                raise KeyError(f"文件 {i['文件名']} 中的节 {section} 或键 {key} 不存在！")

            # 获取实际值
            src_data = para[section][key]
            i['检查值'] = src_data  # 回填检查值到原数据中
            target_dict[key] = src_data

            # 进行值检查
            if dst_data != "Skip":
                if(src_data != dst_data):
                    error_count += 1
                    logging.error(f"文件 {i['文件名']} 中 {section}_{key} 的期望值为 {dst_data}, 实际值为 {src_data}")
            else:
                continue

        except Exception as e:
            error_count += 1
            logging.error(f"检查条目 {i} 时发生错误: {e}")

    return error_count



def process_ost_and_pc_packages(src_pkg_folder_list, dst_pkg_path, cur_pkg, product_genX):
    """
    处理 OST 和 PC 包
    """
    has_ost = "OST" in src_pkg_folder_list
    has_pc = "PC" in src_pkg_folder_list

    if has_ost:
        create_OST(f"{CONFIG['src_pkg_path']}/OST", dst_pkg_path, cur_pkg, product_genX)
    else:
        logging.error("缺少 OST 包")

    if has_pc:
        create_PC(f"{CONFIG['src_pkg_path']}/PC", dst_pkg_path, cur_pkg, product_genX)
    else:
        logging.error("缺少 PC 包")

    if not has_ost and not has_pc:
        return f"Error, 包 {cur_pkg} 的 OST 和 PC 包均缺失"
        # raise Exception(f"包 {cur_pkg} 的 OST 和 PC 包均缺失")

def create_and_check_mt2_package(dst_pkg_path, cur_pkg, checklist_data):
    """
    创建并检查 MT2 包
    """
    mt2_path = f"{dst_pkg_path}/MT2"
    f.copy_folder_contents("./4PCIE-MT2包", mt2_path)
    
    mt2_cfg_path = f"{mt2_path}/cfg/SSDTest.cfg"
    mt2_ini_path = f"{mt2_path}/cfg/PCIE-MT2.ini"
    set_MT2(excel_data, "PCIE", mt2_cfg_path, mt2_ini_path, cur_pkg)

    f.authorize_MPMate(mt2_cfg_path)
    f.authorize_MPMate(mt2_ini_path)

    if en_check_para:
        # 检查MT2
        check_by_excel(mt2_ini_path, checklist_data["MT2_INI"], MT2_ini_dict)
        check_by_excel(mt2_cfg_path, checklist_data["MT2_CFG"], MT2_cfg_dict)
        # 检查K2
        check_by_excel(f"{dst_pkg_path}/PC/K2-MT1/MPTOOL.ini", checklist_data["PC_K2_MPTOOL"], PC_K2_MPTOOL_dict)
        # 检查K1
        check_by_excel(f"{dst_pkg_path}/PC/K1-Burner/MPTOOL.ini", checklist_data["PC_K1_MPTOOL"], PC_K1_MPTOOL_dict)

def compress_new_packages(new_pkg_path, password):
    """
    压缩新生成的包
    """
    newpkg_list = f.get_subfolder_names(new_pkg_path)
    for pkg in newpkg_list:
        f.compress_folder_to_7z(f"{new_pkg_path}/{pkg}", f"{new_pkg_path}/{pkg}.7z", password)

def process_single_package(cur_pkg, pcie_data, product_genX, checklist_data):
    """
    处理单个包的逻辑
    """
    dst_pkg_name = f.get_field_value(pcie_data[1], pcie_data[cur_pkg], "包名")
    dst_pkg_path = f"{CONFIG['new_pkg_path']}/{dst_pkg_name}"
    f.create_directory(dst_pkg_path)

    src_pkg_folder_list = f.get_subfolder_names(CONFIG["src_pkg_path"])
    # 处理OST和PC包
    process_ost_and_pc_packages(src_pkg_folder_list, dst_pkg_path, cur_pkg, product_genX)
    create_and_check_mt2_package(dst_pkg_path, cur_pkg, checklist_data)

    SOP_file = f.search_files_by_name("./5需求文件", "SOP")
    release_note = f.search_files_by_name("./5需求文件", "Release")
    if SOP_file:
        f.copy_file_to_folder(SOP_file[0], f"{dst_pkg_path}")
    if release_note:
        f.copy_file_to_folder(release_note[0], f"{dst_pkg_path}")


if __name__ == "__main__":
    create_all_dir()


