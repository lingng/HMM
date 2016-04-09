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
import math
import json
import cPickle as pickle

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

tags = ['DI', 'NC', 'FF', 'SP', 'DA', 'AQ', 'CC', 'PR',
	'VM', 'VS', 'ZZ', 'P0', 'PP', 'RG', 'AO', 'PX', 
	'NP', 'CS', 'VA', 'DD', 'RN', 'WW', 'PI', 'PD', 
	'PT', 'DR', 'DP', 'DT', 'II']

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

		# if word_dic.has_key(word):
		# 	if word_dic[word].has_key(tag):
		# 		word_dic[word][tag] += 1
		# 	else:
		# 		word_dic[word][tag] = 1
		# else:
		# 	v_dic = {}
		# 	v_dic[tag] = 1
		# 	word_dic[word] = v_dic
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
	Apply add-one smoothing to transition count

	@dic: dictionary of the transition count
"""
def smooth_transition(dic):
	for i in range(0, 29):
		key = "q0,"+tags[i]
		if dic.has_key(key):
			dic[key] += 1
		else:
			dic[key] = 1
	for i in range(0, 29):
		for j in range(0, 29):
			key = tags[i]+","+tags[j]
			if dic.has_key(key):
				dic[key] += 1
			else:
				dic[key] = 1

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
smooth_transition(transition_dic)
count_start_tag(transition_dic)

t_prob_dic = {}
e_prob_dic = {}
# construct transition probability log dictionary
for key, value in transition_dic.iteritems():
	prev_tag = key[0:2]
	pos_tag = key[3:5]
	prev_tag_c = start_tag_dic[prev_tag]
	tmp_tprob = float(value)/float(prev_tag_c)
	log_tprob = math.log(tmp_tprob)
	t_prob_dic[key] = log_tprob

# construct emission probability log dictionary
for key, value in word_dic.iteritems():
	tmp_edic = {}
	for i in range(0, 29):
		e_count = value[i]
		if e_count != 0:
			tag = tags[i]
			tag_count = tag_count_dic[tag]
			tmp_eprob = float(e_count)/float(tag_count)
			log_eprob = math.log(tmp_eprob)
			tmp_edic[tag] = log_eprob
	e_prob_dic[key] = tmp_edic

# Shrink the size of the word_dic
f_word_dic = {}
for key, value in word_dic.iteritems():
	tmp_wdic = {}
	for i in range(0, 29):
		if value[i] != 0:
			tag = tags[i]
			tmp_wdic[tag] = value[i]
	f_word_dic[key] = tmp_wdic

# Write dictionaries to model file.
with open('hmmmodel.txt', 'w') as fout:
	tmpstr = json.dumps(f_word_dic, ensure_ascii = False)
	fout.write(tmpstr)
	fout.write('\n')
	tmpstr = json.dumps(t_prob_dic, ensure_ascii=False)
	fout.write(tmpstr)
	fout.write('\n')
	tmpstr = json.dumps(e_prob_dic, ensure_ascii=False)
	fout.write(tmpstr)
	fout.write('\n')

