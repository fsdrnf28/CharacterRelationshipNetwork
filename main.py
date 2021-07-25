# -*- coding: utf-8 -*-
import os,sys
import jieba,codecs,math
import jieba.posseg as pseg
from config import config

names = {} # dictionary of names
relationships = {} # dictionary of relationships
lineNames = []  #relationships between characters in each line

"""
1. recognize the word of name in each line and record the names appered orderly
2. count the number of occurrences of a name in the whole text
"""
jieba.load_userdict(config['DICT_PATH']) 
with codecs.open(config['TEXT_PATH'],"r","utf8") as f:
    for line in f.readlines():
        poss = pseg.cut(line) 
        lineNames.append([])
        for w in poss:
            if w.flag != "nr" or len(w.word) < 2:
                continue
            lineNames[-1].append(w.word)
            if names.get(w.word) is None:
                names[w.word] = 0
                relationships[w.word] = {}
            names[w.word] += 1

for name,times in names.items():
    print(name,times)

"""
count the number of co-occurrences of two names in a line
"""

for line in lineNames:
    for name1 in line:
        for name2 in line:
            if name1 == name2:
                continue
            if relationships[name1].get(name2) is None:
                relationships[name1][name2] = 1
            else:
                relationships[name1][name2] = relationships[name1][name2] + 1

"""
1. write the name and the number it occurs in the whole texts to "node.txt"
2. write the relationship info to "edge.txt"
"""

with codecs.open(config['NODE_PATH'],"w","gbk") as f:
    f.write("Id Label Weight\r\n")
    for name, times in names.items():
        f.write(name + " " + name + " " + str(times) + "\r\n")

with codecs.open(config['EDGE_PATH'], "w", "gbk") as f:
    f.write("Source Target Weight\r\n")
    for name, edges in relationships.items():
        for v, w in edges.items():
            if w > 3:
                f.write(name + " " + v + " " + str(w) + "\r\n")
