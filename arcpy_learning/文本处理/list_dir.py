import os
import shutil
path = r'C:\Users\Administrator\Desktop\关于《徐闻县国土空间总体规划（2021-2035年）》草案的征求意见复函\无建议或意见的单位\乡镇街道'

list1 = os.listdir(path)

for i in list1:
    print(i[1:].split('）')[0])
