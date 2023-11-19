from Design_scheme_processing.method import Merge_Plan
from Design_scheme_processing.method import Offset_Centerline_of_Road
from Design_scheme_processing.method import eliminate_under_200

if __name__ == '__main__':
    # 从中心线生成路网
    # Offset_Centerline_of_Road.Model_I(
    #     r"D:\DataBase_本地更新库\湛江市国土空间规划\Database\中心城区方案.gdb\中心城区道路中心线20230508",
    #     r"D:\DataBase_本地更新库\湛江市国土空间规划\Database\中心城区方案.gdb\立交节点0307",
    #     r"D:\DataBase_本地更新库\湛江市国土空间规划\Output_Database.gdb", "HCJL", "DJJL")

    # 合成方案
    # Merge_Plan.Model_For_Part_Entirety_Replace(
    #     bgdc=r"D:\DataBase_本地更新库\湛江市国土空间规划\湛江市国土空间规划.gdb\入库版现状20230419",
    #     plan=r"D:\DataBase_本地更新库\湛江市国土空间规划\Database\中心城区方案.gdb\中心城区方案到中心线20230601",
    #     sea=r"D:\DataBase_本地更新库\湛江市国土空间规划\湛江市国土空间规划.gdb\中心城区海域分区20230424_按林科要求修改",
    #     sea_range=r"D:\DataBase_本地更新库\湛江市国土空间规划\湛江市国土空间规划.gdb\E海域范围_大陆海岛修测岸线",
    #     road=r"D:\DataBase_本地更新库\湛江市国土空间规划\Output_Database.gdb\output_roads_20230616",
    #     range=r"D:\DataBase_本地更新库\湛江市国土空间规划\Database\中心城区方案.gdb\中心城区范围线20230601_县级库",
    #     entirety_replace_part=r"D:\DataBase_本地更新库\湛江市国土空间规划\Database\中心城区方案.gdb\PTMZ用地方案20230612",
    #     zone=r"D:\DataBase_共享总库\ZJ\0_基础数据总库\湛江市国土空间总体规划.gdb\B市辖区县级行政边界",
    #     czc=r"D:\DataBase_本地更新库\湛江市国土空间规划\湛江市国土空间规划.gdb\变更调查2020乡村建设用地203",
    #     jsyd=r'D:\DataBase_本地更新库\湛江市国土空间规划\湛江市国土空间规划.gdb\变更调查2020建设用地',
    #     kfbj=r"D:\DataBase_本地更新库\湛江市国土空间规划\湛江市国土空间规划.gdb\封库城镇开发边界",
    #     yjjbnt=r'D:\DataBase_共享总库\ZJ\04_三区三线试划\成果_20221110-广东省“三区三线”划定成果矢量数据（部下发封库版）\三区三线下发版.gdb\永久基本农田',
    #     stbhhx=r'D:\DataBase_共享总库\ZJ\04_三区三线试划\成果_20221110-广东省“三区三线”划定成果矢量数据（部下发封库版）\三区三线下发版.gdb\陆域生态保护红线',
    #     dm2name_table=r"D:\DataBase_本地更新库\湛江市国土空间规划\湛江市国土空间规划.gdb\dm2name_",
    #     output_path=r"D:\DataBase_本地更新库\湛江市国土空间规划\Output_Database.gdb",
    #     plan_across_shoreline=1,
    #     plan_across_kfbj=1
    # )

    # 入库处理
    # eliminate_under_200.eliminate_under_200(input_file=r'D:\DataBase_本地更新库\湛江市国土空间规划\Output_Database.gdb\complete_plan_20230607',
    #                                         styn=r'D:\DataBase_共享总库\ZJ\04_三区三线试划\成果_20221110-广东省“三区三线”划定成果矢量数据（部下发封库版）\三区三线下发版.gdb\STBHYN_d',
    #                                         output_file=r'D:\DataBase_本地更新库\湛江市国土空间规划\Output_Database.gdb\complete_plan_20230607_E',
    #                                         jsyd=r'D:\DataBase_本地更新库\湛江市国土空间规划\湛江市国土空间规划.gdb\变更调查2020建设用地')
    eliminate_under_200.check_by_cursor(input_feature=r"C:\Users\Administrator\Desktop\测试数据.gdb\规划用地用海",
                                        output_path=r"C:\Users\Administrator\Desktop\测试数据.gdb",
                                        output_feature_name="GHYDYH_E")

    '''
    执行完成后需要的步骤：
    1 消除碎图斑
    2 重新计算面积和标识码

    '''
