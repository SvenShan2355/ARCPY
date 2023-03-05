# -*- coding: utf-8 -*-
"""
by Sven_SHAN  2022.11.07
"""
from 方案处理.method import Offset_Centerline_of_Road, Merge_Plan

if __name__ == '__main__':
    # Offset_Centerline_of_Road.Model(
    #     r"E:\DataBase_本地更新库\湛江市国土空间规划\Database\中心城区方案.gdb\中心城区道路中线20230301",
    #     r"E:\DataBase_本地更新库\湛江市国土空间规划\Database\中心城区方案.gdb\立交节点1112",
    #     r"E:\DataBase_本地更新库\湛江市国土空间规划\Output_Database.gdb", "HCJL", "DJJL")

    Merge_Plan.Model_For_Part_Entirety_Replace(
        bgdc=r"E:\DataBase_共享总库\ZJ\06_现状细化数据\中心城区\2022.07.11现状图\001库\市辖区现状图.gdb\变更调查2020海岸线内外合并",
        plan=r"E:\DataBase_本地更新库\湛江市国土空间规划\Database\中心城区方案.gdb\B赤霞坡方案20230215_到中心线",
        sea=r"E:\DataBase_共享总库\ZJ\0_基础数据总库\440800湛江市市级国土空间总体规划矢量数据.gdb\HYGNFQ",
        sea_range=r"E:\DataBase_本地更新库\湛江市国土空间规划\湛江市国土空间规划.gdb\E海域范围新",
        road=r"E:\DataBase_本地更新库\湛江市国土空间规划\Output_Database.gdb\output_roads_d",
        range=r"E:\DataBase_本地更新库\湛江市国土空间规划\Database\中心城区方案.gdb\中心城区范围线20221118",
        entirety_replace_part=r"E:\DataBase_本地更新库\湛江市国土空间规划\Database\中心城区方案.gdb\麻章方案20230221",
        zone=r"E:\DataBase_共享总库\ZJ\0_基础数据总库\湛江市国土空间总体规划.gdb\B市辖区县级行政边界",
        dm2name_table=r"E:\DataBase_本地更新库\湛江市国土空间规划\湛江市国土空间规划.gdb\dm2name_",
        output_path=r"E:\DataBase_本地更新库\湛江市国土空间规划\Output_Database.gdb")

    '''
    执行完成后需要的步骤：
    1 消除碎图斑
    2 重新计算面积和标识码
    3 修改新型产业用地类型
    
    '''