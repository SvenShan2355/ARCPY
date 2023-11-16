# -*- coding: utf-8 -*-
"""
by Sven_SHAN  2022.11.07
"""
from Design_scheme_processing.method import Merge_Plan
from Design_scheme_processing.method import Offset_Centerline_of_Road
from Design_scheme_processing.method import eliminate_under_200
import shutil

if __name__ == '__main__':
    # 从中心线生成路网
    # Offset_Centerline_of_Road.Model_I(
    #     r"E:\DataBase_本地更新库\湛江市国土空间规划\Database\中心城区方案.gdb\中心城区道路中心线20230708",
    #     r"E:\DataBase_本地更新库\湛江市国土空间规划\Database\中心城区方案.gdb\立交节点0307",
    #     r"E:\DataBase_本地更新库\湛江市国土空间规划\Output_Database.gdb", "HCJL", "DJJL")

    # 合成方案
    # Merge_Plan.Model_For_Part_Entirety_Replace(
    #     bgdc=r"E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\主工程文件\GIS湛江市国土空间规划\湛江市国土空间规划.gdb\中心城区XZYDYH20230809",
    #     plan=r"E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\过程文件\矢量\中心城区方案.gdb\霞山赤坎方案到中心线20231114",  # 微调版需要更换
    #     sea=r"E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\主工程文件\GIS湛江市国土空间规划\湛江市国土空间规划.gdb\湛江市海域规划分区20230726",
    #     sea_range=r"E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\主工程文件\GIS湛江市国土空间规划\湛江市国土空间规划.gdb\E海域范围_20000_至三调边界",
    #     road=r"E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\过程文件\矢量\Arcpy_Output_Database.gdb\output_roads_20231031_ckxs",
    #     # range=r"E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\过程文件\矢量\中心城区方案.gdb\湛江中心城区20231114",
    #     range=r"E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\主工程文件\GIS湛江市国土空间规划\湛江市国土空间规划.gdb\赤坎霞山入库范围",
    #     entirety_replace_part=r"E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\过程文件\矢量\中心城区方案.gdb\PTMZ用地方案1114_sdax",
    #     zone=r"E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\主工程文件\GIS湛江市国土空间规划\湛江市国土空间规划.gdb\赤坎霞山入库范围",
    #     czc=r"E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\主工程文件\GIS湛江市国土空间规划\湛江市国土空间规划.gdb\变更调查2020乡村建设用地203",
    #     jsyd=r'E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\主工程文件\GIS湛江市国土空间规划\湛江市国土空间规划.gdb\变更调查2020建设用地',
    #     kfbj=r"E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\主工程文件\GIS湛江市国土空间规划\湛江市国土空间规划.gdb\封库城镇开发边界",  # 微调版需要更换
    #     yjjbnt=r'E:\数据文件\广东省\湛江市\0_市本级\基础数据\03_三区三线\20221110_广东省“三区三线”划定成果矢量数据（部下发封库版）\三区三线下发版.gdb\永久基本农田',
    #     stbhhx=r'E:\数据文件\广东省\湛江市\0_市本级\基础数据\03_三区三线\20221110_广东省“三区三线”划定成果矢量数据（部下发封库版）\三区三线下发版.gdb\陆域生态保护红线',
    #     dm2name_table=r"E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\主工程文件\GIS湛江市国土空间规划\湛江市国土空间规划.gdb\dm2name_",
    #     output_path=r"E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\过程文件\矢量\Arcpy_Output_Database.gdb",
    #     plan_across_shoreline=1,
    #     plan_across_kfbj=1
    # )

    # 消除碎图斑
    # eliminate_under_200.eliminate_under_200(input_file=r'E:\DataBase_本地更新库\湛江市国土空间规划\Output_Database.gdb\complete_plan_20231031_xs',
    #                                         styn=r'E:\DataBase_共享总库\ZJ\04_三区三线试划\成果_20221110-广东省“三区三线”划定成果矢量数据（部下发封库版）\三区三线下发版.gdb\STBHYN_d',
    #                                         output_file=r'E:\DataBase_本地更新库\湛江市国土空间规划\Output_Database.gdb\complete_plan_20231031_xs_E',
    #                                         jsyd=r'E:\DataBase_本地更新库\湛江市国土空间规划\湛江市国土空间规划.gdb\变更调查2020建设用地')
    eliminate_under_200.check_by_cursor(
        input_feature=r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb\规划用地用海_Dissolv_MultipartToSi",
        output_feature_name="complete_plan_20231116_ck_E")

    '''
    执行完成后需要的步骤：
    1 消除碎图斑
    2 重新计算面积和标识码

    '''
