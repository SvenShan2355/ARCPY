# -*- coding: utf-8 -*-
"""
by Sven_SHAN  2022.11.07
"""
import os
import arcpy
from arcpy import analysis
from arcpy import management


def Model_For_Part_Entirety_Replace(bgdc, plan, sea, sea_range, road, range, entirety_replace_part, zone, czc, jsyd,
                                    kfbj, yjjbnt, stbhhx, dm2name_table, output_path, plan_across_shoreline=0):  # 模型
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
        ————————————————准备相关基础数据————————————————
        '''

        arcpy.management.CreateFileGDB("C:\\", "TEMP_GDB", "CURRENT")
        print("Process: 建立缓存空间")

        plan_E = "C:\\TEMP_GDB.gdb\\plan_E"
        arcpy.analysis.Erase(plan, yjjbnt, plan_E)
        plan_EE = "C:\\TEMP_GDB.gdb\\plan_EE"
        arcpy.analysis.Erase(plan_E, stbhhx, plan_EE)
        road_E = "C:\\TEMP_GDB.gdb\\road_E"
        arcpy.analysis.Erase(road, yjjbnt, road_E)
        road_EE = "C:\\TEMP_GDB.gdb\\road_EE"
        arcpy.analysis.Erase(road_E, stbhhx, road_EE)
        print("Process: 擦除永农和生态红线内规划")

        '''
        ————————————————合并用地方案部分————————————————
        '''

        inside_ZXCQ_current_land = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_current_land"
        arcpy.analysis.Clip(bgdc, range, inside_ZXCQ_current_land)
        print("Process1/28: 擦除中心城区范围外现状用地图斑")

        inside_ZXCQ_plan_sea = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_sea"
        arcpy.analysis.Clip(sea, range, inside_ZXCQ_plan_sea)
        print("Process2/28: 擦除中心城区范围外用海图斑")

        inside_ZXCQ_plan_land = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_land"
        arcpy.analysis.Clip(plan_EE, range, inside_ZXCQ_plan_land)
        print("Process3/28: 擦除中心城区范围外规划用地图斑")

        inside_ZXCQ_plan_road = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_road"
        arcpy.analysis.Clip(road_EE, range, inside_ZXCQ_plan_road)
        print("Process4/28: 擦除中心城区范围外规划道路图斑")

        inside_ZXCQ_unplanned_land = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_unplanned_land"
        arcpy.analysis.Erase(inside_ZXCQ_current_land, inside_ZXCQ_plan_land, inside_ZXCQ_unplanned_land)
        print("Process5/28: 中心城区范围内，提取保留现状部分图斑")

        inside_ZXCQ_Cland_and_Pland = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_Cland_and_Pland"
        # 维护合并字段
        # Create the required FieldMap and FieldMappings objects
        infile1 = inside_ZXCQ_unplanned_land
        infile2 = inside_ZXCQ_plan_land
        fm_YDYHYJLDM = arcpy.FieldMap()
        fm_YDYHEJLDM = arcpy.FieldMap()
        fm_YDYHSJLDM = arcpy.FieldMap()
        fm_YSDM = arcpy.FieldMap()
        fms = arcpy.FieldMappings()
        # Get the field names of vegetation type and diameter for both original
        infile1_YDYHYJLDM = 'YDYHYJLDM'
        infile1_YDYHEJLDM = 'YDYHEJLDM'
        infile1_YDYHSJLDM = 'YDYHSJLDM'
        infile1_YSDM = 'YSDM'
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
        fm_YSDM.addInputField(infile1, infile1_YSDM)
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
        YSDM = fm_YSDM.outputField
        YSDM.name = 'YSDM'
        YSDM.aliasName = 'YSDM'
        YSDM.length = 10
        fm_YSDM.outputField = YSDM
        # Add the FieldMap objects to the FieldMappings object
        fms.addFieldMap(fm_YDYHYJLDM)
        fms.addFieldMap(fm_YDYHEJLDM)
        fms.addFieldMap(fm_YDYHSJLDM)
        fms.addFieldMap(fm_YSDM)
        print("Process6/28: 维护合并字段")
        arcpy.management.Merge([inside_ZXCQ_unplanned_land, inside_ZXCQ_plan_land], inside_ZXCQ_Cland_and_Pland, fms)
        print("Process7/28: 将中心城区规划用地和现状保留用地合并")

        if plan_across_shoreline == 1:
            inside_ZXCQ_plan_land_over_sea = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_land_over_sea"
            arcpy.analysis.Clip(inside_ZXCQ_Cland_and_Pland, sea_range, inside_ZXCQ_plan_land_over_sea)
            inside_ZXCQ_plan_Pland_and_Cland_over_sea = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_Pland_and_Cland_over_sea"
            arcpy.analysis.Select(inside_ZXCQ_plan_land_over_sea, inside_ZXCQ_plan_Pland_and_Cland_over_sea,
                                  where_clause="YDYHYJLDM IN ('07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','24')")
            print("Process8/28: 提取中心城区内规划+现状用地海岸线外的建设用地部分")

            inside_ZXCQ_plan_land_in_landside = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_land_in_landside"
            arcpy.analysis.Erase(inside_ZXCQ_Cland_and_Pland, sea_range, inside_ZXCQ_plan_land_in_landside)
            print("Process9/28: 提取中心城区内规划用地和现状用地中，海岸线内的部分")

            inside_ZXCQ_plan_sea_unrenew_part = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_sea_unrenew_part"
            arcpy.analysis.Erase(inside_ZXCQ_plan_sea, inside_ZXCQ_plan_Pland_and_Cland_over_sea,
                                 inside_ZXCQ_plan_sea_unrenew_part)
            print("Process10/28: 中心城区规划用海中擦除用地方案中已规划海域")

            inside_ZXCQ_plan_sea_renew = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_sea_renew"
            arcpy.management.Merge([inside_ZXCQ_plan_sea_unrenew_part, inside_ZXCQ_plan_Pland_and_Cland_over_sea],
                                   inside_ZXCQ_plan_sea_renew)
            print("Process11/28: 更新中心城区规划用海")

            inside_ZXCQ_plan = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan"
            arcpy.management.Merge([inside_ZXCQ_plan_sea_renew, inside_ZXCQ_plan_land_in_landside], inside_ZXCQ_plan)
            print("Process12/28: 组合中心城区海岸线内规划用地和规划用海")

        elif plan_across_shoreline == 0:
            inside_ZXCQ_plan_land_over_sea = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_land_over_sea"
            arcpy.analysis.Clip(inside_ZXCQ_plan_land, sea_range, inside_ZXCQ_plan_land_over_sea)
            print("Process8/28: 提取中心城区内规划用地中，海岸线外的部分")

            inside_ZXCQ_plan_sea_over_sea = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_sea_over_sea"
            arcpy.analysis.Select(inside_ZXCQ_plan_land_over_sea, inside_ZXCQ_plan_sea_over_sea,
                                  where_clause="YDYHYJLDM IN ('18','19','20','21','22','24')")
            print("Process8/28: 提取中心城区内规划用地中，海岸线外的用海")

            inside_ZXCQ_plan_land_in_landside = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_land_in_landside"
            arcpy.analysis.Erase(inside_ZXCQ_Cland_and_Pland, sea_range, inside_ZXCQ_plan_land_in_landside)
            print("Process9/28: 提取中心城区内规划用地和现状用地中，海岸线内的部分")

            inside_ZXCQ_plan_sea_unrenew_part = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_sea_unrenew_part"
            arcpy.analysis.Erase(inside_ZXCQ_plan_sea, inside_ZXCQ_plan_sea_over_sea,
                                 inside_ZXCQ_plan_sea_unrenew_part)
            print("Process10/28: 中心城区规划用海中擦除用地方案中已规划海域")

            inside_ZXCQ_plan_sea_renew = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_sea_renew"
            arcpy.management.Merge([inside_ZXCQ_plan_sea_unrenew_part, inside_ZXCQ_plan_sea_over_sea],
                                   inside_ZXCQ_plan_sea_renew)
            print("Process11/28: 更新中心城区规划用海")

            inside_ZXCQ_plan = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan"
            arcpy.management.Merge([inside_ZXCQ_plan_sea_renew, inside_ZXCQ_plan_land_in_landside], inside_ZXCQ_plan)
            print("Process12/28: 组合中心城区海岸线内规划用地和规划用海")

        '''
        ————————————————替换道路部分————————————————
        '''

        inside_ZXCQ_plan_erase_road = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_except_plan_land_over_sea_erase_road"
        arcpy.analysis.Erase(inside_ZXCQ_plan, road_EE, inside_ZXCQ_plan_erase_road)
        print("Process13/28: 擦除合成的方案中的道路部分")

        inside_ZXCQ_plan_renew_road = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_renew_road"
        arcpy.management.Merge([inside_ZXCQ_plan_erase_road, inside_ZXCQ_plan_road], inside_ZXCQ_plan_renew_road)
        print("Process14/28: 将道路合并入已经擦除道路部分的方案中")

        '''
        ————————————————整体替换部分————————————————
        '''
        if entirety_replace_part != "":
            inside_ZXCQ_plan_renew_road_unreplace_part = "C:\\TEMP_GDB.gdb\\inside_ZXCQ_plan_except_plan_land_over_sea_unreplace_part"
            arcpy.analysis.Erase(inside_ZXCQ_plan_renew_road, entirety_replace_part,
                                 inside_ZXCQ_plan_renew_road_unreplace_part)
            print("Process15/28: 擦除需要替换部分方案")

            replaced_plan = "C:\\TEMP_GDB.gdb\\replaced_plan"
            arcpy.management.Merge([inside_ZXCQ_plan_renew_road_unreplace_part, entirety_replace_part], replaced_plan)
            print("Process16/28: 将需要替换的部分与其他部分合成完整方案")

            plan_by_zone = "C:\\TEMP_GDB.gdb\\plan_by_zone"
            arcpy.analysis.Identity(replaced_plan, zone, plan_by_zone)
            print("Process17/28: 按照行政区标识方案")
        else:
            plan_by_zone = "C:\\TEMP_GDB.gdb\\plan_by_zone"
            arcpy.analysis.Identity(inside_ZXCQ_plan_renew_road, zone, plan_by_zone)
            print("Process17/28: 按照行政区标识方案")

        '''
        ————————————————标识部分————————————————
        '''

        plan_by_czc = "C:\\TEMP_GDB.gdb\\plan_by_czc"
        arcpy.analysis.Identity(plan_by_zone, czc, plan_by_czc)
        print("Process18/28: 按照城镇村标识方案")

        plan_by_kfbj = "C:\\TEMP_GDB.gdb\\plan_by_kfbj"
        arcpy.analysis.Identity(plan_by_czc, kfbj, plan_by_kfbj)
        print("Process19/28: 按照开发边界标识方案")

        plan_by_jsyd = "C:\\TEMP_GDB.gdb\\plan_by_jsyd"
        arcpy.analysis.Identity(plan_by_kfbj, jsyd, plan_by_jsyd)

        single_part_plan = os.path.join(output_path, "single_part_plan")
        arcpy.management.MultipartToSinglepart(plan_by_jsyd, single_part_plan)

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
        print("Process20/28: 补充交通缺失字段")

        if plan_across_shoreline == 1:
            check_used_land_codebook = """
def check_used_land(jsyd,ydyhfldm):
    if jsyd == 1 and ydyhfldm[:2] not in ['07','08','09','10','11','12','13','14','15','16']:
        return "16"
    else:
        return ydyhfldm
                    """
            arcpy.management.CalculateField(single_part_plan, field="YDYHEJLDM",
                                            expression="check_used_land(!jsyd!,!YDYHEJLDM!)",
                                            expression_type="PYTHON3",
                                            code_block=check_used_land_codebook
                                            )
        elif plan_across_shoreline == 0:
            check_used_land_codebook = """
def check_used_land(jsyd,ydyhfldm):
    if jsyd == 1 and ydyhfldm[:2] not in ['07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','24']:
        return "16"
    else:
        return ydyhfldm
                    """
            arcpy.management.CalculateField(single_part_plan, field="YDYHEJLDM",
                                            expression="check_used_land(!jsyd!,!YDYHEJLDM!)",
                                            expression_type="PYTHON3",
                                            code_block=check_used_land_codebook
                                            )

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
        print("Process21/28: 补充上色字段(COLOR)")

        arcpy.management.AddField(single_part_plan, field_name="GHZT", field_type="TEXT", field_length=2)
        GHZT_codebook = """
def GHZT(ysdm, jsyd): # 通过用于替换的现状要素图层的图层要素代码确认是否是现状用地
    if ysdm == "2090010100" or jsyd == 1:
        return "10"
    else:
        return "20"
        """
        arcpy.management.CalculateField(single_part_plan, field="GHZT", expression="GHZT(!YSDM!,!jsyd!)",
                                        expression_type="PYTHON3", code_block=GHZT_codebook)
        print("Process22/28: 补充规划状态字段(GHZT)")

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
        print("Process23/28: 补充用地用海分类代码字段(YDYHFLDM)")

        arcpy.management.CalculateField(single_part_plan, field="YSDM", expression="2090050245",
                                        expression_type="PYTHON3")
        xzqdm_codebook = """
def xzqdm(xzqdm):
    if xzqdm == "":
        return '440800'
    else:
        return xzqdm        
        """
        arcpy.management.CalculateField(single_part_plan, field="XZQDM", expression="xzqdm(!XZQDM!)",
                                        expression_type="PYTHON3", code_block=xzqdm_codebook)

        xzqmc_codebook = """
def xzqmc(xzqmc):
    if xzqmc == "":
        return '湛江市'
    else:
        return xzqmc        
        """
        arcpy.management.CalculateField(single_part_plan, field="XZQMC", expression="xzqmc(!XZQMC!)",
                                        expression_type="PYTHON3", code_block=xzqmc_codebook)
        print("Process24/28: 补充行政区相关字段")

        # arcpy.management.CalculateGeometryAttributes(in_features=single_part_plan,
        #                                              geometry_property=[["MJ", "AREA_GEODESIC"]],
        #                                              area_unit= "SQUARE_METERS")
        # arcpy.management.CalculateField(single_part_plan, field="MJ", expression="round(!MJ!,2)",
        #                                 expression_type="PYTHON3")

        YD1004_codebook = """
def NI_codebook(ydyh):
    if ydyh in ['1004']:
        return "规划新型产业用地，由于缺少对应代码，按照一类工业用地100101表示"
    else:
        return ""
        """
        arcpy.management.CalculateField(single_part_plan, field="BZ", expression="NI_codebook(!YDYHFLDM!)",
                                        expression_type="PYTHON3", code_block=YD1004_codebook)

        YD1004reset_codebook = """
def NIR_codebook(ydyh):
    if ydyh in ['1004']:
        return "100101"
    else:
        return ydyh
        """
        arcpy.management.CalculateField(single_part_plan, field="YDYHFLDM", expression="NIR_codebook(!YDYHFLDM!)",
                                        expression_type="PYTHON3", code_block=YD1004reset_codebook)
        print("Process25/28: 备注新型产业用地")

        czc_codebook = """
def czc(czcsx,ydyh,kfbj):
    if kfbj == 1:
        if ydyh[:2] in ['07','08','09','10','11','12','13','14','16'] and ydyh not in ['0703','1002','1003']:
            return '10'
        elif ydyh[:2] == '15' or ydyh in ['1002','1003']:
            return  '特殊'
        elif czcsx in ['20']:
            return '20'
        elif ydyh == '0703':
            return '10'
        else:
            return ''
    else:
        if czcsx == '20':
            return '20'
        elif ydyh[:2] == '15' or ydyh in ['1002','1003']:
            return '特殊'
        elif ydyh[:2] in ['07','08','09','10','11','13','14','16'] and ydyh not in ['1002','1003']:
            return '10'
        elif ydyh[:2] == '12':
            return '区域'
        else:
            return ''
        """
        arcpy.management.CalculateField(single_part_plan, field="CZCSX", expression="czc(!CZCSX1!,!YDYHFLDM!,!kfbj!)",
                                        expression_type="PYTHON3",
                                        code_block=czc_codebook)
        print("Process26/28: 补充城镇村属性码(CZCSX)")

        complete_plan = os.path.join(output_path, "complete_plan")
        arcpy.management.AddField(single_part_plan, field_name="YDYHFLMC", field_type="TEXT", field_length=50)
        arcpy.MakeFeatureLayer_management(single_part_plan, "plan_lyr")
        arcpy.JoinField_management("plan_lyr", "YDYHFLDM", dm2name_table, "dm")
        arcpy.management.CalculateField("plan_lyr", "YDYHFLMC", "!name!", "PYTHON3")
        arcpy.CopyFeatures_management("plan_lyr", complete_plan)

        arcpy.management.CalculateField(complete_plan, field="YDYHFLDM", expression="!YDYHFLDM!.ljust(6,'0')",
                                        expression_type="PYTHON3")
        print("Process28/28: 补充用地用海分类名称字段(YDYHFLMC)")

        arcpy.management.DeleteField(complete_plan,
                                     "FID_plan_by_kfbj;FID_plan_by_czc;FID_plan_by_zone;FID_inside_ZXCQ_plan_renew_road;ZONE;MERGE_SRC;FID_B市辖区县级行政边界;FID_变更调查2020乡村建设用地203;FID_封库城镇开发边界;FID_变更调查2020建设用地;ORIG_FID;id;dm;name;YSDM_1",
                                     "DELETE_FIELDS")
        print("Process28/28: 清除多余字段")

        arcpy.management.Delete(r"C:\TEMP_GDB.gdb", '')
        print("Process: 清除缓存")
