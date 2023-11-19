import arcpy
import time
import os

# arcpy.env.workspace = r"C:\Users\Administrator\Desktop\测试数据.gdb"
# arcpy.env.overwriteOutput = True
# input_feature = "GH"
# input_lyr = arcpy.MakeFeatureLayer_management(input_feature, "input_lyr")
# intersect_lyr = arcpy.MakeFeatureLayer_management(input_feature, "intersect_lyr")
# print("start")
# with arcpy.da.SearchCursor(input_lyr, ["OID@", "SHAPE@"]) as cursor:
#     for row in cursor:
#         feature_shape = row[1]
#         feature_id = row[0]
#         feature_area = feature_shape.getArea("GEODESIC")
#         if feature_area > 500:  # 筛选面积大于500的要素
#             st = time.process_time()
#             arcpy.SelectLayerByLocation_management(intersect_lyr, 'intersect', feature_shape)
#             with arcpy.da.SearchCursor(intersect_lyr, ["OID@", "SHAPE@"]) as sub_cursor:  # 选取与该要素相邻的要素
#                 for sub_row in sub_cursor:
#                     sub_feature_id = sub_row[0]  # 输出相邻要素id
#                     if feature_id != sub_feature_id:
#                         print(sub_feature_id)
#             arcpy.SelectLayerByAttribute_management(intersect_lyr, "CLEAR_SELECTION")
#             et = time.process_time()
#             res = et - st
#             print(res)
#             print("end sub_feature_id")
#             print("stop")

import arcpy
import datetime

# Create an insert cursor for a table specifying the fields that will
# have values provided
fields = ['rowid', 'distance', 'CFCC', 'DateInsp']

with arcpy.da.InsertCursor(r"C:\Users\Administrator\Desktop\测试数据.gdb\GHYDYH_E", fields) as cursor:
    # Create 25 new rows. Set default values on distance and CFCC code
    for x in range(0, 25):
        cursor.insertRow((x, 100, 'A10', datetime.datetime.now()))
