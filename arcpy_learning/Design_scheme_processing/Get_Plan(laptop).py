from Design_scheme_processing.method import Merge_Plan
from Design_scheme_processing.method import Offset_Centerline_of_Road

if __name__ == '__main__':
    # 从中心线生成路网
    Offset_Centerline_of_Road.Model(
        r"D:\地理数据库——0116\DataBase_本地更新库\湛江市国土空间规划0114\Database\中心城区方案.gdb\赤霞坡路网中心线20230215",
        r"D:\地理数据库——0116\DataBase_本地更新库\湛江市国土空间规划0114\Database\中心城区方案.gdb\立交节点1112",
        r"D:\地理数据库——0116\DataBase_本地更新库\湛江市国土空间规划0114\Output_Database.gdb", "HCJL", "DJJL")

    # 合成方案
    Merge_Plan.Model_For_Part_Entirety_Replace(
        r"D:\地理数据库——0116\DataBase_共享总库\ZJ\06_现状细化数据\中心城区\2022.07.11现状图\001库\市辖区现状图.gdb\A变更调查2020海岸线内部分",
        r"D:\地理数据库——0116\DataBase_本地更新库\湛江市国土空间规划0114\Database\中心城区方案.gdb\B赤霞坡方案20230215_到中心线",
        r"D:\地理数据库——0116\DataBase_共享总库\ZJ\05_各种规划\湛江市海洋分区规划成果20221111.gdb\用海分区",
        r"D:\地理数据库——0116\DataBase_本地更新库\湛江市国土空间规划0114\湛江市国土空间规划.gdb\E海域范围新",
        r"D:\地理数据库——0116\DataBase_本地更新库\湛江市国土空间规划0114\Output_Database.gdb\output_roads_d",
        r"D:\地理数据库——0116\DataBase_本地更新库\湛江市国土空间规划0114\Database\中心城区方案.gdb\中心城区范围线20221118",
        r"D:\地理数据库——0116\DataBase_本地更新库\湛江市国土空间规划0114\Database\中心城区方案.gdb\麻章方案20230221",
        r"D:\地理数据库——0116\DataBase_本地更新库\湛江市国土空间规划0114\Output_Database.gdb")

    # 拆分数据库