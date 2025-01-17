import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import scrolledtext
import tkinter.ttk as ttk
from main_sata import clearData,sata_package
import sys
# cur_path = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.abspath(cur_path))
import bsx_pcie_package as pcie
from Tools import myTools

from tkinter import *
# 功能：一键清除1原始文件 5需求文件 7新包
def confirm_selection():
    print('当前路径：', os.path.dirname(os.path.abspath(__file__)))
    paths = ['./1原始包/SATA', './1原始包/PCIE', './5需求文件', './7新包', './6检查表格']
    rs = myTools.clearData(paths)
    if rs == 1:
        messagebox._show("PASS", "已经清除上次打包的数据，请开始重新打包！")
    else:
        messagebox.showerror('FAIL','清除数据失败，请检查！！')

# # 功能：将数据展示到界面上
def confirm_selection2():
    # 获取type值
    interface_type = variable0.get()
    print('选择的接口类型为:',type)
    # 插入数据

    # if interface_type == 'SATA':
    #     datas = getInfoFromExcelbyone(type=interface_type)
    # elif interface_type == 'PCIE':
    #     datas = getInfoFromExcelbyone(type=interface_type)
    # else:
    #     messagebox.showerror('error', '请选择接口类型')
    if interface_type != '':
        datas = myTools.getInfoFromExcelbyone(type=interface_type)
    else:
        messagebox.showerror('error', '请选择接口类型')
    for i in range(15):
        if i < len(datas):
            print(datas[i])
            table.insert('', 'end', text='1', values=tuple(datas[i]))
        else:
            table.insert('', 'end', text='1', values=('','','','',''))
# # 特殊功能检查模块
def confirm_selection3():
    paths = ['./3校验工具', './4SATA-分站SLT包', './4SATA-一站式SLT包', './5需求文件/生产软件包自动打包需求表格.xlsx']
    # 获取type值
    interface_type = variable0.get()
    print('选择的接口类型为:', type)
    # 删除./7新包下的文件
    myTools.delete_directory_contents('./7新包')
    if interface_type == 'SATA':
        paths.append('./1原始包/SATA')
        check_dir_logs = myTools.check_dirIsOK(paths,type)  # 检查必要的文件是否缺失
        if check_dir_logs == '':
            rs = sata_package()
        else:
            messagebox.showerror('error', check_dir_logs)
    elif interface_type == 'PCIE':

        paths.append('./1原始包/PCIE')
        check_dir_logs = myTools.check_dirIsOK(paths,type)
        if check_dir_logs == '':
            rs = pcie.create_all_dir()
        else:
            messagebox.showerror('error', check_dir_logs)
    else:
        messagebox.showerror('error','请选择接口类型')
    if rs.lower().__contains__('pass'):
        messagebox._show("PASS", rs)
    elif rs.lower().__contains__('error'):
        messagebox.showerror('error', rs)
def confirm_selection4():
    result = messagebox.askokcancel("提示", "你确定需要压缩 7新包下的文件夹！")
    if result:
        # 压缩
        path = './7新包'
        rs = myTools.compress(path)
        if rs.__contains__('error'):
            messagebox.showerror('error',rs.split('-')[1])
        else:
            messagebox._show('pass',rs.split('-')[1])
    else:
        print("User clicked Cancel")
def check_datas():
    interface_type = variable0.get()
    # 删除./7新包下的文件
    myTools.delete_directory_contents('./7新包')
    if interface_type == 'SATA':
        pass
# 创建主窗口
root = tk.Tk()
root.title("软件包检查")

# 设置窗口大小
root.geometry("1400x800")

# 创建变量用于保存选择的路径
folder1_var = tk.StringVar()
folder2_var = tk.StringVar()
file_var = tk.StringVar()
variable0 = tk.StringVar(root)
variable1 = tk.StringVar(root)
# ---------------------------上模块-----------------------------------


frame_top = tk.LabelFrame(root, text="基本信息确认", padx=10, pady=10)
frame_top.pack(pady=10, fill=tk.X, padx=10)

folder_frame = tk.Frame(frame_top)
tk.Button(folder_frame, text="一健清除信息", command=confirm_selection).pack(side=tk.LEFT,padx=10)
folder_frame.pack(pady=5, fill=tk.X)
tk.Label(folder_frame, text="接口类型").pack(side=tk.LEFT, padx=5)
tk.OptionMenu(folder_frame, variable0, *["PCIE", "SATA"]).pack(side=tk.LEFT, padx=10)

tk.Label(folder_frame, text="打包类型").pack(side=tk.LEFT, padx=5)
tk.OptionMenu(folder_frame, variable1, *["客制化包", "量产包"]).pack(side=tk.LEFT, padx=10)

# -----------------————中模块————————————————————————————————————————
frame_middle = tk.LabelFrame(root, text="自动打包信息获取", padx=10, pady=10)
frame_middle.pack(pady=1, fill=tk.X, padx=10)


# 第二行：一个文件选择框
row2 = tk.Frame(frame_middle)
names=('包名','容量','版本','是否支持L1.2','读性能','写性能')
# 创建一个Treeview对象
table = ttk.Treeview(frame_middle, columns=names,height=15)

# 设置列的标题
table.heading('#0', text='1',anchor='center')
names=('包名','容量','版本','是否支持L1.2','读性能','写性能')
for onename in names:
    table.heading(onename, text=onename, anchor='center')
# 插入列
table.column('#0', width=1,anchor='center')
for onename in names:
    if onename == '包名':
        table.column(onename, width=400,anchor='center')
    else:
        table.column(onename, width=200,anchor='center')
# 放置表格
table.pack(fill='both', expand=True)

# 第四行，确定按钮
row5 = tk.Frame(frame_middle)
row5.pack(pady=1, fill=tk.X)
tk.Button(row5, text="获取信息", command=confirm_selection2).pack(padx=300,side=tk.LEFT)
tk.Button(row5, text="开始打包", command=confirm_selection3).pack(padx=1,side=tk.LEFT)
tk.Button(row5, text="一键压缩", command=confirm_selection4).pack(padx=260,side=tk.LEFT)
# -------------------------下模块---------------------------------------
frame_3= tk.LabelFrame(root, text="基本信息检查", padx=10, pady=10)
frame_3.pack(pady=2, fill=tk.X, padx=10)

# 第四行，确定按钮
row3 = tk.Frame(frame_3)
row3.pack(pady=1, fill=tk.X)

prompt_pass_2 = scrolledtext.ScrolledText(row3, height=10, width=65, bd=0, relief="raised", highlightbackground="red",bg='honeydew')
prompt_pass_2.pack(side=tk.LEFT, padx=5)

prompt_error_2 = scrolledtext.ScrolledText(row3, height=10, width=65, bd=0, relief="raised", highlightbackground="red",bg = 'mistyrose')
prompt_error_2.pack(side=tk.LEFT, padx=5)

prompt_warn_2 = scrolledtext.ScrolledText(row3, height=10, width=55, bd=0, relief="raised", highlightbackground="red", bg = 'lightyellow')
prompt_warn_2.pack(side=tk.LEFT, padx=5)
row6 = tk.Frame(frame_3)
row6.pack(pady=1, fill=tk.X)
tk.Button(row6, text="开始检查", command=check_datas).pack(padx=500,side=tk.LEFT)
# 运行主事件循环
root.mainloop()