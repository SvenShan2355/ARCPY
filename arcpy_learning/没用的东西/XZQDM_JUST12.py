# -*- coding: utf-8 -*-

import os
import arcpy.management

arcpy.env.workspace = r'E:\DataBase_共享总库\ZJ\14_成果数据库\县级数据库质检\5.1\光明区\440311光明区县级国土空间总体规划矢量数据.gdb'
datasets = arcpy.ListDatasets(feature_type='feature')
datasets = [''] + datasets if datasets is not None else []
for ds in datasets:
    for fc in arcpy.ListFeatureClasses(feature_dataset=ds):
        path = os.path.join(arcpy.env.workspace, ds, fc)
        field_names = [f.name for f in arcpy.ListFields(path)]
        if 'XZQDM' in field_names:
            arcpy.management.CalculateField(path, field="XZQDM", expression="!XZQDM!.ljust(12,'0')",
                                            expression_type="PYTHON3")
            print('{} done'.format(fc))
        else:
            print('{} without XZQDM'.format(fc))
