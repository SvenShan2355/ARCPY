# -*- coding: utf-8 -*-
"""
by Sven_SHAN  2022.10.25
"""
import os
import arcpy
from arcpy import analysis
from arcpy import management

def Model(centerline_path, output_path, buffer_distance, chamfer_distance):  # 模型
    '''
    参数（中心线图层, 输出目录, 缓冲距离字段名称[缓冲距离为红线宽度的一半], 倒角距离字段名称）
    '''

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    # Model Environment settings
    with arcpy.EnvManager(
            cartographicCoordinateSystem="PROJCS[\"CGCS2000_3_Degree_GK_Zone_37\",GEOGCS[\"GCS_China_Geodetic_Coordinate_System_2000\",DATUM[\"D_China_2000\",SPHEROID[\"CGCS2000\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Gauss_Kruger\"],PARAMETER[\"False_Easting\",37500000.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",111.0],PARAMETER[\"Scale_Factor\",1.0],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]",
            scratchWorkspace=r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb",
            workspace=r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb"):
        arcpy.management.CreateFileGDB("C:\\", "TEMP_GDB", "CURRENT")

        print("水文分析ing.....")

        print("填洼")
        print("流向分析")
        print("流量分析")
        print("提取河网")
        print("河网分级")
        print("栅格河网矢量化")
        print("平滑河网")
        print("流域分析")

if __name__ == '__main__':
    # 输入图层必须有"HCJL"和"DJJL"两个字段
    Model(r"D:\PL\DataBase_本地更新库\ZJ\湛江市国土空间规划0930\Database\中心城区方案.gdb\D_路网中心线合并整理20221021",
          r"D:\PL\DataBase_本地更新库\ZJ\湛江市国土空间规划0930\Database\中心城区方案.gdb", "HCJL", "DJJL")