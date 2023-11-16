import arcpy

input_feature = r"C:\Users\Administrator\Documents\ArcGIS\Default.gdb\规划用地用海_Dissolv_MultipartToSi"

fields = [feild.name for feild in arcpy.ListFields(input_feature) if not feild.required]
print(fields)
czc_index = fields.index("CZCSX")
bz_index = fields.index("BZ")
feature_id = row[0]
feature_shape = row[1]

with arcpy.da.SearchCursor(input_feature, ["OID@", "SHAPE@"] + fields,
                           f"OID <> {feature_id} AND SHAPE.st_intersects({feature_shape})=1") as cursor:
    for row in cursor:
        print(row[czc_index + 2], row[bz_index + 2])
