"""
CSCI 544 Homework 6 hmmlearn.py
Yuting ZHANG
6099111047
yutingz@usc.edu
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
# import codecs
import json

# Global
transition_dic = {}		#key: tag1,tag2  value: count
start_tag_dic = {}		#key: tag_start  value: count

tag_count_dic = {}		#key: tag 		value: count
word_dic = {}			#key: word 		value: list of the count for the 29 tags

tag_dic = { 			#key: tag 		value: index for the tag
	'DI': 0, 'NC': 1, 'FF': 2, 'SP': 3, 
	'DA': 4, 'AQ': 5, 'CC': 6, 'PR': 7, 
	'VM': 8, 'VS': 9, 'ZZ': 10, 'P0': 11, 
	'PP': 12, 'RG': 13, 'AO': 14, 'PX': 15, 
	'NP': 16, 'CS': 17, 'VA': 18, 'DD': 19, 
	'RN': 20, 'WW': 21, 'PI': 22, 'PD': 23, 
	'PT': 24, 'DR': 25, 'DP': 26, 'DT': 27, 'II': 28
}

"""
	Get the index for the corresponding tag.
	
	@tag: String
	rtn: integer
"""
def get_idx(tag):
	return tag_dic[tag]

"""
	Construc the model line by line.

	@line: String of the labeled line
"""
def construct_model(line):
	line = line.strip()
	lst = line.split(' ')
	slst = []
	slst.append("q0")

	for item in lst:
		word = item[:-3]
		tag = item[-2:]

		if tag_count_dic.has_key(tag):
			tag_count_dic[tag] += 1
		else:
			tag_count_dic[tag] = 1
		slst.append(tag)

		if word_dic.has_key(word):
			tidx = get_idx(tag)
			word_dic[word][tidx] += 1
		else:
			taglst = [0]*29
			tid = get_idx(tag)
			taglst[tid] += 1
			word_dic[word] = taglst

	for i in range(0, len(slst)-2):
		key = slst[i]+","+slst[i+1]
		if transition_dic.has_key(key):
			transition_dic[key] += 1
		else:
			transition_dic[key] = 1

"""
	Count the start tag of the transition to calculate the transition probability

	@dic: The transition probability dictionary
"""
def count_start_tag(dic):
	for key, value in dic.iteritems():
		start_tag = key.split(',')[0]
		if start_tag_dic.has_key(start_tag):
			start_tag_dic[start_tag] += value
		else:
			start_tag_dic[start_tag] = value

"""
Main Function
"""
# Deal with wrong argument number situation
if len(sys.argv) != 2:
    print "Wrong argument number"
    sys.exit()
path = sys.argv[1]

if not path.endswith('.txt'):
	print "Please enter a path to the traning txt file"
	sys.exit()


with open(path, 'r') as fin:
	while 1:
		line = fin.readline()
		if not line:
			break
		construct_model(line)

count_start_tag(transition_dic)

# Write dictionaries to model file.
with open('hmmmodel.txt', 'w') as fout:
	tmpstr = json.dumps(word_dic,ensure_ascii=False)
	fout.write(tmpstr)
	fout.write('\n')
	tmpstr = json.dumps(tag_count_dic,ensure_ascii=False)
	fout.write(tmpstr)
	fout.write('\n')
	tmpstr = json.dumps(start_tag_dic,ensure_ascii=False)
	fout.write(tmpstr)
	fout.write('\n')
	tmpstr = json.dumps(transition_dic,ensure_ascii=False)
	fout.write(tmpstr)
