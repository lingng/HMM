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

"""
	Get the transitions and count them in the transition dictionary
	Add start tag (q0) and end tag (q1).

	@pairs: the list of word/tag pair.
	@tran_c_dic: transition count dictionary. 
		Key: transition (format: tag1,tag2 ) Value: count of this transition
"""
def get_transition(pairs, tran_c_dic):
	# for all start transition
	initial_transition = "q0,"+pairs[0][-2:]
	if tran_c_dic.has_key(initial_transition):
		tran_c_dic[initial_transition] += 1
	else:
		tran_c_dic[initial_transition] = 1

	# paired transition
	for i in range(1, len(pairs)):
		prev_tag = pairs[i-1][-2:]
		curr_tag = pairs[i][-2:]
		transition_key = prev_tag+","+curr_tag
		if tran_c_dic.has_key(transition_key):
			tran_c_dic[transition_key] += 1
		else:
			tran_c_dic[transition_key] = 1

	# for all end transition
	final_transition = pairs[len(pairs)-1][-2:]+",q1"
	if tran_c_dic.has_key(final_transition):
		tran_c_dic[final_transition] += 1
	else:
		tran_c_dic[final_transition] = 1

"""
	Get the count of a specific tag.

	@pairs: the list of word/tag pair.
	@tag_c_dic: dictionary of tag count. Key: tag; Value: count of this tag
"""
def get_tag_count(pairs, tag_c_dic):
	for i in range(0, len(pairs)):
		tag = pairs[i][-2:]
		if tag_c_dic.has_key(tag):
			tag_c_dic[tag] += 1
		else:
			tag_c_dic[tag] = 1

"""
	Get the emission count.

	@pairs: the list of word/tag pair.
	@emi_dic: Emission dictionary.
		Key: word
		Value: A dictionary. Key: tag; Value: count
"""
def get_emission_count(pairs, emi_dic):
	for i in range(0, len(pairs)):
		word = pairs[i][:-3]
		tag = pairs[i][-2:]
		if emi_dic.has_key(word):
			if emi_dic[word].has_key(tag):
				emi_dic[word][tag] += 1
			else:
				emi_dic[word][tag] = 1
		else:
			obj = {}
			obj[tag] = 1
			emi_dic[word] = obj

"""
	Construct model from the given line.

	@line: input line
	@tran_c_dic: transition count dictionary
	@tag_c_dic: tag count dictionary
	@emi_dic: emission dictionary
"""
def construct_model(line, tran_c_dic, tag_c_dic, emi_dic):
	line = line.strip()
	pairs = line.split(" ")
	get_transition(pairs, tran_c_dic)
	get_tag_count(pairs, tag_c_dic)
	get_emission_count(pairs, emi_dic)

"""
	Calculate the emission probability.
	After finishing the function, the stored value in the emi_dic will be the emission probability rather than the count

	@emi_dic: emission probability dictionary
	@tag_c_dic: tag count dictionary
"""
def calculate_emission_prob(emi_dic, tag_c_dic):
	for word, word_c_dic in emi_dic.iteritems():
		for tag, tag_c in word_c_dic.iteritems():
			emission_prob = float(tag_c)/float(tag_c_dic[tag])
			e_p = math.log(emission_prob)
			emi_dic[word][tag] = e_p

"""
	Get the number that the transition starts from this tag.

	@tran_c_dic: transition count dictionary
	return: a dictionary. Key: tag; Value: the count that the transition start with this tag.
"""
def get_start_tag_count(tran_c_dic):
	start_dic = {}
	for transition_key, transition_count in tran_c_dic.iteritems():
		prev_tag = transition_key[:2]
		if start_dic.has_key(prev_tag):
			start_dic[prev_tag] += transition_count
		else:
			start_dic[prev_tag] = transition_count
	return start_dic

"""
	Calculate transition probability. Apply add-one smoothing for transitions

	@tran_c_dic: Transition count dictionary
	return: transition probability dictionary
"""
def calculate_transition_prob(tran_c_dic):
	start_tag_dic = get_start_tag_count(tran_c_dic)

	tags = [u'DI', u'NC', u'FF', u'SP', u'DA', u'AQ', u'CC', u'PR',
			u'VM', u'VS', u'ZZ', u'P0', u'PP', u'RG', u'AO', u'PX', 
			u'NP', u'CS', u'VA', u'DD', u'RN', u'WW', u'PI', u'PD', 
			u'PT', u'DR', u'DP', u'DT', u'II']

	tran_p_dic = {}

	for i in range(0, len(tags)):
		# Start of the sentence. q0: start tag.
		# from q0 to 29 tags -> +29
		beginning_transition = "q0,"+tags[i]
		if tran_c_dic.has_key(beginning_transition):
			tran_c = tran_c_dic[beginning_transition]+1
		else:
			tran_c = 1
		start_c = start_tag_dic["q0"]+29
		tran_p = float(tran_c)/float(start_c)
		tran_p = math.log(tran_p)
		tran_p_dic[beginning_transition] = tran_p

		# End of the sentence. q1: end tag.
		# From 29 tags to 29tags + end tag -> +30
		ending_transition = tags[i]+",q1"
		if tran_c_dic.has_key(ending_transition):
			tran_c = tran_c_dic[ending_transition]+1
		else:
			tran_c = 1
		start_c = start_tag_dic[tags[i]]+30
		tran_p = float(tran_c)/float(start_c)
		tran_p = math.log(tran_p)
		tran_p_dic[ending_transition] = tran_p

		# Normal transition between 29 tags
		# From 29 tags to 29tags + end tag -> +30
		for j in range(0, 29):
			transition_key = tags[i]+","+tags[j]
			
			if tran_c_dic.has_key(transition_key):
				tran_c = tran_c_dic[transition_key] + 1
			else:
				tran_c = 1
			start_c = start_tag_dic[tags[i]] + 30
			tran_p = float(tran_c)/float(start_c)
			tran_p = math.log(tran_p)
			tran_p_dic[transition_key] = tran_p
	return tran_p_dic

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

transition_count_dic = {}
tag_count_dic = {}
emission_dic = {}

with open(path, 'r') as fin:
	while 1:
		line = fin.readline()
		if not line:
			break
		construct_model(line, transition_count_dic, tag_count_dic, emission_dic)
tran_prob = calculate_transition_prob(transition_count_dic)
calculate_emission_prob(emission_dic, tag_count_dic)
# Write dictionaries to model file.
with open('hmmmodel.txt', 'w') as fout:
	tmpstr = json.dumps(tran_prob, ensure_ascii=False)
	fout.write(tmpstr)
	fout.write('\n')
	tmpstr = json.dumps(emission_dic, ensure_ascii=False)
	fout.write(tmpstr)
	fout.write('\n')
