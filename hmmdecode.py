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
import math
import json

# Global
# word_dic = {}
transition_dic = {}
emission_dic = {}
# -1 stands for q0; -2 stands for impossible state
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

def get_curr_prob(prev_word, c_word, prev_p):
	# Return list of probability and list of back pointer
	# print c_word, prev_p
	tmp_p = []
	tmp_b = []
	# Prev word only 1 tag
	if emission_dic.has_key(prev_word) and len(emission_dic[prev_word]) == 1:
		if emission_dic.has_key(c_word) and len(emission_dic[c_word]) == 1:
			prev_t = emission_dic[prev_word].iterkeys().next()
			prev_i = tag_dic[prev_t]
			curr_t = emission_dic[c_word].iterkeys().next()
			e_p = emission_dic[c_word].itervalues().next()
			
			for i in range(0, 29):
				key = prev_t+","+curr_t
				t_p = transition_dic[key]
				if i != tag_dic[curr_t]:
					tmp_p.append(0) # Impossible prob
					tmp_b.append(-2)
				else:
					tmp_p.append(prev_p[i] + t_p + e_p)
					tmp_b.append(prev_i)
			# print "1-1"
		elif emission_dic.has_key(c_word) and len(emission_dic[c_word]) != 1:
			prev_t = emission_dic[prev_word].iterkeys().next()
			prev_i = tag_dic[prev_t]
			for c_t in emission_dic[c_word].iterkeys():
				e_p = emission_dic[c_word][c_t]
				for i in range(0, 29):
					key = prev_t+","+c_t
					t_p = transition_dic[key]
					if i != tag_dic[c_t]:
						tmp_p.append(0) # Impossible prob
						tmp_b.append(-2)
					else:
						tmp_p.append(prev_p[i] + t_p + e_p)
						tmp_b.append(prev_i)
			# print "1-mul"
		else:
			prev_t = emission_dic[prev_word].iterkeys().next()
			prev_i = tag_dic[prev_t]
			for i in range(0, 29):
				c_t = tags[i]
				key = prev_t+","+c_t
				t_p = transition_dic[key]
				tmp_p.append(prev_p[prev_i] + t_p)
				tmp_b.append(prev_i)
			# print "1-none"
	elif emission_dic.has_key(prev_word) and len(emission_dic[prev_word]) != 1:
		if emission_dic.has_key(c_word) and len(emission_dic[c_word]) == 1:
			
			print "mul-1"
	# 	elif emission_dic.has_key(c_word) and len(emission_dic[c_word]) != 1:
	# 		print "mul-mul"
	# 	else:
	# 		print "mul-none"		
	# else:
	# 	if emission_dic.has_key(c_word) and len(emission_dic[c_word]) == 1:
	# 		print "none-1"
	# 	elif emission_dic.has_key(c_word) and len(emission_dic[c_word]) != 1:
	# 		print "none-mul"
	# 	else:
	# 		print "none-none"
	# Prev word multiple tag
	# elif emission_dic.has_key(prev_word) and len(emission_dic[prev_word]) != 1:
	# Prev word not in dic
	# else:
	# if emission_dic.has_key(c_word):
	# 	if len(emission_dic[c_word]) == 1:
	# 		# Only 1 tag for this word
	# 		value = emission_dic[c_word]
	# 		curr_t = value.iterkeys().next()
	# 		e_p = value.itervalues().next()
	# 		for i in range(0, 29):
	# 			prev_t = tags[i]
	# 			key = prev_t+","+curr_t
	# 			t_p = transition_dic[key]
	# 			tmp_p.append(prev_p[i] + t_p + e_p)
	# 		max_i = tmp_p.index(max(tmp_p))
			
	# 		for i in range(0, 29):
	# 			if i != max_i:
	# 				tmp_b.append(-2)
	# 			else:
	# 				tmp_b.append(max_i)
	# 		return tmp_p, tmp_b
	# 	else:
	# 		print "More than 1 tag"
	# 		tmp_p = [-2, -2, -2, -2, 4, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2]
	# 		tmp_b = [-2, -2, -2, -2, 4, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2]
	# else:
	# 	print "Not in dic"
	# 	for i in range(0, 29):
	# 		prev_t = tags[i]
	# 		key = prev_t+","+curr_t
	# 		t_p = transition_dic[key]
	# 		tmp_p.append(prev_p[i] + t_p)
	# 	max_i = tmp_p.index(max(tmp_p))

	# 	for i in range(0, 29):
	# 		if i != max_i:
	# 			tmp_b.append(-2)
	# 		else:
	# 			tmp_b.append(max_i)
	# 	return tmp_p, tmp_b
	# return tmp_p, tmp_b


def viterbi(line):
	# Initialization
	line = line.strip()
	print line
	words = line.split(" ")

	# 2D array for probability and backpointer
	probability = []
	backpointer = []

	word = words[0]
	tmp_p = []
	tmp_b = []
	for i in range(0, 29):
		prev_t = "q0"
		curr_t = tags[i]
		key = prev_t+","+curr_t
		tmp_p.append(transition_dic[key])
		# If word appear in the word dic
		if emission_dic.has_key(word):
			# current tag
			curr_t = tags[i]
			# If the word has this tag
			if emission_dic[word].has_key(curr_t):
				tmp_p[i] = tmp_p[i]+emission_dic[word][curr_t]
		tmp_b.append(-1)
	probability.append(tmp_p)
	backpointer.append(tmp_b)

	for i in range(1, len(words)):
		tmprst = get_curr_prob(words[i-1], words[i], probability[-1])
		# probability.append(tmprst[0])
		# backpointer.append(tmprst[1])


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
transition_dic = json.loads(line)
line = fmodel.readline()
emission_dic = json.loads(line)

fin = open(path, 'r')
while 1:
	line = fin.readline()
	if not line:
		break
	viterbi(line)
