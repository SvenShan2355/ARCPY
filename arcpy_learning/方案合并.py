# -*- coding: utf-8 -*-
"""
by Sven_SHAN  2022.11.07
"""
import os
import arcpy
from arcpy import analysis
from arcpy import management


def Model(bgdc, plan, sea, road, range, output_path):  # 模型
    '''
    参数（现状图层, 方案图层, 用海图层, 路网图层, 中心城区范围图层, 输出目录）
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

        clip2="C:\\TEMP_GDB.gdb\\clip2"
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

        merge2 = "C:\\TEMP_GDB.gdb\\merge2"
        arcpy.management.Merge([merge1, sea], merge2)

        erase2 = "C:\\TEMP_GDB.gdb\\erase2"
        arcpy.analysis.Erase(merge2, road, erase2)
        print("Process: 擦除道路")

        merge3 = "C:\\TEMP_GDB.gdb\\merge3"
        arcpy.management.Merge([erase2, road], merge3)
        print("Process: 合并道路")

        output_name = os.path.join(output_path, "merged_plan")
        arcpy.analysis.Clip(merge3, range, output_name)
        print("Process: 擦除方案范围外图斑")

        arcpy.management.AddField(output_name, field_name="着色", field_type="TEXT", field_length=4)

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

        arcpy.management.CalculateField(output_name, field="着色", expression="color(!YDYHEJLDM!)",
                                        expression_type="PYTHON3", code_block=color_codebook)

        arcpy.management.Delete(r"C:\TEMP_GDB.gdb", '')
        print("清除缓存")


if __name__ == '__main__':
    Model(r"E:\DataBase_共享总库\ZJ\06_现状细化数据\中心城区\2022.07.11现状图\001库\市辖区现状图.gdb\A变更调查2020海岸线内部分",
          r"E:\DataBase_本地更新库\湛江市国土空间规划1103\Database\中心城区方案.gdb\B中心城区方案20221116_到中心线",
          r"E:\DataBase_共享总库\ZJ\05_各种规划\湛江市海洋分区规划成果20221111.gdb\用海分区",
          r"E:\DataBase_本地更新库\湛江市国土空间规划1103\Output_Database.gdb\output_roads",
          r"E:\DataBase_本地更新库\湛江市国土空间规划1103\Database\中心城区方案.gdb\中心城区范围线20221113",
          r"E:\DataBase_本地更新库\湛江市国土空间规划1103\Output_Database.gdb")
