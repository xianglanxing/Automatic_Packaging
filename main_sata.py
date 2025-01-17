import pandas as pd

from Tools import myTools
import py7zr
import os
# 方法： 修改指定路径下  K1 K2 K3包名字

def reNames(path):
    dirsPC = os.listdir(path)
    for one in dirsPC:
        if one.lower().__contains__('mpt') or one.lower().__contains__('k2'):
            myTools.rename_folder(path + '/' + one, 'K2-MT1')
        elif one.lower().__contains__('buner') or one.lower().__contains__('k1') or 'rdt' in one.lower():
            myTools.rename_folder(path + '/' + one, 'K1-Buner')
        elif one.lower().__contains__('up'):
            myTools.rename_folder(path + '/' + one, 'K3-Update')
        else:
            print('检查PC文件目录，发现文件夹名为' + one)
# 方法： 根据parametes 来决定是否创建M.2 mSata HS文件夹，并将K1 K2 K3文件复制过来
def createDir(path_new,path_ori,type,parametes):  # type 是PC 和 OST

    to_path = path_new + '/'+type
    myTools.creat_folder(path_new, type)
    if parametes['M.2'] == 1:
        # 创建M.2文件夹
        myTools.copy_folder(path_ori, to_path)  # 拷贝文件pc_path = path_new + '/PC'
        myTools.rename_folder(to_path + '/' + type, 'M.2')
        reNames(to_path + '/M.2')
    if parametes['mSata'] == 1:
        # 创建mSata文件夹
        myTools.copy_folder(path_ori, to_path)  # 拷贝文件pc_path = path_new + '/PC'
        myTools.rename_folder(to_path + '/' + type, 'mSata')
        reNames(to_path + '/mSata')
    if parametes['HS'] == 1:
        # 创建mSata文件夹
        myTools.copy_folder(path_ori, to_path)  # 拷贝文件pc_path = path_new + '/PC'
        myTools.rename_folder(to_path + '/' + type, 'HS')
        reNames(to_path + '/HS')
# 方法1：创建K1 K2 (K3) 和 MT2 SLT-10%  SLT-100%路径 并copy原始文件
def createNewProject(fileName,root_path,parametes):
    # 创建新包路径
    myTools.creat_folder(root_path+'/'+'7新包',fileName)
    path_new = root_path+'/'+'7新包'+'/'+fileName
    # 判断原始包
    path_original = root_path +'/'+'1原始包/SATA'
    path_pc = path_original + '/PC'
    path_ost = path_original + '/OST'

    # 把K1 K2包复制到新包路径下 并修改包名
    dirs_pc = os.listdir(path_pc)
    dirs_ost = os.listdir(path_ost)
    if len(dirs_pc) > 0:
        createDir(path_new, path_pc, 'PC', parametes)
        path_amptool = root_path + '/' + '4SATA-分站SLT包'
        amptool_name = os.listdir(path_amptool)[0]
        if parametes['SLT-10%'] == 1:
            myTools.copy_and_rename_folder(path_amptool + '/' + amptool_name, path_new+'/PC', 'SLT-10%')
        if parametes['SLT-100%'] == 1:
            myTools.copy_and_rename_folder(path_amptool + '/' + amptool_name, path_new+'/PC', 'SLT-100%')
        # 复制MT2包
        myTools.copy_and_rename_folder(path_amptool + '/' + amptool_name, path_new+'/PC', 'MT2')

    if len(dirs_ost) > 0:
        #K1 K2 K3
        createDir(path_new, path_ost, 'OST', parametes)
        #MT2 SLT
        path_amptool = root_path + '/' + '4SATA-一站式SLT包'
        amptool_name = os.listdir(path_amptool)[0]
        myTools.copy_and_rename_folder(path_amptool + '/' + amptool_name, path_new+'/OST', 'SLT-10%')
        myTools.copy_and_rename_folder(path_amptool + '/' + amptool_name, path_new+'/OST', 'SLT-100%')
# 方法2：PC和OST路径下的K1 K2 K3 进行赋值，以及对SLT MT2包进行赋值操作
# parametes_modify 先赋值外形ConnectorType的值，再增加其他需要修改参数
def assignment_main(fileName,root_path,newName,parametes_K1_2,params_MT2,params_SLT): #one_type 是'MT2','SLT-10%','SLT-100%'
    SATA_TYPES = {'HS':'0','M.2':'1','mSata':'2'}
    path_newPro = root_path+'/'+newName+'/'+fileName
    for one in os.listdir(path_newPro): # OST PC 等
        # K1 K2 包，配置文件修改参数
        for function_type in os.listdir(path_newPro + '/' + one):  # M.2 HS mSata
            parametes_modify = {}  # 存放需要修改的参数
            if function_type in ['MT2', 'SLT-10%', 'SLT-100%']:
                path_cfg = path_newPro + '/' + one + '/' + function_type + '/cfg/AMPTool.cfg'
                path_ini = path_newPro + '/' + one + '/' + function_type + '/cfg/' + 'SATA.ini'
                if function_type == 'MT2':
                    parametes_modify = params_MT2
                if function_type == 'SLT-10%':
                    parametes_modify.update(params_SLT)
                    params_SLT.update({'AllSpace': '0'})
                if function_type == 'SLT-100%':
                    parametes_modify.update(params_SLT)
                    params_SLT.update({'AllSpace': '2'})
                myTools.modify_Dict_info(path_cfg, parametes_modify)
                myTools.modify_Dict_info(path_ini, parametes_modify)

            else:
                path_final = path_newPro + '/' + one + '/' + function_type
                fileNames = os.listdir(path_final)
                for oneFile in fileNames:  # K1 K2 K3
                    parametes_modify = {}
                    # K1 只修改外形，K2 除了修改外形，还有其他的修改信息。
                    if oneFile.lower().__contains__('k1') or oneFile.lower().__contains__('k2'):
                        path_ini = path_final + '/' + oneFile + '/MPTOOL.ini'
                        parametes_modify['ConnectorType'] = SATA_TYPES[function_type] # K1值修改外形
                        if oneFile.lower().__contains__('k2'):
                            parametes_modify.update(parametes_K1_2)  # 字典合并

                        myTools.modify_Dict_info(path_ini, parametes_modify)

# 方法2：PC和OST路径下的K1 K2 K3 进行赋值，以及对SLT MT2包进行赋值操作
# parametes_modify 先赋值外形ConnectorType的值，再增加其他需要修改参数


def getInfoFromExcel(path,name,type):

    all_datas = []
    # indexs = ['编号', '软件包名', '产品', '容量', 'FW版本', '是否支持L1.2', 'M.2', 'HS', 'mSata', 'SLT-10%', 'SLT-100%', '读电流', '写电流', '待机电流', '读性能', '写性能', 'SmartQCInfo', 'VendorSmartQCInfo', 'SmartQCInfo3', 'VendorSmartQCInfo4', '锁温', 'smart设置']
    excel_file = pd.ExcelFile(path+'/'+name)
    for sheet_name in excel_file.sheet_names:
        if sheet_name == type:
            df = pd.read_excel(excel_file, sheet_name=sheet_name,header=0)  # 从指定行开始读数据
            df.fillna('空白', inplace=True)
            datas = df.values.tolist()

            for i in range(len(datas)):
                if i==0:
                    indexs = datas[i]
                else:
                    params_basic = dict(zip(indexs[0:6], datas[i][0:6]))
                    params_creat = dict(zip(indexs[6:11], datas[i][6:11]))
                    params_MT2 = dict(zip(indexs[-4:-2], datas[i][-4:-2]))
                    params_SLT = dict(zip(indexs[11:-2], datas[i][11:-2]))
                    params_customize = dict(zip(indexs[-2:], datas[i][-2:]))
                    all_datas.append([params_basic,params_creat,params_MT2,params_SLT,params_customize])
            return all_datas
def getPath(path,type):
    files = os.listdir(path)
    if type == 'release_not':
        for one in files:
            if one.__contains__('pdf'):
                return one
    elif type == 'SOP':
        for one in files:
            if one.__contains__('SOP') or one.__contains__('流程') or one.__contains__('生产测试'):
                return one
    return ''

def getCustomizeParams(params_customize):
    params_all = {}

    temper_value = params_customize['锁温']
    if temper_value != '空白':
        if str(temper_value).__contains__('-'):  # 温度范围区间
            min_temper = temper_value.split('-')[0]
            max_temper = temper_value.split('-')[1]
        else:
            min_temper = max_temper = temper_value
            params_all['CusCurThermal'] = temper_value
        params_all['CusMinThermal'] = min_temper
        params_all['CusMaxThermal'] = max_temper

        params_all['ThermalSensorType'] = 0
    otherParem = params_customize['K2其他参数']
    if otherParem != '空白':
        value_items = otherParem.split(',')
        for one_item in value_items:
            key = one_item.split('=')[0]
            value = one_item.split('=')[1]
            params_all[key] = value
    return params_all

def clearData():
    #  7新包文件夹是空的 不是空文件则删除下面的文件
    myTools.delete_directory_contents('./1原始包/SATA')
    myTools.delete_directory_contents('./1原始包/PCIE')
    myTools.delete_directory_contents('./7新包')
    myTools.delete_directory_contents('./6检查表格')
    names = os.listdir('./5需求文件')
    for one in names:
        if not one.__contains__('需求表格'):

            if os.path.exists('./5需求文件'+'/'+one):
                os.remove('./5需求文件'+'/'+one)
    return 1

def verification_amptool(path):
    for one in os.listdir(path):
        if one == 'OST' or one == 'PC':
            path_next = path + '/'+one
            for itm in os.listdir(path_next):
                if itm.lower().__contains__('slt') or itm.lower().__contains__('mt2'):
                    path_ini = path_next + '/' + itm + '/cfg/'+'SATA.ini'
                    path_cfg = path_next + '/' + itm + '/cfg/'+'AMPTOOL.cfg'
                    myTools.authorize_MPMate(path_ini)
                    myTools.authorize_MPMate(path_cfg)
# 点击开始打包前，检查必要的文件是否存在
def check_dirIsOK():
    paths = ['./1原始包/SATA','./3校验工具','./4SATA-分站SLT包','./4SATA-一站式SLT包','./5需求文件/生产软件包自动打包需求表格.xlsx']

    logs = ''
    for onePath in paths:
        if os.path.isfile(onePath):
            if not os.path.exists(onePath):
                logs += 'error '+onePath + '不存在，请检查\n'
        else:
            if len(os.listdir(onePath)) < 1:
                logs += 'error '+onePath + '是空文件夹，请检查\n'
    return logs
# sata 打包主函数
def sata_package():
# if __name__ == '__main__':
    check_dir_logs = check_dirIsOK()
    if check_dir_logs == '':

        root_path = '.'
        path_need = root_path+'/5需求文件'
        name_excel = '生产软件包自动打包需求表格.xlsx'
        # 1、获取需求表格里面的内容
        all_params = getInfoFromExcel(path_need,name_excel,'SATA')
        # 2、确保 7新包文件夹是空的 不是空文件则删除下面的文件
        myTools.delete_directory_contents(root_path+'/7新包')
        # 3、根据需求表格中的信息来 依次 打包软件包
        if len(all_params) > 0:
            for oneParam in all_params: # 开始打包
                # 提取K1 K2包的Param
                params_basic =oneParam[0]
                parametes_creat = oneParam[1]
                parametes_MT2 = oneParam[2]
                parametes_SLT = oneParam[3]
                params_customize = oneParam[4]

                parametes_K1_2 = {'ModelNum': params_basic['容量'] + ' SSD'}
                parametes_MT2.update({'Step1':'6','Step2':'4','Step3':'0','Step4':'0','Step5':'0','Step6':'0'})
                parametes_SLT.update({'Step1':'1','Step2':'2','Step3':'3','Step4':'1','Step5':'6','Step6':'4'})

                # 低功耗信息
                if int(params_basic['是否支持L1.2']) == 1:
                    parametes_K1_2.update({'EnableHIPM':'1','EnableDIPM':'1','EnDeviceSleep':'1'})
                elif int(params_basic['是否支持L1.2']) == 0:
                    parametes_K1_2.update({'EnableHIPM':'0','EnableDIPM':'0','EnDeviceSleep':'0'})

                # 客制化参数设置
                parametes_K1_2_Customize = getCustomizeParams(params_customize)
                if len(parametes_K1_2_Customize) != 0:
                    parametes_K1_2.update(parametes_K1_2_Customize)

                fileName = params_basic['软件包名']
                # 创建PC OST HS M.2 mSata K1 K2 SLT 和MT2文件 并复制
                print('开始创建'+fileName+'--------------------------------------------------------')
                createNewProject(fileName, root_path, parametes_creat)

                print('创建成功')
                print('****开始给'+fileName+'的K1 K2 SLT和MT2 赋值')
                assignment_main(fileName, root_path, '7新包', parametes_K1_2, parametes_MT2, parametes_SLT)

                # 复制sop流程文档和release note文档
                print('复制SOP和release note')
                release_note_name = getPath(path_need, 'release_not')

                sop_name = getPath(path_need, 'SOP')
                print(len(release_note_name))
                if len(release_note_name) > 0 and len(sop_name) > 0:
                    myTools.copyFile(path_need + '/' + release_note_name, root_path + '/7新包/' + fileName)
                    myTools.copyFile(path_need + '/' + sop_name, root_path + '/7新包/' + fileName)
                else:
                    if len(release_note_name) == 0:
                        return 'error-release Note 文档缺失'
                    if len(sop_name) == 0:
                        return 'error-SOP流程 文档缺失'
                # 对配置文件进行校验
                print('对配置文件进行校验')
                verification_amptool(root_path+'/7新包/'+fileName)

            # # return 'PASS,打包完成'
            #     # 压缩 整个文件
            #     print('开始压缩文件--------')
            #     # 创建压缩文件
            #     with py7zr.SevenZipFile(fileName+'.7z', mode='w',password='1234') as z:
            #         z.writeall(root_path+'/7新包/'+fileName)
                return 'PASS,打包完成'
                # break
        else:
            print('SATA需求表是空白的，请检查！！')
    else:
        print('check_dir_logs:',check_dir_logs)
        return check_dir_logs
# if __name__=='__main__':
    pass
    # root_path = '.'
    # path_need = root_path+'/5需求文件'
    # name_excel = '生产软件包自动打包需求表格.xlsx'
    # # 1、获取需求表格里面的内容
    # all_params = getInfoFromExcel(path_need,name_excel,'SATA')
    # # 2、确保 7新包文件夹是空的 不是空文件则删除下面的文件
    # myTools.delete_directory_contents(root_path+'/7新包')
    # # 3、根据需求表格中的信息来 依次 打包软件包
    # if len(all_params) > 0:
    #     for oneParam in all_params: # 开始打包
    #         # 提取K1 K2包的Param
    #         params_basic =oneParam[0]
    #         print('params_basic:',params_basic)
    #         parametes_creat = oneParam[1]
    #         parametes_MT2 = oneParam[2]
    #         parametes_SLT = oneParam[3]
    #         params_customize = oneParam[4]
    #
    #         parametes_K1_2 = {'ModelNum': params_basic['容量'] + ' SSD'}
    #         parametes_MT2.update({'Step1':'6','Step2':'4','Step3':'0','Step4':'0','Step5':'0','Step6':'0'})
    #         parametes_SLT.update({'Step1':'1','Step2':'2','Step3':'3','Step4':'1','Step5':'6','Step6':'4'})
    #
    #         # 低功耗信息
    #         print('params_basic',params_basic['是否支持L1.2'])
    #         if int(params_basic['是否支持L1.2']) == 1:
    #             parametes_K1_2.update({'EnableHIPM':'1','EnableDIPM':'1','EnDeviceSleep':'1'})
    #         elif int(params_basic['是否支持L1.2']) == 0:
    #             parametes_K1_2.update({'EnableHIPM':'0','EnableDIPM':'0','EnDeviceSleep':'0'})
    #
    #         # 客制化参数设置
    #         parametes_K1_2_Customize = getCustomizeParams(params_customize)
    #         if len(parametes_K1_2_Customize) != 0:
    #             parametes_K1_2.update(parametes_K1_2_Customize)
    #
    #         fileName = params_basic['软件包名']
    #         # 创建PC OST HS M.2 mSata K1 K2 SLT 和MT2文件 并复制
    #         print('开始创建'+fileName+'--------------------------------------------------------')
    #         createNewProject(fileName, root_path, parametes_creat)
    #
    #         print('创建成功')
    #         print('****开始给'+fileName+'的K1 K2 SLT和MT2 赋值')
    #         assignment_main(fileName, root_path, '7新包', parametes_K1_2, parametes_MT2, parametes_SLT)
    #
    #         # 复制sop流程文档和release note文档
    #         release_note_name = getPath(path_need, 'release_not')
    #         sop_name = getPath(path_need, 'SOP')
    #         if len(release_note_name) > 0 and len(sop_name) > 0:
    #             myTools.copyFile(path_need + '/' + release_note_name, root_path + '/7新包/' + fileName)
    #             myTools.copyFile(path_need + '/' + sop_name, root_path + '/7新包/' + fileName)
    #         else:
    #             if release_note_name == None:
    #                 print('release Note 文档缺失')
    #             if sop_name == None:
    #                 print('SOP流程 文档缺失')
    #         # # 压缩 整个文件
    #         # print('开始压缩文件--------')
    #         # # 创建压缩文件
    #         # with py7zr.SevenZipFile(fileName+'.7z', mode='w',password='1234') as z:
    #         #     z.writeall(root_path+'/7新包/'+fileName)
    #         # break
    # else:
    #     print('SATA需求表是空白的，请检查！！')
    # #
    # # # parametes = {"ModelNum": "256GB SSD",'interface_type_M.2':'1','interface_type_mSata':'1','interface_type_HS':'1','SLT-10%':'1','SLT-100%':'1'}
    # # # parametes_K1_2 = {'ModelNum':'256GB SSD'}
    # # # parametes_MT2 = {'Step1':'6','Step2':'4','Step3':'0','Step4':'6','Step5':'4','Step6':'0',
    # # #                  'SmartQCInfo':'01<1;05<1;A0<1;B0<1;B1<6;C7<1','SmartQCInfo2':'01<2'}
    # # # parametes_SLT = {'Step1':'1','Step2':'2','Step3':'3','Step4':'1','Step5':'6','Step6':'4',
    # # #                  'SmartQCInfos':'01<1','SmartQCInfo2s':'01<1',
    # # #                  'SmartQCInfo':'01<1;05<1;A0<1;B0<1;B1<6;C7<1','SmartQCInfo2':'01<2',
    # # #                  'MinSeqReadSpeed':'500','MinSeqWriteSpeed':'470',
    # # #                  'ReadCurrentMax':'280','WriteCurrentMa':'310','StdbyCurrentMax':'170'}
