# -*- coding: utf-8 -*-
"""
by Sven_SHAN  2022.10.25
"""
import os
import arcpy
from arcpy import management
from arcpy import analysis


def Hydrologic_Analysis(t_map, output_path, Terrestrial_area):  # 模型
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
        # arcpy.management.CreateFileGDB("C:\\", "TEMP_GDB", "CURRENT")

        print("水文分析ing.....")

        outfill = arcpy.sa.Fill(t_map)
        print("填洼完成")

        outFlowDirection = arcpy.sa.FlowDirection(outfill, force_flow="NORMAL")
        print("流向分析完成")

        outFlowAccumulation = arcpy.sa.FlowAccumulation(outFlowDirection)
        print("流量分析完成")

        # river_net = "C:\\TEMP_GDB.gdb\\river_net"
        # arcpy.sa.RasterCalculator("Con(outFlowAccumulation>1000,1)", river_net)
        river_net = arcpy.ia.Con(outFlowAccumulation > 1000, 1)
        print("提取河网完成")

        outStreamOrder = arcpy.sa.StreamOrder(river_net, outFlowDirection, order_method="STRAHLER")
        print("河网分级完成")

        ver_river_net_path = os.path.join(output_path, "ver_river_net")
        arcpy.sa.StreamToFeature(outStreamOrder, outFlowDirection, ver_river_net_path)
        print("栅格河网矢量化完成")

        Basin_path = os.path.join(output_path, "Basin")
        arcpy.sa.Basin(outFlowDirection).save(Basin_path)
        print("流域分析完成")

        ver_river_net_clip = os.path.join(output_path, "ver_river_net_clip")
        analysis.Clip(in_features=ver_river_net_path, clip_features=Terrestrial_area, out_feature_class=ver_river_net_clip)
        print("裁剪海岸线内部分")

        outHillshade = os.path.join(output_path, "Hillshade")
        arcpy.sa.Hillshade(t_map, azimuth=135, model_shadows="SHADOWS").save(outHillshade)



if __name__ == '__main__':

    Hydrologic_Analysis(r"D:\PL\DataBase_共享总库\ZJ\10_地形图\湛江地形图\Rectangle_#1_高程\Rectangle_#1_高程\Rectangle_#1_高程_Level_16.tif",
                        r"D:\PL\DataBase_本地更新库\ZJ\湛江市国土空间规划0930\Output_Database.gdb",
                        r"D:\PL\DataBase_本地更新库\ZJ\湛江市国土空间规划0930\湛江市国土空间规划.gdb\湛江陆域范围")
