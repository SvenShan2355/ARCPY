import pandas as pd
import numpy as np
import scipy

csv_path = r'C:\Users\Administrator\Desktop\hatches_Dissolve_Identity_TableToExcel.csv'


# 读取街道信息
def read_csv(csv_path):
    blocks_list = []
    blocks_dict = {}
    reader = pd.read_csv(csv_path)
    blocks_in_range = reader.dropna(axis=0, how='any')

    for index2 in blocks_in_range.index:
        if blocks_in_range.loc[index2].values[1] in blocks_dict.keys():
            blocks_dict[blocks_in_range.loc[index2].values[1]].append(blocks_in_range.loc[index2].values[3])
            # print(1)
        else:
            blocks_dict[blocks_in_range.loc[index2].values[1]] = [blocks_in_range.loc[index2].values[3], ]
            # print(0)
    id = 0
    blocks_id_dict = {}
    for key in blocks_dict.keys():
        blocks_id_dict[id] = key
        id += 1

    return blocks_id_dict, blocks_dict


# 形成街区共街道矩阵
def count_same_street(blocks_id_dict, blocks_dict):
    i = 0
    matrix = []

    for block_key1 in blocks_id_dict.keys():
        matrix.append([])
        if blocks_id_dict[block_key1] in blocks_dict.keys():
            set1 = set(blocks_dict[blocks_id_dict[block_key1]])
            for block_key2 in blocks_id_dict.keys():
                if blocks_id_dict[block_key2] in blocks_dict.keys():
                    set2 = set(blocks_dict[blocks_id_dict[block_key2]])
                    if block_key1 != block_key2:
                        matrix[i].append(len(set1 & set2))
                    else:
                        matrix[i].append(0)
                else:
                    matrix[i].append(0)
        else:
            matrix[i] = ([0] * len(blocks_id_dict))
        i += 1
    return matrix


# 形成新的街区数据集
def refresh_blocks_dict(block_dict, street_matrix, blocks_id_dict):
    n_matrix = np.array(street_matrix)
    tri_matrix = np.triu(n_matrix)
    max = tri_matrix.max()
    print(f'max is {max}')
    linked_block = []
    combine_blocks_groups = []
    row, column = np.where(tri_matrix == max)
    # 形成可以合并的街区组
    for i in range(len(row)):
        if blocks_id_dict[row[i]] not in linked_block and blocks_id_dict[column[i]] not in linked_block:
            combine_blocks_groups.append([blocks_id_dict[row[i]], blocks_id_dict[column[i]]])

        else:
            count = []
            for combine_blocks_group_index in range(len(combine_blocks_groups)):

                if blocks_id_dict[row[i]] in combine_blocks_groups[combine_blocks_group_index]:
                    combine_blocks_groups[combine_blocks_group_index].append(blocks_id_dict[column[i]])
                    combine_blocks_groups[combine_blocks_group_index] = list(
                        set(combine_blocks_groups[combine_blocks_group_index]))
                    count.append(combine_blocks_group_index)

                elif blocks_id_dict[column[i]] in combine_blocks_groups[combine_blocks_group_index]:
                    combine_blocks_groups[combine_blocks_group_index].append(blocks_id_dict[row[i]])
                    combine_blocks_groups[combine_blocks_group_index] = list(
                        set(combine_blocks_groups[combine_blocks_group_index]))
                    count.append(combine_blocks_group_index)

            if len(count) > 1:
                # print(f'count:{count}')
                new_group = list(set(combine_blocks_groups.pop(count[1]) + combine_blocks_groups.pop(count[0])))
                combine_blocks_groups.append(new_group)

        linked_block += [blocks_id_dict[row[i]], blocks_id_dict[column[i]]]
        # print(f' combine_blocks_groups  is {combine_blocks_groups}')

    # 合并街区并更新街区表
    for combine_blocks_group in combine_blocks_groups:
        new_name = ''
        street_list = []
        # print(f'combine_blocks_group is {combine_blocks_group}')
        for combine_block in combine_blocks_group:
            street_list = street_list + blocks_dict.pop(combine_block)
            new_name = str(new_name + str(combine_block) + '+')
        new_name = new_name[:-1]
        blocks_dict[new_name] = list(set(street_list))
        # print(new_name, blocks_dict[new_name])

    id = 0
    new_blocks_id_dict = {}
    for key in blocks_dict.keys():
        new_blocks_id_dict[id] = key
        id += 1

    return blocks_dict, new_blocks_id_dict


blocks_id_dict, blocks_dict = read_csv(csv_path)
matrix = count_same_street(blocks_id_dict, blocks_dict)
# blocks_dict, blocks_id_dict = refresh_blocks_dict(blocks_dict, matrix, blocks_id_dict)

while len(blocks_dict) > 30:
    blocks_dict, blocks_id_dict = refresh_blocks_dict(blocks_dict, matrix, blocks_id_dict)
    # for key1 in blocks_dict.keys():
    #     print(f'{key1} contain {blocks_dict[key1]}')
    print(len(blocks_dict))
    # for key2 in blocks_id_dict.keys():
    #     print(f'{key2} means {blocks_id_dict[key2]}')
    matrix = count_same_street(blocks_id_dict, blocks_dict)

for key1 in blocks_dict.keys():
    print(f'{key1} contain {blocks_dict[key1]}')

