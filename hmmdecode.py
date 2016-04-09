"""
CSCI 544 Homework 6 hmmdecode.py
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
Main Function
"""
# Deal with wrong argument number situation
if len(sys.argv) != 2:
    print "Wrong argument number"
    sys.exit()
path = sys.argv[1]

if not path.endswith('.txt'):
	print "Please enter a path to corpus txt file"
	sys.exit()

model_path = "hmmmodel.txt"
fmodel = open(model_path, 'r')
line = fmodel.readline()
word_dic = json.loads(line)

line = fmodel.readline()
tag_count_dic = json.loads(line)

line = fmodel.readline()
start_tag_dic = json.loads(line)

line = fmodel.readline()
transition_dic = json.loads(line)

fin = open(path, 'r')
while 1:
	line = fin.readline()
	if not line:
		break
	# for word in line.split(' '):
	# 	if word_dic.has_key(word):
	# 		print "has key"
	# 	else:
	# 		print "no key"
