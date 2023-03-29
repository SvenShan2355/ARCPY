# -*- coding: utf-8 -*-
"""
by Sven_SHAN  2022.10.11
"""
import os
import arcpy
from arcpy import analysis
from arcpy import management
from arcpy import edit


def eliminate_under_200(input_file, styn, output_file, jsyd):
    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False

    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")
    # Model Environment settings
    with arcpy.EnvManager(
            cartographicCoordinateSystem="PROJCS[\"CGCS2000_3_Degree_GK_Zone_37\",GEOGCS[\"GCS_China_Geodetic_Coordinate_System_2000\",DATUM[\"D_China_2000\",SPHEROID[\"CGCS2000\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Gauss_Kruger\"],PARAMETER[\"False_Easting\",37500000.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",111.0],PARAMETER[\"Scale_Factor\",1.0],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]",
            scratchWorkspace=r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb",
            workspace=r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb"):
        arcpy.management.CreateFileGDB("C:\\", "TEMP_GDB", "CURRENT")

        sql_under_200 = r'Shape_Area < 200.05'
        ex_sql = r"(CZCSX1 = '20' or CZCSX = '') And Shape_Area > 200.05"

        inside_styn = r'C:\\TEMP_GDB.gdb\\inside_styn'
        inside_styn1 = r'C:\\TEMP_GDB.gdb\\inside_styn1'
        inside_styn2 = r'C:\\TEMP_GDB.gdb\\inside_styn2'
        inside_styn3 = r'C:\\TEMP_GDB.gdb\\inside_styn3'
        outside_styn = r'C:\\TEMP_GDB.gdb\\outside_styn'
        arcpy.analysis.Clip(input_file, styn, inside_styn)

        arcpy.management.MakeFeatureLayer(inside_styn, 'inside_styn')
        arcpy.management.SelectLayerByAttribute('inside_styn', "NEW_SELECTION", sql_under_200)
        arcpy.management.Eliminate('inside_styn', inside_styn1, "LENGTH", ex_where_clause="jsyd = 1", ex_features=jsyd)

        arcpy.management.MakeFeatureLayer(inside_styn1, 'inside_styn1')
        arcpy.management.SelectLayerByAttribute('inside_styn1', "NEW_SELECTION", sql_under_200)
        arcpy.management.Eliminate('inside_styn1', inside_styn2, "LENGTH", ex_where_clause="jsyd = 1", ex_features=jsyd)

        arcpy.management.MakeFeatureLayer(inside_styn2, 'inside_styn2')
        arcpy.management.SelectLayerByAttribute('inside_styn2', "NEW_SELECTION", sql_under_200)
        arcpy.management.Eliminate('inside_styn2', inside_styn3, "LENGTH", ex_where_clause="jsyd = 1", ex_features=jsyd)

        arcpy.analysis.Erase(input_file, styn, outside_styn)

        cz = r'C:\\TEMP_GDB.gdb\\cz'
        nc = r'C:\\TEMP_GDB.gdb\\nc'
        fjs = r'C:\\TEMP_GDB.gdb\\fjs'

        arcpy.analysis.Select(outside_styn, cz, r"CZCSX IN ('10', '区域', '特殊')")
        arcpy.analysis.Select(outside_styn, nc, r"CZCSX IN ('20')")
        arcpy.analysis.Select(outside_styn, fjs, r"CZCSX IN ('')")

        cz1 = r'C:\\TEMP_GDB.gdb\\cz1'
        cz2 = r'C:\\TEMP_GDB.gdb\\cz2'
        cz3 = r'C:\\TEMP_GDB.gdb\\cz3'

        nc1 = r'C:\\TEMP_GDB.gdb\\nc1'
        nc2 = r'C:\\TEMP_GDB.gdb\\nc2'
        nc3 = r'C:\\TEMP_GDB.gdb\\nc3'

        fjs1 = r'C:\\TEMP_GDB.gdb\\fjs1'
        fjs2 = r'C:\\TEMP_GDB.gdb\\fjs2'
        fjs3 = r'C:\\TEMP_GDB.gdb\\fjs3'

        arcpy.management.MakeFeatureLayer(cz, 'cz')
        arcpy.management.SelectLayerByAttribute('cz', "NEW_SELECTION", sql_under_200)
        arcpy.management.Eliminate('cz', cz1, "LENGTH")

        arcpy.management.MakeFeatureLayer(cz1, 'cz1')
        arcpy.management.SelectLayerByAttribute('cz1', "NEW_SELECTION", sql_under_200)
        arcpy.management.Eliminate('cz1', cz2, "LENGTH")

        arcpy.management.MakeFeatureLayer(cz2, 'cz2')
        arcpy.management.SelectLayerByAttribute('cz2', "NEW_SELECTION", sql_under_200)
        arcpy.management.Eliminate('cz2', cz3, "LENGTH")
        print(1)

        arcpy.management.MakeFeatureLayer(nc, 'nc')
        arcpy.management.SelectLayerByAttribute('nc', "NEW_SELECTION", sql_under_200)
        arcpy.management.Eliminate('nc', nc1, "LENGTH")

        arcpy.management.MakeFeatureLayer(nc1, 'nc1')
        arcpy.management.SelectLayerByAttribute('nc1', "NEW_SELECTION", sql_under_200)
        arcpy.management.Eliminate('nc1', nc2, "LENGTH")

        arcpy.management.MakeFeatureLayer(nc2, 'nc2')
        arcpy.management.SelectLayerByAttribute('nc2', "NEW_SELECTION", sql_under_200)
        arcpy.management.Eliminate('nc2', nc3, "LENGTH")
        print(2)

        arcpy.management.MakeFeatureLayer(fjs, 'fjs')
        arcpy.management.SelectLayerByAttribute('fjs', "NEW_SELECTION", sql_under_200)
        arcpy.management.Eliminate('fjs', fjs1, "LENGTH")

        arcpy.management.MakeFeatureLayer(fjs1, 'fjs1')
        arcpy.management.SelectLayerByAttribute('fjs1', "NEW_SELECTION", sql_under_200)
        arcpy.management.Eliminate('fjs1', fjs2, "LENGTH")

        arcpy.management.MakeFeatureLayer(fjs2, 'fjs2')
        arcpy.management.SelectLayerByAttribute('fjs2', "NEW_SELECTION", sql_under_200)
        arcpy.management.Eliminate('fjs2', fjs3, "LENGTH")
        print(3)

        stynw = r'C:\\TEMP_GDB.gdb\\stynw'
        stynw1 = r'C:\\TEMP_GDB.gdb\\stynw1'
        stynw2 = r'C:\\TEMP_GDB.gdb\\stynw2'
        stynw3 = r'C:\\TEMP_GDB.gdb\\stynw3'
        cover = r'C:\\TEMP_GDB.gdb\\cover'

        arcpy.management.Merge([cz3, nc3, fjs3], stynw)
        print(4)

        arcpy.analysis.Select(stynw, cover, where_clause="(CZCSX1 = '20' or CZCSX = '') And Shape_Area > 200.05")

        arcpy.management.MakeFeatureLayer(stynw, 'stynw')
        arcpy.management.SelectLayerByAttribute('stynw', "NEW_SELECTION", sql_under_200)
        arcpy.management.Eliminate('stynw', stynw1, "LENGTH", ex_where_clause = ex_sql, ex_features=cover)

        arcpy.management.MakeFeatureLayer(stynw1, 'stynw1')
        arcpy.management.SelectLayerByAttribute('stynw1', "NEW_SELECTION", sql_under_200)
        arcpy.management.Eliminate('stynw1', stynw2, "LENGTH", ex_where_clause=ex_sql, ex_features=cover)

        arcpy.management.MakeFeatureLayer(stynw2, 'stynw2')
        arcpy.management.SelectLayerByAttribute('stynw2', "NEW_SELECTION", sql_under_200)
        arcpy.management.Eliminate('stynw2', stynw3, "LENGTH", ex_where_clause=ex_sql, ex_features=cover)
        print(5)

        arcpy.management.Merge([stynw3, inside_styn3], output_file)

    arcpy.management.Delete(r"C:\TEMP_GDB.gdb", '')
    print("Process: 清除缓存")
