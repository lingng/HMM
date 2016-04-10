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
import codecs
import json

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

def initialization(word):
	probability = []
	if emission_dic.has_key(word):
		for i in range(0, 29):
			t_key = "q0,"+tags[i]
			t_prob = transition_dic[t_key]
			e_tag = tags[i]
			if emission_dic[word].has_key(e_tag):
				e_prob = emission_dic[word][e_tag]
				probability.append(e_prob+t_prob)
			else:
				probability.append(t_prob-25)
	else:
		for i in range(0, 29):
			t_key = "q0,"+tags[i]
			t_prob = transition_dic[t_key]
			probability.append(t_prob)
	return probability

def prev_one(prev_w, curr_w, prev_p):
	backpointer = []
	probability = []

	prev_t = emission_dic[prev_w].iterkeys().next()
	prev_idx = tag_dic[prev_t]

	for i in range(0, 29):
		backpointer.append(prev_idx)

	if emission_dic.has_key(curr_w):
		curr_tags = emission_dic[curr_w]
		# 1 - 1
		if len(curr_tags) == 1:
			return prev_p, backpointer
		# 1 - mul
		else:
			curr_idxs = []
			for tag in curr_tags:
				curr_idx = tag_dic[tag]
				curr_idxs.append(curr_idx)
			for i in range(0, 29):
				if i not in curr_idxs:
					probability.append(prev_p[prev_idx]-25)
				else:
					curr_t = tags[i]
					transition_key = prev_t+","+curr_t
					t_prob = transition_dic[transition_key]
					e_prob = emission_dic[curr_w][curr_t]
					probability.append(prev_p[prev_idx]+t_prob+e_prob)
			return probability, backpointer
	# 1 - unknown
	else:
		for i in range(0, 29):
			curr_t = tags[i]
			transition_key = prev_t+","+curr_t
			t_prob = transition_dic[transition_key]
			probability.append(prev_p[prev_idx]+t_prob)
		return probability, backpointer

def prev_mul(prev_w, curr_w, prev_p):
	backpointer = []
	probability = []

	prev_tags = emission_dic[prev_w].keys()

	if emission_dic.has_key(curr_w):
		# dictionary of the current word
		curr_tags = emission_dic[curr_w]

		# mul - 1
		if len(curr_tags) == 1:
			curr_t = curr_tags.iterkeys().next()
			curr_idx = tag_dic[curr_t]
			e_prob = emission_dic[curr_w][curr_t]

			# If not current word's tag index, -25
			# If is the current word's tag index, go through all previous tags to get a max prob val
			for i in range(0, 29):
				if i != curr_idx:
					probability.append(min(prev_p)-25)
					backpointer.append(-2)
				else:
					max_v = -10000
					max_i = -2
					for prev_t in prev_tags:
						prev_idx = tag_dic[prev_t]
						transition_key = prev_t+","+curr_t
						t_prob = transition_dic[transition_key]
						prob_val =prev_p[prev_idx]+t_prob+e_prob
						if prob_val > max_v:
							max_v = prob_val
							max_i = prev_idx

					probability.append(max_v)
					backpointer.append(max_i)
			return probability, backpointer
		# mul - mul
		else:
			for curr_i in range(0, 29):
				curr_t = tags[curr_i]
				if curr_tags.has_key(curr_t):
					e_prob = curr_tags[curr_t]
					max_v = -10000
					max_i = -2

					for prev_t in prev_tags:
						prev_idx = tag_dic[prev_t]
						transition_key = prev_t+","+tags[curr_i]
						t_prob = transition_dic[transition_key]
						value = prev_p[prev_idx]+t_prob+e_prob
						if value > max_v:
							max_v = value
							max_i = prev_idx
					probability.append(max_v)
					backpointer.append(max_i)

				else:
					probability.append(min(prev_p)-25)
					backpointer.append(-2)
			return probability, backpointer
	# mul - none
	else:
		for i in range(0, 29):
			curr_t = tags[i]
			max_v = -10000
			max_i = -2

			for prev_t in prev_tags:
				prev_idx = tag_dic[prev_t]
				transition_key = prev_t+","+curr_t
				t_prob = transition_dic[transition_key]
				value = prev_p[prev_idx]+t_prob
				if value > max_v:
					max_v = value
					max_i = prev_idx
			probability.append(max_v)
			backpointer.append(max_i)

		return probability, backpointer
			
def prev_none(prev_w, curr_w, prev_p):
	backpointer = []
	probability = []

	if emission_dic.has_key(curr_w):
		curr_tags = emission_dic[curr_w]
		# none - 1
		if len(curr_tags) == 1:
			curr_t = curr_tags.iterkeys().next()
			curr_i = tag_dic[curr_t]
			for i in range(0, 29):
				if i != curr_i:
					probability.append(min(prev_p)-25)
					backpointer.append(-2)
				else:
					max_v = -10000
					max_i = -2
					for j in range(0, 29):
						prev_t = tags[j]
						transition_key = prev_t+","+curr_t
						t_prob = transition_dic[transition_key]
						value = prev_p[j]+t_prob
						if value > max_v:
							max_v = value
							max_i = j
					probability.append(max_v)
					backpointer.append(max_i)
			return probability, backpointer
		# none - mul
		else:
			for i in range(0, 29):
				curr_t = tags[i]
				if curr_tags.has_key(curr_t):
					max_v = -10000
					max_i = -2
					for j in range(0, 29):
						prev_t = tags[j]
						transition_key = prev_t+","+curr_t
						t_prob = transition_dic[transition_key]
						value = prev_p[j]+t_prob
						if value > max_v:
							max_v = value
							max_i = j
					probability.append(max_v)
					backpointer.append(max_i)
				else:
					probability.append(min(prev_p)-25)
					backpointer.append(-2)
			return probability, backpointer
	# none - none
	else:
		for i in range(0, 29):
			curr_t = tags[i]
			max_v = -10000
			max_i = -2
			for j in range(0, 29):
				prev_t = tags[j]
				transition_key = prev_t+","+curr_t
				t_prob = transition_dic[transition_key]
				value = prev_p[j]+t_prob
				if value > max_v:
					max_v = value
					max_i = j
			probability.append(max_v)
			backpointer.append(max_i)
		return probability, backpointer
	
def get_probability(prev_w, curr_w, prev_p, probabilities, backpointers):
	# previous word has only one possible tag
	if emission_dic.has_key(prev_w) and len(emission_dic[prev_w]) == 1:
		rst = prev_one(prev_w, curr_w, prev_p)
		probabilities.append(rst[0])
		backpointers.append(rst[1])
	elif emission_dic.has_key(prev_w) and len(emission_dic[prev_w]) != 1:
		rst = prev_mul(prev_w, curr_w, prev_p)
		probabilities.append(rst[0])
		backpointers.append(rst[1])
	else:
		rst = prev_none(prev_w, curr_w, prev_p)
		probabilities.append(rst[0])
		backpointers.append(rst[1])

def get_final_path(prob, back):
	tags_i = []

	max_p = max(prob[len(prob)-1])
	max_i = prob[len(prob)-1].index(max(prob[len(prob)-1]))
	
	tags_i.append(max_i)
	
	for i in range(len(prob)-1, -1, -1):
		max_i = back[i][max_i]
		tags_i.append(max_i)
	rst = []
	for i in range(0, len(tags_i)):
		tag_i = tags_i.pop()
		if tag_i == -1:
			rst.append("q0")
		else:
			tag = tags[tag_i]
			rst.append(tag)
	rst = rst[1:]
	return rst

def construct_result_line(w, t):
	rst = []
	for i in range(0, len(w)):
		pair = w[i]+"/"+t[i]
		rst.append(pair)
	return " ".join(rst)

def get_end_prob(prev_w, prev_p, probabilities, backpointers):
	curr_t = "q1"

	backpointer = []
	probability = []

	if emission_dic.has_key(prev_w):
		prev_tags = emission_dic[prev_w]
		# 1 - q1
		if len(prev_tags) == 1:
			prev_t = prev_tags.iterkeys().next()
			prev_i = tag_dic[prev_t]

			transition_key = prev_t+",q1"
			t_prob = transition_dic[transition_key]
	
			for i in range(0, 29):
				if i != prev_i:
					probability.append(prev_p[i]-25)
					backpointer.append(prev_i)
				else:
					probability.append(prev_p[i]+t_prob)
					backpointer.append(prev_i)
			probabilities.append(probability)
			backpointers.append(backpointer)
		# mul - q1
		else:
			max_v = -10000
			max_i = -2

			for prev_t in prev_tags.iterkeys():
				transition_key = prev_t+",q1"
				t_prob = transition_dic[transition_key]
				if value > max_v:
					max_i = i
					max_v = value

			for i in range(0,29):
				if i != max_i:
					probability.append(prev_p[i]-25)
					backpointer.append(-2)
				else:
					probability.append(max_v)
					backpointer.append(max_i)
			probabilities.append(probability)
			backpointers.append(backpointer)
			# for i in range(0, 29):
			# 	prev_t = tags[i]
			# 	if prev_tags.has_key(prev_t):
			# 		transition_key = prev_t+",q1"
			# 		t_prob = transition_dic[transition_key]
			# 		value = prev_p[i]+t_prob
			# 		if value > max_v:
			# 			max_i = i
			# 			max_v = value
			# 	else:

	# unknown - q1
	else:
		for i in range(0, 29):
			prev_t = tags[i]
			transition_key = prev_t+",q1"
			t_prob = transition_dic[transition_key]
			probability.append(prev_p[i]+t_prob)
			backpointer.append(i)
		probabilities.append(probability)
		backpointers.append(backpointer)

def viterbi(line):
	line = line.strip()
	words = line.split(" ")
	probabilities = []
	backpointers = []

	# Initialization
	probabilities.append(initialization(words[0]))
	t_b = []
	for i in range(0, 29):
		t_b.append(-1)
	backpointers.append(t_b)

	for i in range(1, len(words)):
		get_probability(words[i-1], words[i], probabilities[-1], probabilities, backpointers)
	get_end_prob(words[len(words)-1], probabilities[-1], probabilities, backpointers)

	tags = get_final_path(probabilities, backpointers)
	rstline = construct_result_line(words, tags)
	return rstline

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
with open("hmmoutput.txt", "w") as fout:
	while 1:
		line = fin.readline()
		if not line:
			break
		rstline = viterbi(line)
		fout.write(rstline)
		fout.write("\n")