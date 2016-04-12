#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Acc:
# Correct: 81817
# Total: 95673
# Accuracy: 0.855173350893

import sys
import os
import math
import json

word_dic = {}
f_word_dic = {}
tag_dic = { 			#key: tag 		value: index for the tag
	'DI': 0, 'NC': 1, 'FF': 2, 'SP': 3, 
	'DA': 4, 'AQ': 5, 'CC': 6, 'PR': 7, 
	'VM': 8, 'VS': 9, 'ZZ': 10, 'P0': 11, 
	'PP': 12, 'RG': 13, 'AO': 14, 'PX': 15, 
	'NP': 16, 'CS': 17, 'VA': 18, 'DD': 19, 
	'RN': 20, 'WW': 21, 'PI': 22, 'PD': 23, 
	'PT': 24, 'DR': 25, 'DP': 26, 'DT': 27, 'II': 28
}

tags = ['DI', 'NC', 'FF', 'SP', 'DA', 'AQ', 'CC', 'PR',
	'VM', 'VS', 'ZZ', 'P0', 'PP', 'RG', 'AO', 'PX', 
	'NP', 'CS', 'VA', 'DD', 'RN', 'WW', 'PI', 'PD', 
	'PT', 'DR', 'DP', 'DT', 'II']
def get_idx(tag):
	return tag_dic[tag]

def construct_model(line):
	line = line.strip()
	lst = line.split(' ')
	slst = []

	for item in lst:
		word = item[:-3]
		tag = item[-2:]

		if word_dic.has_key(word):
			tidx = get_idx(tag)
			word_dic[word][tidx] += 1
		else:
			taglst = [0]*29
			tid = get_idx(tag)
			taglst[tid] += 1
			word_dic[word] = taglst

def get_most_tag(dic):
	for key, value in dic.iteritems():
		max_v = max(value)
		max_i = value.index(max_v)
		tag = tags[max_i]
		f_word_dic[key] = tag
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
get_most_tag(word_dic)

with open('basemodel.txt', 'w') as fout:
	tmpstr = json.dumps(f_word_dic, ensure_ascii = False)
	fout.write(tmpstr)
	