# -*- coding: utf-8 -*-
"""
by Sven_SHAN  2022.7.25
"""
import os
import arcpy
from arcpy import analysis
from arcpy import management
from arcpy import ddd
from arcpy import stats
from arcpy import conversion
from arcpy import gapro


def Model(input_feature_path, output_path, number_of_clusters=0, max_edge_length=100, Delineate_method='PERIMETER_ONLY'):  # 模型
    '''
    参数（需要聚合的面要素, 输出目录, 聚类数量[默认2-30], 最长连接距离[默认100], 修剪方式['PERIMETER_ONLY','ALL']）
    '''


    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = False
    arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")

    # 环境设置
    with arcpy.EnvManager(
            cartographicCoordinateSystem="PROJCS[\"CGCS2000_3_Degree_GK_Zone_37\",GEOGCS[\"GCS_China_Geodetic_Coordinate_System_2000\",DATUM[\"D_China_2000\",SPHEROID[\"CGCS2000\",6378137.0,298.257222101]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]],PROJECTION[\"Gauss_Kruger\"],PARAMETER[\"False_Easting\",37500000.0],PARAMETER[\"False_Northing\",0.0],PARAMETER[\"Central_Meridian\",111.0],PARAMETER[\"Scale_Factor\",1.0],PARAMETER[\"Latitude_Of_Origin\",0.0],UNIT[\"Meter\",1.0]]",
            scratchWorkspace=r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb",
            workspace=r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb"):

        # 建立缓存空间
        temp_folder = r'C:\temp_folder'
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
        arcpy.management.CreateFileGDB(temp_folder, "TEMP_GDB", "CURRENT")
        temp_gdb = os.path.join(temp_folder, "TEMP_GDB.gdb")
        print('建立缓存空间')

        # 复制输入要素
        arcpy.conversion.FeatureClassToFeatureClass(input_feature_path, temp_gdb, 'input_feature_surface')
        input_feature_surface = os.path.join(temp_gdb, 'input_feature_surface')
        print('复制输入要素')

        # 要素聚类
        Clustered_surface = os.path.join(temp_gdb, 'Clustered_surface')

        arcpy.management.CalculateGeometryAttributes(input_feature_surface, [['x_co', 'CENTROID_X'], ['y_co', 'CENTROID_Y']], length_unit='METERS')

        if number_of_clusters == 0:
            arcpy.stats.MultivariateClustering(input_feature_surface, Clustered_surface, analysis_fields=['x_co', 'y_co'], clustering_method='K_MEANS')
        else:
            arcpy.stats.MultivariateClustering(input_feature_surface, Clustered_surface, analysis_fields=['x_co', 'y_co'], clustering_method='K_MEANS', number_of_clusters=number_of_clusters)

        Clustered_surface_z = os.path.join(temp_gdb, 'Clustered_surface_z')
        arcpy.gapro.CalculateField(Clustered_surface, Clustered_surface_z, field_to_calculate='NEW_FIELD', field_name='z_co', field_type='DOUBLE', expression=0)

        point_set = os.path.join(temp_gdb, 'point_set_ALL')
        arcpy.management.FeatureVerticesToPoints(Clustered_surface_z, point_set, point_location='ALL')

        arcpy.analysis.Statistics(Clustered_surface, os.path.join(temp_gdb, 'max_cluster'), statistics_fields=[['CLUSTER_ID','MAX']])
        cursor = arcpy.SearchCursor(os.path.join(temp_gdb, 'max_cluster'))
        cluster_num = 0
        for row in cursor:
            cluster_num = row.getValue('MAX_CLUSTER_ID')
        print('要素聚类')


        # 通过创建TIN及连接筛选生成多块包络线
        for i in range(int(cluster_num)):
            j=i+1

            point_set_name = 'point_set'+str(j)
            Selected_point = os.path.join(temp_gdb, point_set_name)
            arcpy.analysis.Select(in_features=point_set, out_feature_class=Selected_point,
                                  where_clause="CLUSTER_ID = {}".format(j))

            TIN_path = os.path.join(temp_folder, 'TIN{}'.format(j))
            arcpy.ddd.CreateTin(TIN_path,
                                'PROJCS["CGCS2000_3_Degree_GK_Zone_37",GEOGCS["GCS_China_Geodetic_Coordinate_System_2000",DATUM["D_China_2000",SPHEROID["CGCS2000",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",37500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",111.0],PARAMETER["Scale_Factor",1.0],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]',
                                "{} 'z_co' Mass_Points <None>".format(Selected_point), "DELAUNAY")

            arcpy.ddd.DelineateTinDataArea(TIN_path, max_edge_length, method=Delineate_method)
            out_feature = os.path.join(temp_gdb, 'surface{}'.format(j))
            arcpy.ddd.TinDomain(TIN_path, out_feature_class=out_feature, out_geometry_type='POLYGON')
            print('包络线TIN{}'.format(j))


        # 块包络线融合
        input_list = []
        for k in range(int(cluster_num)):
            l = k+1
            input_list.append(os.path.join(temp_gdb,'surface{}'.format(l)))
        merge_output = os.path.join(temp_gdb, 'Merge_output')
        arcpy.management.Merge(input_list, merge_output)
        arcpy.management.Dissolve(merge_output, os.path.join(output_path, 'Envelope'))
        print('块包络线融合')

        os.remove(temp_folder)
        print('清除缓存')

        print('完成')

if __name__ == '__main__':

    Model(r"E:\DataBase_本地更新库\ZJ\开发边界外管控论文\开发边界外管控论文.gdb\麻章区稳定耕地",
          r"E:\DataBase_本地更新库\ZJ\开发边界外管控论文\开发边界外管控论文.gdb")