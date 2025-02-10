'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2024-12-31 15:48:11
LastEditors: bobo.bsx 2286362745@qq.com
LastEditTime: 2025-02-08 11:25:15
FilePath: \auto_package\package.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import sys
import os

sys.path.append(os.path.abspath("./bsx_func"))

import os_func as f
import tk_pcie_packing as tk_p
import dm_pcie_packing as dm_p
import global_vars as gl


if __name__ == "__main__":
    dm_pcie_name = ["P220L", "P2811", "P2306", "P2217", "P2300", "P2216"]

    pcie_data = gl.excel_data['PCIE']
    product_name = f.get_field_value(pcie_data[1], pcie_data[2], "产品")


    print("开始打包")
    if product_name in dm_pcie_name:
        dm_p.DM_PCIE_auto_packing()
    else:
        tk_p.TK_PCIE_auto_packing()


