# -*- coding: utf-8 -*-

import scipy.cluster.hierarchy as hcluster
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import csv

mpl.rcParams['font.sans-serif'] = ['SimHei']
df = pd.read_csv(r'C:\Users\Administrator\Desktop\geoinfo.csv', header=0, index_col=0)
data_dic = list(df.itertuples())
print(data_dic)
for point in data_dic:
    name,x,y = point
    plt.scatter(x,y)
    plt.text(x,y,name,fontdict={"size":4})
    plt.axis('equal')
plt.show()
# df.values[:, :] = df.values[:, :].astype(float)
# plt.scatter(x=list[:, 1:2], y=list[:, 0:1], marker='.')
#
# # disMat = hcluster.distance.pdist(X=df[['x', 'y']], metric='euclidean')
# # Z = hcluster.linkage(disMat,method='single')
# # P = hcluster.dendrogram(Z)
# plt.show()


# data = pd.read_csv(r"G:\ARCPY\arcpy_learning\信息收集\cost_Matrix.csv", header=0, index_col=0)
# matrix = data.values

# linkage = hcluster.linkage(matrix, method='single')
# print(linkage)
# p = hcluster.dendrogram(linkage, leaf_font_size=10.)
