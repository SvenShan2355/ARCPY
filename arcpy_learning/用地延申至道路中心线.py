# -*- coding: utf-8 -*-
"""
by Sven_SHAN  2022.10.11
"""
import os
import arcpy
from arcpy import analysis
from arcpy import management
from arcpy import edit


def Surface2Centerline(land_input_path, centerline_input_path, output_dir, YDDM, road_DM):
    '''
    参数（输入文件路径, 输出目录, 区分道路用地的字段名称, 道路用地代表的代码）
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

        # 道路用地整合
        Road_Surfaces = "C:\\TEMP_GDB.gdb\\road_surfaces"
        Land_Surfaces = "C:\\TEMP_GDB.gdb\\land_surfaces"
        road_selece_clause = YDDM + "=" + road_DM
        land_selece_clause = YDDM + "<>" + road_DM
        arcpy.analysis.Select(in_features=land_input_path, out_feature_class=Road_Surfaces,
                              where_clause=road_selece_clause)
        arcpy.analysis.Select(in_features=land_input_path, out_feature_class=Land_Surfaces,
                              where_clause=land_selece_clause)
        Road_Surface = "C:\\TEMP_GDB.gdb\\road_surface"
        arcpy.management.Dissolve(in_features=Road_Surfaces, out_feature_class=Road_Surface)

        # 用地功能提取为点
        information_points = "C:\\TEMP_GDB.gdb\\information_points"
        arcpy.management.FeatureToPoint(in_features=Land_Surfaces, out_feature_class=information_points,
                                        point_location="CENTROID")

        # 用地面转线
        old_Land_boundary = "C:\\TEMP_GDB.gdb\\old_Land_boundary"
        arcpy.management.FeatureToLine(in_features=Land_Surfaces, out_feature_class=old_Land_boundary)

        # 擦除与道路面重合的线
        land_boundary_updata = "C:\\TEMP_GDB.gdb\\land_boundary_updata"
        arcpy.analysis.Erase(in_features=old_Land_boundary, erase_features=Road_Surface,
                             out_feature_class=land_boundary_updata)
        arcpy.management.DeleteIdentical(in_dataset=land_boundary_updata, fields="Shape")

        # 形成新的用地边界
        new_land_boundary = "C:\\TEMP_GDB.gdb\\land_boundary_merge"
        arcpy.management.Merge(inputs=[land_boundary_updata, centerline_input_path], output=new_land_boundary)

        # 剩余用地线延申
        arcpy.edit.ExtendLine(in_features=new_land_boundary, length="50 Meters", extend_to="EXTENSION")

        # 边界转面
        new_land = "C:\\TEMP_GDB.gdb\\new_land"
        arcpy.management.FeatureToPolygon(in_features=new_land_boundary, out_feature_class=new_land)

        # 面赋值
        output_path = os.path.join(output_dir, "output_surface")
        arcpy.analysis.SpatialJoin(target_features=new_land, join_features=information_points,
                                   out_feature_class=output_path,
                                   join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", match_option="CONTAINS")

        # arcpy.management.Delete(r"C:\TEMP_GDB.gdb", '')
        # print("清除缓存")


if __name__ == '__main__':
    # 输入图层必须有"HCJL"和"DJJL"两个字段
    Surface2Centerline(r"E:\DataBase_本地更新库\ZJ\湛江市国土空间规划0930\Database\中心城区方案.gdb\霞山旧城20221011",
                       r"E:\DataBase_本地更新库\ZJ\湛江市国土空间规划0930\Database\中心城区方案.gdb\C_路网中心线合并",
                       r"E:\DataBase_本地更新库\ZJ\湛江市国土空间规划0930\Database\中心城区方案.gdb",
                       "YDYHEJLDM", "\'1207\'")
