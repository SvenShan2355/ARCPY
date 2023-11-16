# -*- coding: utf-8 -*-
"""
by Sven_SHAN  2022.10.11
"""
import os
import arcpy
from arcpy import analysis
from arcpy import management
import math
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

        sql_under_200 = r"Shape_Area < 200.05 and BZ = ''"
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

        arcpy.analysis.Select(outside_styn, cz,
                              r"CZCSX = '10' Or ((YDYHFLDM LIKE '12%' Or YDYHFLDM LIKE '15%') And CZCSX IS NULL)")
        arcpy.analysis.Select(outside_styn, nc, r"CZCSX = '20'")
        arcpy.analysis.Select(outside_styn, fjs,
                              r"CZCSX IS NULL AND YDYHFLDM NOT LIKE '12%' AND YDYHFLDM NOT LIKE '15%'")

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

        # arcpy.analysis.Select(stynw, cover, where_clause="(CZCSX1 = '20' or CZCSX = '') And Shape_Area > 200.05")
        #
        # arcpy.management.MakeFeatureLayer(stynw, 'stynw')
        # arcpy.management.SelectLayerByAttribute('stynw', "NEW_SELECTION", sql_under_200)
        # arcpy.management.Eliminate('stynw', stynw1, "LENGTH", ex_where_clause = ex_sql, ex_features=cover)
        #
        # arcpy.management.MakeFeatureLayer(stynw1, 'stynw1')
        # arcpy.management.SelectLayerByAttribute('stynw1', "NEW_SELECTION", sql_under_200)
        # arcpy.management.Eliminate('stynw1', stynw2, "LENGTH", ex_where_clause=ex_sql, ex_features=cover)
        #
        # arcpy.management.MakeFeatureLayer(stynw2, 'stynw2')
        # arcpy.management.SelectLayerByAttribute('stynw2', "NEW_SELECTION", sql_under_200)
        # arcpy.management.Eliminate('stynw2', stynw3, "LENGTH", ex_where_clause=ex_sql, ex_features=cover)
        # print(5)

        arcpy.management.Merge([stynw, inside_styn3], output_file)


def check_by_cursor(input_feature, output_feature_name, min_area=200):
    merge_features = []
    processed_features = set()

    fields = [feild.name for feild in arcpy.ListFields(input_feature) if not feild.required]
    czc_index = fields.index("CZCSX")
    bz_index = fields.index("BZ")

    with arcpy.da.SearchCursor(input_feature, ["OID@", "SHAPE@"] + fields) as cursor:
        for row in cursor:
            feature_id = row[0]
            feature_shape = row[1]
            feature_area = feature_shape.getArea("GEODESIC")
            feature_czc = row[czc_index+2]
            feature_bz = row[bz_index+2]
            print(row,feature_area)
            if feature_area > min_area:
                with arcpy.da.SearchCursor(input_feature, ["OID@", "SHAPE@"] + fields,
                                           f"OBJECTID <> {feature_id} AND SHAPE.STIntersects({feature_shape})='t'")as sub_cursor:
                    for sub_row in sub_cursor:
                        sub_feature_id = sub_row[0]
                        sub_feature_shape = sub_row[1]
                        sub_feature_area = sub_feature_shape.getArea("GEODESIC")
                        sub_feature_czc = sub_row[czc_index+2]
                        sub_feature_bz = sub_row[bz_index+2]
                        if sub_feature_area < min_area and sub_feature_czc == feature_czc and sub_feature_bz == feature_bz:
                            feature_shape = feature_shape.union(sub_feature_shape)
                            processed_features.add(sub_feature_id)
                feature_row = [feature_id, feature_shape] + list(row[3:])
                merge_features.append(feature_row)
            else:
                feature_row = [feature_id, feature_shape] + list(row[3:])
                merge_features.append(feature_row)
        for row in merge_features:
            feature_id = row[0]
            if feature_id in processed_features:
                merge_features.remove(row)
    print(merge_features)

    arcpy.CreateFeatureclass_management(r"E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\过程文件\矢量\Arcpy_Output_Database.gdb",
                                        output_feature_name, "POLYGON", spatial_reference=input_feature)

    with arcpy.da.InsertCursor(
            os.path.join(r"E:\工程文件\2_湛江市国土空间总体规划（2020-2035年）\过程文件\矢量\Arcpy_Output_Database.gdb", output_feature_name),
            ["SHAPE@"] + fields) as cursor:
        for row in merge_features:
            feature_shape = row[1]
            feature_fields = row[2:]
            if feature_shape is not None:
                cursor.insertRow([feature_shape]+feature_fields)
