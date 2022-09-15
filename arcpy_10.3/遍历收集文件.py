# -*- coding:UTF-8 -*-

import arcpy
import os
import re

file_path_list = []


# 遍历所有文件目录并提取文件格式为mdb的文件的文件路径
def get_all_mdb_path(folder_path):
    global file_path_list
    target_regex = re.compile(r'(\w)*.mdb')
    target_list = os.listdir(folder_path)
    for target in target_list:
        target_path = os.path.join(folder_path, target)
        if os.path.isdir(target_path):
            get_all_mdb_path(target_path)
        else:
            if target_regex.search(target_path) is not None:
                file_path_list.append(target_path)
    return


if __name__ == '__main__':
    # 需要收集的文件目录
    file_path = r"D:\PL\DataBase_共享总库\ZJ\05_各种规划\土规\45土规方案汇总".decode('utf8')

    # # 新建地理数据库
    # path = r'./'
    # arcpy.CreateFileGDB_management(path, 'test')

    # 遍历所有文件目录并提取文件格式为mdb的文件的文件路径
    get_all_mdb_path(file_path)

    XMID = 0

    # 遍历所有找到的mdb
    for test_path in file_path_list:
        XMID = XMID + 1
        # 将所选mdb设置为工作环境
        arcpy.env.workspace = test_path
        # 将所选mdb对应的文件目录部分生成项目名称
        XMMC = test_path.split("\\")[8]
        # 确定导入的文件名
        file_name = 'TG' + str(XMID)
        # 寻找mdb中需要导入的要素数据集，并导入创建的地理数据库
        fdss = arcpy.ListFeatureClasses()
        if 'LSDKFW' in fdss:
            arcpy.FeatureClassToFeatureClass_conversion(in_features='LSDKFW', out_path=r'.\test.gdb',
                                                        out_name=file_name)
        elif 'TZDKFW' in fdss:
            arcpy.FeatureClassToFeatureClass_conversion(in_features='TZDKFW', out_path=r'.\test.gdb',
                                                        out_name=file_name)
        # 切换工作路径为新建地理数据库
        arcpy.env.workspace = r'.\test.gdb'
        # 增加字段并将项目名称填入对应字段
        arcpy.AddField_management(in_table=file_name, field_name='XMMC', field_type='TEXT', field_length='255')
        arcpy.CalculateField_management(in_table=file_name, field='XMMC', expression='"' + XMMC + '"')
