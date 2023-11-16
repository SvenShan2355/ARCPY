import os

path = r'C:\Users\Administrator\Downloads\CNKI-20231027173149116.txt'

paper_list = []
paper = []

with open(path, 'r', encoding='utf-8') as f1:
    for line in f1:
        if line != '\n':
            paper.append(line)
        else:
            paper_list.append(paper)
            paper = []

for p in paper_list:
    k = '0'
    for i in p:
        if i[1] == k:
            1
    print(p)
