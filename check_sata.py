# 联芸方案-SATA-2.3架构 check
import configparser
import os
import re

def check_datas():
    pass
# manufacturer：厂家
'''
功能：1、获取参数表格参数在各个工具的ini和cfg配置文件中的真实值 2、对比期望和真实值的差异
输入1：tool_type，chcke表格第一列，工具名称
输入2：config_type，check表格第二列，配置文件是ini还是cfg
输入3：stage_type,check表格第三列，表示是哪个环节使用。比如K1、K2、PC&MT2、PC&SLT-10%、PC&SLT-100%、OST&SLT-10%、OST&SLT-100%
输入4：check_lists_dicts，check表格中的数据，写成字典的形式，key是前4列通过_拼接的字符串，value是参数期待值
输入5：data_dicts，是配置文件中所有的key-value
输出：输出格式是list,是参数表格中填上真实值和对比结果
'''
def Chcek_AMPTOOL(tool_type,config_type, stage_type,check_lists_dicts,data_dicts):
    print('tool_type:',tool_type)
    print('config_type:',config_type)
    print('stage_type:',stage_type)
    print('check_lists_dicts:',check_lists_dicts)
    print('data_dicts:',data_dicts)
    # 1、从check_lists_dicts 中提取指定文件的参数
    new_check_lists_dicts = {}
    for one_line in check_lists_dicts.keys():
        if stage_type.__contains__('&'):
            if one_line.__contains__(tool_type) and one_line.__contains__(config_type) and one_line.__contains__(
                    stage_type.split('&')[0]) and one_line.__contains__(stage_type.split('&')[1]):

                new_check_lists_dicts[one_line] = check_lists_dicts[one_line]
        else:
            if one_line.__contains__(tool_type) and one_line.__contains__(config_type) and one_line.__contains__(stage_type):
                new_check_lists_dicts[one_line] = check_lists_dicts[one_line]
    print('new_check_lists_dicts',new_check_lists_dicts)
    final_rs = []
    # 2、获取参数值，并进行对比
    all_data_keys = data_dicts.keys() # 从ini里面读取的数据
    for check_key in new_check_lists_dicts.keys():  # 检查表格数据  check_key = AMPOOL-cfg-OST&PC-CtrlType
        oneLine = check_key.split('_') # oneLine = [AMPOOL,cfg,OST&PC,CtrlType]
        new_key = oneLine[3] # new_key = CtrlType
        if new_key in all_data_keys:
            # 获取期望值和真实值
            Expect_rs = new_check_lists_dicts[check_key]
            actual_rs = data_dicts[new_key]
            print('new_key:', new_key, 'actual_rs:', actual_rs)
            # 转换值的格式  # %%%%%%%%%%%%%%%%有坑，理想情况是除了samrt值之外，其他值都是ini和float格式数据
            if bool(re.fullmatch(r'[\d.]+', actual_rs)) and bool(str(Expect_rs).isdigit()):
                if actual_rs.__contains__('.'):
                    actual_rs = int(actual_rs.split('.')[0])
                else:
                    actual_rs = int(actual_rs)
                Expect_rs = int(Expect_rs)
            else:
                pass

            # 对比
            if str(Expect_rs) == str(actual_rs):
                comparison_rs = '一致'
            else:
                comparison_rs = '不一致'
            final_rs.append([tool_type, config_type, stage_type,new_key, Expect_rs, actual_rs, comparison_rs])
        else:
            print(check_key+'参数不存在，请检查！！')
    return final_rs
# 从配置文件中读取数据
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
#从表格中读取数据
def get_check_dicts(path,sheetName):
    excel_file = pd.ExcelFile(path)
    check_dicts = {}
    for sheet_name in excel_file.sheet_names:
        if sheet_name == sheetName:
            df = pd.read_excel(excel_file, sheet_name=sheet_name, header=1).iloc[:, :5]  # 从指定行开始读数据
            for oneLine in df.values.tolist():
                key = oneLine[0] + '_' + oneLine[1] + '_' + oneLine[2] + '_' + oneLine[3]
                value = oneLine[4]
                check_dicts[key] = value
    return check_dicts

# ini_path = './test_xxl/SLT-S30W-128GB.ini'
# dict_ini = get_Dict_info(ini_path)
# print('chck_dicts',chck_dicts)
# print('dict_ini',dict_ini)
# print(Chcek_AMPTOOL('AMPTOOL','ini', 'SLT',chck_dicts,dict_ini))
#Chcek_AMPTOOL(tool_type,config_type, stage_type,check_lists_dicts,data_dicts):
def check_data_main(path):
    # 获取检查表格数据
    path_check = './6检查记录/checklist_SATA.xlsx'
    chck_dicts = get_check_dicts(path_check, 'SATA基本数据')

    all_lists = []
    for oneName in os.listdir(path):  #包名
        one_lists = [['tool_type','config_type','stage_type','参数','期望值','实际值','对比结果']]
        if os.path.isdir(path + '/' + oneName): #如果是文件夹 就开始检查
            new_path = path + '/' +oneName
            print('new_path:',new_path)
            for production_type in os.listdir(new_path):  # PC OST
                new_path_next = new_path + '/' + production_type
                print('new_path_next:',new_path_next)
                if os.path.isdir(new_path_next):  # 判断是否是文件夹
                    rs_lists = []
                    for shape in os.listdir(new_path_next): #外形 HS M.2 masta MT2 SLT

                        if shape.lower().__contains__('mt2') or shape.lower().__contains__('slt'):
                            tool_type = 'AMPTOOL'
                            config_type = 'ini'
                            stage_type = production_type + '&' + shape

                            cfg_path = new_path_next + '/' + shape + '/cfg/AMPTool.cfg'
                            ini_path = new_path_next + '/' + shape + '/cfg/SATA.ini'

                            dicts_ini = get_Dict_info(ini_path)

                            dicts_cfg = get_Dict_info(cfg_path)

                            rs_list_ini = Chcek_AMPTOOL(tool_type, config_type, stage_type, chck_dicts, dicts_ini)
                            rs_list_cfg = Chcek_AMPTOOL(tool_type, config_type, stage_type, chck_dicts, dicts_cfg)

                            rs_lists = rs_list_ini + rs_list_cfg
                            print('____________shape:',shape)
                            print('rs_lists:',rs_lists)
                            one_lists += rs_lists
                        else:
                            new_path_shap = new_path_next + '/' + shape

                            for oneType in os.listdir(new_path_shap):  # K1 K2
                                print('_____________oneType:',oneType)
                                if oneType.lower().__contains__('k1') or oneType.lower().__contains__('k2'):
                                    tool_type = 'MPTOOL'
                                    config_type = 'ini'
                                    if oneType.lower().__contains__('k1'):
                                        stage_type ='K1'
                                    elif oneType.lower().__contains__('k2'):
                                        stage_type = 'K2'
                                    mptool_ini_path = new_path_next + '/' + oneType + '/MPTOOL.ini'
                                    # Ini配置文件原始数据
                                    data_dicts = get_Dict_info(mptool_ini_path)
                                    rs_lists = Chcek_AMPTOOL(tool_type,config_type, stage_type,chck_dicts,data_dicts)
                                    print('rs_lists:',rs_lists)
                                    one_lists += rs_lists

        print('one_lists:',one_lists)

        all_lists.append(one_lists)
import pandas as pd
file_path = './7新包'
check_data_main(file_path)





