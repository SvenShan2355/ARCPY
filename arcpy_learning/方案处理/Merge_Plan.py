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


def Model_For_Part_Entirety_Replace(bgdc, plan, sea, sea_range, road, range, entirety_replace_part, zone, dm2name_table,
                                    output_path):  # 模型
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
        '''
        ————————————————创建缓存空间部分————————————————
        '''

        arcpy.management.CreateFileGDB("C:\\", "TEMP_GDB", "CURRENT")
        print("Process: 建立缓存空间")

        '''
        ————————————————合并用地方案部分————————————————
        '''

        inside_ZXCQ_current_land = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_current_land"
        arcpy.analysis.Clip(bgdc, range, inside_ZXCQ_current_land)
        print("Process: 擦除中心城区范围外现状用地图斑")

        inside_ZXCQ_plan_sea = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_sea"
        arcpy.analysis.Clip(sea, range, inside_ZXCQ_plan_sea)
        print("Process: 擦除中心城区范围外用海图斑")

        inside_ZXCQ_plan_land = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_land"
        arcpy.analysis.Clip(plan, range, inside_ZXCQ_plan_land)
        print("Process: 擦除中心城区范围外规划用地图斑")

        inside_ZXCQ_plan_road = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_road"
        arcpy.analysis.Clip(road, range, inside_ZXCQ_plan_road)
        print("Process: 擦除中心城区范围外规划道路图斑")

        inside_ZXCQ_unplanned_land = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_unplanned_land"
        arcpy.analysis.Erase(inside_ZXCQ_current_land, inside_ZXCQ_plan_land, inside_ZXCQ_unplanned_land)
        print("Process: 中心城区范围内，提取保留现状部分图斑")

        inside_ZXCQ_Cland_and_Pland = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_Cland_and_Pland"
        # 维护合并字段
        # Create the required FieldMap and FieldMappings objects
        infile1 = inside_ZXCQ_unplanned_land
        infile2 = inside_ZXCQ_plan_land
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
        arcpy.management.Merge([inside_ZXCQ_unplanned_land, inside_ZXCQ_plan_land], inside_ZXCQ_Cland_and_Pland, fms)
        print("Process: 将中心城区规划用地和现状保留用地合并")

        inside_ZXCQ_plan_land_over_sea = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_land_over_sea"
        arcpy.analysis.Clip(inside_ZXCQ_plan_land, sea_range, inside_ZXCQ_plan_land_over_sea)
        print("Process: 提取中心城区内规划用地中，海岸线外的部分")

        inside_ZXCQ_plan_land_in_landside = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_land_in_landside"
        arcpy.analysis.Erase(inside_ZXCQ_Cland_and_Pland, sea_range, inside_ZXCQ_plan_land_in_landside)
        print("Process: 提取中心城区内规划用地和现状用地中，海岸线内的部分")

        inside_ZXCQ_plan_sea_unrenew_part = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_sea_unrenew_part"
        arcpy.analysis.Erase(inside_ZXCQ_plan_sea, inside_ZXCQ_plan_land_over_sea, inside_ZXCQ_plan_sea_unrenew_part)
        print("Process: 中心城区规划用海中擦除用地方案中已规划海域")

        inside_ZXCQ_plan_sea_renew = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_sea_renew"
        arcpy.management.Merge([inside_ZXCQ_plan_sea_unrenew_part, inside_ZXCQ_plan_land_over_sea],
                               inside_ZXCQ_plan_sea_renew)
        print("Process: 更新中心城区规划用海")

        inside_ZXCQ_plan = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan"
        arcpy.management.Merge([inside_ZXCQ_plan_sea_renew, inside_ZXCQ_plan_land_in_landside], inside_ZXCQ_plan)
        print("Process: 组合中心城区海岸线内规划用地和规划用海")

        '''
        ————————————————替换道路部分————————————————
        '''

        inside_ZXCQ_plan_erase_road = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_except_plan_land_over_sea_erase_road"
        arcpy.analysis.Erase(inside_ZXCQ_plan, road, inside_ZXCQ_plan_erase_road)
        print("Process: 擦除合成的方案中的道路部分")

        inside_ZXCQ_plan_renew_road = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_renew_road"
        arcpy.management.Merge([inside_ZXCQ_plan_erase_road, inside_ZXCQ_plan_road], inside_ZXCQ_plan_renew_road)
        print("Process: 将道路合并入已经擦除道路部分的方案中")

        '''
        ————————————————整体替换部分————————————————
        '''

        inside_ZXCQ_plan_renew_road_unreplace_part = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_except_plan_land_over_sea_unreplace_part"
        arcpy.analysis.Erase(inside_ZXCQ_plan_renew_road, entirety_replace_part,
                             inside_ZXCQ_plan_renew_road_unreplace_part)
        print("Process: 擦除需要替换部分方案")

        replaced_plan = "C:\\TEMP_GDB.gdb\\replaced_plan"
        arcpy.management.Merge([inside_ZXCQ_plan_renew_road_unreplace_part, entirety_replace_part], replaced_plan)
        print("Process: 将需要替换的部分与其他部分合成完整方案")

        plan_by_zone = "C:\\TEMP_GDB.gdb\\plan_by_zone"
        arcpy.analysis.Identity(replaced_plan, zone, plan_by_zone)
        print("Process: 按照行政区标识方案")

        single_part_plan = os.path.join(output_path, "single_part_plan")
        arcpy.management.MultipartToSinglepart(plan_by_zone, single_part_plan)

        '''
        ————————————————字段整理部分————————————————
        '''

        traffic_codebook = """
def traffic(DM):
    if DM is None:
        return "1207"
    else:
        return DM
            """
        arcpy.management.CalculateField(single_part_plan, field="YDYHEJLDM", expression="traffic(!YDYHEJLDM!)",
                                        expression_type="PYTHON3", code_block=traffic_codebook)
        print("Process: 补充交通缺失字段")

        arcpy.management.AddField(single_part_plan, field_name="COLOR", field_type="TEXT", field_length=4)
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
        arcpy.management.CalculateField(single_part_plan, field="COLOR", expression="color(!YDYHEJLDM!)",
                                        expression_type="PYTHON3", code_block=color_codebook)
        print("Process: 补充上色字段(COLOR)")

        arcpy.management.AddField(single_part_plan, field_name="GHZT", field_type="TEXT", field_length=2)
        GHZT_codebook = """
def GHZT(dlmc):
    if dlmc is None:
        return "20"
    else:
        return "10"
        """
        arcpy.management.CalculateField(single_part_plan, field="GHZT", expression="GHZT(!地类名称!)",
                                        expression_type="PYTHON3", code_block=GHZT_codebook)
        print("Process: 补充规划状态字段(GHZT)")

        arcpy.management.AddField(single_part_plan, field_name="YDYHFLDM", field_type="TEXT", field_length=10)
        YDYHFLDM_codebook = """
def YDYHFLDM(ydyh2,ydyh3):
    if ydyh3 in ['100103','110103']:
        return ydyh3
    elif ydyh2[:2] in ['07','08','10','11','12','13','14']:
        return ydyh2
    else:
        return ydyh2[:2]
        """
        arcpy.management.CalculateField(single_part_plan, field="YDYHFLDM",
                                        expression="YDYHFLDM(!YDYHEJLDM!,!YDYHSJLDM!)",
                                        expression_type="PYTHON3", code_block=YDYHFLDM_codebook)
        print("Process: 补充用地用海分类代码字段(YDYHFLDM)")

        arcpy.management.CalculateField(single_part_plan, field="YSDM", expression="2090020620",
                                        expression_type="PYTHON3")
        arcpy.management.CalculateField(single_part_plan, field="XZQDM", expression="!XZQDM_1!",
                                        expression_type="PYTHON3")
        arcpy.management.CalculateField(single_part_plan, field="XZQMC", expression="!XZQMC_1!",
                                        expression_type="PYTHON3")

        # arcpy.management.CalculateGeometryAttributes(in_features=single_part_plan,
        #                                              geometry_property=[["MJ", "AREA_GEODESIC"]],
        #                                              area_unit= "SQUARE_METERS")
        # arcpy.management.CalculateField(single_part_plan, field="MJ", expression="round(!MJ!,2)",
        #                                 expression_type="PYTHON3")

        complete_plan = os.path.join(output_path, "complete_plan")
        arcpy.management.AddField(single_part_plan, field_name="YDYHFLMC", field_type="TEXT", field_length=50)
        arcpy.MakeFeatureLayer_management(single_part_plan, "plan_lyr")
        arcpy.JoinField_management("plan_lyr", "YDYHFLDM", dm2name_table, "dm")
        arcpy.management.CalculateField("plan_lyr", "YDYHEJLMC", "!name!", "PYTHON3")
        arcpy.CopyFeatures_management("plan_lyr", complete_plan)
        print("Process: 补充用地用海分类名称字段(YDYHFLMC)")

        arcpy.management.DeleteField(complete_plan,
                                     "FID_replaced_plan;GHFQDM;GHFQMC;GKYQ;YDYHYJLMC;YDYHEJLMC;YDYHSJLMC;区域;地类名称;面积;FID_B市辖区县级行政边界;BSM_1;YSDM_1;XZQDM_1;XZQMC_1;BZ_1;ORIG_FID;id;dm;name",
                                     "DELETE_FIELDS")

        arcpy.management.Delete(r"C:\TEMP_GDB.gdb", '')
        print("清除缓存")
