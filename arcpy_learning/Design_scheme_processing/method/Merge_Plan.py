# -*- coding: utf-8 -*-
"""
by Sven_SHAN  2022.11.07
"""
import os
import arcpy
from arcpy import analysis
from arcpy import management


def Model_For_Merge_Plan(bgdc, plan, sea, sea_range, road, range, output_path):  # 模型
    '''
    参数（现状图层, 方案图层, 用海图层, 海域范围，路网图层, 中心城区范围图层, 输出目录）
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
        print("Process: 建立缓存空间")

        clip1 = "C:\\TEMP_GDB.gdb\\clip1"
        arcpy.analysis.Clip(bgdc, range, clip1)
        print("Process: 擦除方案范围外现状用地图斑")

        clip2 = "C:\\TEMP_GDB.gdb\\clip2"
        arcpy.analysis.Clip(sea, range, clip2)
        print("Process: 擦除方案范围外用海图斑")

        erase1 = "C:\\TEMP_GDB.gdb\\erase1"
        arcpy.analysis.Erase(clip1, plan, erase1)
        print("Process: 擦除规划范围")

        merge1 = "C:\\TEMP_GDB.gdb\\merge1"
        # 维护合并字段
        # Create the required FieldMap and FieldMappings objects
        infile1 = erase1
        infile2 = plan
        fm_YDYHYJLDM = arcpy.FieldMap()
        fm_YDYHEJLDM = arcpy.FieldMap()
        fm_YDYHSJLDM = arcpy.FieldMap()
        fms = arcpy.FieldMappings()
        # Get the field names of vegetation type and diameter for both original
        infile1_YDYHYJLDM = '一级代码'
        infile1_YDYHEJLDM = '二级代码'
        infile1_YDYHSJLDM = 'GTFLMCDM'
        infile2_YDYHYJLDM = 'YDYHYJLDM'
        infile2_YDYHEJLDM = 'YDYHEJLDM'
        infile2_YDYHSJLDM = 'YDYHSJLDM'
        # Add fields to their corresponding FieldMap objects
        fm_YDYHYJLDM.addInputField(infile1, infile1_YDYHYJLDM)
        fm_YDYHYJLDM.addInputField(infile2, infile2_YDYHYJLDM)
        fm_YDYHEJLDM.addInputField(infile1, infile1_YDYHEJLDM)
        fm_YDYHEJLDM.addInputField(infile2, infile2_YDYHEJLDM)
        fm_YDYHSJLDM.addInputField(infile1, infile1_YDYHSJLDM)
        fm_YDYHSJLDM.addInputField(infile2, infile2_YDYHSJLDM)
        # Set the output field properties for both FieldMap objects
        YDYHYJLDM = fm_YDYHYJLDM.outputField
        YDYHYJLDM.name = 'YDYHYJLDM'
        YDYHYJLDM.aliasName = 'YDYHYJLDM'
        YDYHYJLDM.length = 2
        fm_YDYHYJLDM.outputField = YDYHYJLDM
        YDYHEJLDM = fm_YDYHEJLDM.outputField
        YDYHEJLDM.name = 'YDYHEJLDM'
        YDYHEJLDM.aliasName = 'YDYHEJLDM'
        YDYHEJLDM.length = 4
        fm_YDYHEJLDM.outputField = YDYHEJLDM
        YDYHSJLDM = fm_YDYHSJLDM.outputField
        YDYHSJLDM.name = 'YDYHSJLDM'
        YDYHSJLDM.aliasName = 'YDYHSJLDM'
        YDYHSJLDM.length = 6
        fm_YDYHSJLDM.outputField = YDYHSJLDM
        # Add the FieldMap objects to the FieldMappings object
        fms.addFieldMap(fm_YDYHYJLDM)
        fms.addFieldMap(fm_YDYHEJLDM)
        fms.addFieldMap(fm_YDYHSJLDM)
        print("Process: 维护合并字段")
        arcpy.management.Merge([erase1, plan], merge1, fms)
        print("Process: 合并规划范围")

        plan_sea = "C:\\TEMP_GDB.gdb\\plan_sea"
        arcpy.analysis.Select(plan, plan_sea,
                              "YDYHEJLDM LIKE '18%' OR YDYHEJLDM LIKE '19%' OR YDYHEJLDM LIKE '20%' OR YDYHEJLDM LIKE '21%' OR YDYHEJLDM LIKE '22%' OR YDYHEJLDM LIKE '24%' ")
        print("Process: 选择规划海域")

        erase_sea_range = "C:\\TEMP_GDB.gdb\\erase_sea_range"
        arcpy.analysis.Erase(merge1, sea_range, erase_sea_range)
        print("Process: 擦除海岸线外规划")

        merge_plan_and_sea = "C:\\TEMP_GDB.gdb\\merge_plan_and_sea"
        arcpy.management.Merge([plan_sea, erase_sea_range], merge_plan_and_sea)
        print("Process: 组合海岸线内规划和规划用海")

        old_sea_left = "C:\\TEMP_GDB.gdb\\old_sea_left"
        arcpy.analysis.Erase(sea, plan_sea, old_sea_left)
        print("Process: 擦除已规划海域")

        merge2 = "C:\\TEMP_GDB.gdb\\merge2"
        arcpy.management.Merge([merge_plan_and_sea, old_sea_left], merge2)

        erase2 = "C:\\TEMP_GDB.gdb\\erase2"
        arcpy.analysis.Erase(merge2, road, erase2)
        print("Process: 擦除道路")

        merge3 = "C:\\TEMP_GDB.gdb\\merge3"
        arcpy.management.Merge([erase2, road], merge3)
        print("Process: 合并道路")

        output_name = os.path.join(output_path, "merged_plan")
        arcpy.analysis.Clip(merge3, range, output_name)
        print("Process: 擦除方案范围外图斑")

        arcpy.management.AddField(output_name, field_name="COLOR", field_type="TEXT", field_length=4)

        color_codebook = """
def color(DM):
    if DM[:2] in ['08', '10', '11', '14']:
        return DM
    elif DM in ['0701', '0702']:
        return '0701'
    elif DM in ['0703', '0704']:
        return '0703'
    elif DM in ['1202', '1205', '1207']:
        return DM
    else:
        return DM[:2]
        """

        arcpy.management.CalculateField(output_name, field="COLOR", expression="color(!YDYHEJLDM!)",
                                        expression_type="PYTHON3", code_block=color_codebook)

        arcpy.management.Delete(r"C:\TEMP_GDB.gdb", '')
        print("清除缓存")


def Model_For_Part_Entirety_Replace(bgdc, plan, sea, sea_range, road, range, entirety_replace_part, output_path):  # 模型
    '''
    参数（现状图层, 方案图层, 用海图层, 海域范围，路网图层, 中心城区范围图层, 需要整体替换的部分，输出目录）
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
        print("Process: 建立缓存空间")

        clip1 = "C:\\TEMP_GDB.gdb\\clip1"
        arcpy.analysis.Clip(bgdc, range, clip1)
        print("Process: 擦除方案范围外现状用地图斑")

        clip2 = "C:\\TEMP_GDB.gdb\\clip2"
        arcpy.analysis.Clip(sea, range, clip2)
        print("Process: 擦除方案范围外用海图斑")

        erase1 = "C:\\TEMP_GDB.gdb\\erase1"
        arcpy.analysis.Erase(clip1, plan, erase1)
        print("Process: 擦除规划范围")

        merge1 = "C:\\TEMP_GDB.gdb\\merge1"
        # 维护合并字段
        # Create the required FieldMap and FieldMappings objects
        infile1 = erase1
        infile2 = plan
        fm_YDYHYJLDM = arcpy.FieldMap()
        fm_YDYHEJLDM = arcpy.FieldMap()
        fm_YDYHSJLDM = arcpy.FieldMap()
        fms = arcpy.FieldMappings()
        # Get the field names of vegetation type and diameter for both original
        infile1_YDYHYJLDM = '一级代码'
        infile1_YDYHEJLDM = '二级代码'
        infile1_YDYHSJLDM = 'GTFLMCDM'
        infile2_YDYHYJLDM = 'YDYHYJLDM'
        infile2_YDYHEJLDM = 'YDYHEJLDM'
        infile2_YDYHSJLDM = 'YDYHSJLDM'
        # Add fields to their corresponding FieldMap objects
        fm_YDYHYJLDM.addInputField(infile1, infile1_YDYHYJLDM)
        fm_YDYHYJLDM.addInputField(infile2, infile2_YDYHYJLDM)
        fm_YDYHEJLDM.addInputField(infile1, infile1_YDYHEJLDM)
        fm_YDYHEJLDM.addInputField(infile2, infile2_YDYHEJLDM)
        fm_YDYHSJLDM.addInputField(infile1, infile1_YDYHSJLDM)
        fm_YDYHSJLDM.addInputField(infile2, infile2_YDYHSJLDM)
        # Set the output field properties for both FieldMap objects
        YDYHYJLDM = fm_YDYHYJLDM.outputField
        YDYHYJLDM.name = 'YDYHYJLDM'
        YDYHYJLDM.aliasName = 'YDYHYJLDM'
        YDYHYJLDM.length = 2
        fm_YDYHYJLDM.outputField = YDYHYJLDM
        YDYHEJLDM = fm_YDYHEJLDM.outputField
        YDYHEJLDM.name = 'YDYHEJLDM'
        YDYHEJLDM.aliasName = 'YDYHEJLDM'
        YDYHEJLDM.length = 4
        fm_YDYHEJLDM.outputField = YDYHEJLDM
        YDYHSJLDM = fm_YDYHSJLDM.outputField
        YDYHSJLDM.name = 'YDYHSJLDM'
        YDYHSJLDM.aliasName = 'YDYHSJLDM'
        YDYHSJLDM.length = 6
        fm_YDYHSJLDM.outputField = YDYHSJLDM
        # Add the FieldMap objects to the FieldMappings object
        fms.addFieldMap(fm_YDYHYJLDM)
        fms.addFieldMap(fm_YDYHEJLDM)
        fms.addFieldMap(fm_YDYHSJLDM)
        print("Process: 维护合并字段")
        arcpy.management.Merge([erase1, plan], merge1, fms)
        print("Process: 合并规划范围")

        plan_sea = "C:\\TEMP_GDB.gdb\\plan_sea"
        arcpy.analysis.Select(plan, plan_sea,
                              "YDYHEJLDM LIKE '18%' OR YDYHEJLDM LIKE '19%' OR YDYHEJLDM LIKE '20%' OR YDYHEJLDM LIKE '21%' OR YDYHEJLDM LIKE '22%' OR YDYHEJLDM LIKE '24%' ")
        print("Process: 选择规划海域")

        erase_sea_range = "C:\\TEMP_GDB.gdb\\erase_sea_range"
        arcpy.analysis.Erase(merge1, sea_range, erase_sea_range)
        print("Process: 擦除海岸线外规划")

        merge_plan_and_sea = "C:\\TEMP_GDB.gdb\\merge_plan_and_sea"
        arcpy.management.Merge([plan_sea, erase_sea_range], merge_plan_and_sea)
        print("Process: 组合海岸线内规划和规划用海")

        old_sea_left = "C:\\TEMP_GDB.gdb\\old_sea_left"
        arcpy.analysis.Erase(sea, plan_sea, old_sea_left)
        print("Process: 擦除已规划海域")

        merge2 = "C:\\TEMP_GDB.gdb\\merge2"
        arcpy.management.Merge([merge_plan_and_sea, old_sea_left], merge2)

        erase2 = "C:\\TEMP_GDB.gdb\\erase2"
        arcpy.analysis.Erase(merge2, road, erase2)
        print("Process: 擦除道路")

        merge3 = "C:\\TEMP_GDB.gdb\\merge3"
        arcpy.management.Merge([erase2, road], merge3)
        print("Process: 合并道路")

        merge_plan1 = "C:\\TEMP_GDB.gdb\\merge_plan1"
        arcpy.analysis.Clip(merge3, range, merge_plan1)
        print("Process: 擦除方案范围外图斑")

        erase3 = "C:\\TEMP_GDB.gdb\\erase3"
        arcpy.analysis.Erase(merge_plan1, entirety_replace_part, erase3)

        arcpy.management.AddField(merge_plan1, field_name="COLOR", field_type="TEXT", field_length=4)

        output_name = os.path.join(output_path, "merged_plan1")
        arcpy.management.Merge([erase3, entirety_replace_part], output_name)

        color_codebook = """
def color(DM):
    if DM[:2] in ['08', '10', '11', '14']:
        return DM
    elif DM in ['0701', '0702']:
        return '0701'
    elif DM in ['0703', '0704']:
        return '0703'
    elif DM in ['1202', '1205', '1207']:
        return DM
    else:
        return DM[:2]
        """

        arcpy.management.CalculateField(output_name, field="COLOR", expression="color(!YDYHEJLDM!)",
                                        expression_type="PYTHON3", code_block=color_codebook)

        arcpy.management.Delete(r"C:\TEMP_GDB.gdb", '')
        print("清除缓存")
