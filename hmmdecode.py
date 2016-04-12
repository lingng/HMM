#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CSCI 544 Homework 6 hmmdecode.py
Yuting ZHANG
6099111047
yutingz@usc.edu
"""

import sys
import os
import math
import codecs
import json

reload(sys)
sys.setdefaultencoding("utf-8")

"""
	Get the possible tags for the given word

	@word: String of the word
	return: list of possible tags
"""
def get_word_tags(word):
	tags = []
	if emission_dic.has_key(word):
		for tag in emission_dic[word].iterkeys():
			tags.append(tag)
	else:
		# no such word in the training set, return all tags as possible tags
		tags = [u'DI', u'NC', u'FF', u'SP', u'DA', u'AQ', u'CC', u'PR',
			u'VM', u'VS', u'ZZ', u'P0', u'PP', u'RG', u'AO', u'PX', 
			u'NP', u'CS', u'VA', u'DD', u'RN', u'WW', u'PI', u'PD', 
			u'PT', u'DR', u'DP', u'DT', u'II']
	return tags

"""
	Get all the emission probabilities for the given word

	@word: String of the word
	return: dictionary of the emission probabilities. 
		Key: the possible tags for this word
		Value: the emission probability
"""
def get_word_emissions(word):
	word_e = {}
	# word = word.encoding("utf-8")
	if emission_dic.has_key(word):
		word_e = emission_dic[word]
	return word_e

"""
	Initialization the probability and the backpointer

	@word: String of the word
	return: two dictionaries of the probability and the backpointers
		prob: Key: possible tags for the current word; 
			  Value: transition_probability(q0, tag) [+ emission_probability(word[0]|tag)]
		back: Key: possible tags for the current word;
			  Value: q0
"""
def initialization(word):
	prob = {}
	back = {}
	
	tags = get_word_tags(word)
	e_probs = get_word_emissions(word)
	if len(e_probs) == 0:
		# No such beginning word in the training set
		for tag in tags:
			transition_key = "q0,"+tag
			t_prob = transition_dic[transition_key]
			prob[tag] = t_prob
			back[tag] = "q0"
	else:
		# Have this word in the training set, thus need to add the emission probability
		for tag in tags:
			transition_key = "q0,"+tag
			t_prob = transition_dic[transition_key]
			prob[tag] = t_prob + e_probs[tag]
			back[tag] = "q0"
	return prob, back

"""
	Get the probability for the given word

	@word: String of the word
	@prev_p: Dictionary of the previous probability
	return: two dictionaries of the probability and the backpointers
		prob: Key: possible tags for the current word; 
			  Value: max( previous_probability(previous_tag) + transition_probability(previous_tag, current_tag) [+ emission_probability(word|current_tag)] )
		back: Key: possible tags for the current word;
			  Value: previous_tag with the maximum calculated probability
"""
def get_probability(word, prev_p):
	prob = {}
	back = {}
	tags = get_word_tags(word)
	e_probs = get_word_emissions(word)
	if len(e_probs) != 0:
		# Have such word in the training set
		for curr_t in tags:
			max_v = -10000
			max_t = "ept"
			for prev_t in prev_p.iterkeys():
				transition_key = prev_t+","+curr_t
				t_prob = transition_dic[transition_key]
				e_prob = e_probs[curr_t]
				value = prev_p[prev_t] + t_prob + e_prob
				if value > max_v:
					max_v = value
					max_t = prev_t
			prob[curr_t] = max_v
			back[curr_t] = max_t
	else:
		# print word
		# No such word in training set
		for curr_t in tags:
			max_v = -10000
			max_t = "ept"
			for prev_t in prev_p.iterkeys():
				transition_key = prev_t+","+curr_t
				t_prob = transition_dic[transition_key]
				value = prev_p[prev_t] + t_prob
				if value > max_v:
					max_v = value
					max_t = prev_t
			prob[curr_t] = max_v
			back[curr_t] = max_t
	return prob, back

"""
	Add the end state, get the final probability and the final backpointer

	@word: String of the word
	@prev_p: Dictionary of the previous probability
	return: two dictionaries of the probability and the backpointers
		prob: Key: q1; 
			  Value: max( previous_probability(previous_tag) + transition_probability(previous_tag, q1) )
		back: Key: q1;
			  Value: previous_tag with the maximum calculated probability
"""
def add_ending(word, prev_p):
	prob = {}
	back = {}
	for prev_t in prev_p.iterkeys():
		transition_key = prev_t+",q1"
		t_prob = transition_dic[transition_key]
		if prob.has_key("q1"):
			val = prev_p[prev_t]+t_prob
			if val > prob["q1"]:
				back["q1"] = prev_t
			prob["q1"] = max(val, prob["q1"])
		else:
			prob["q1"] = prev_p[prev_t]+t_prob
			back["q1"] = prev_t
	return prob, back

"""
	Get the final result for the line.

	@back: A list of backpointers. A list of dictionaries.
	@words: A list of string. 
	return: String of the "word/tag" pair. Use whitespace to join them.
"""
def get_path(back, words):
	r_tags = []
	c_tags = []
	s_tag = back[len(back)-1]["q1"]
	r_tags.append(s_tag)

	for i in range(len(back)-2, 0, -1):
		s_tag = back[i][s_tag]
		r_tags.append(s_tag)
	for i in range(len(r_tags)-1, -1, -1):
		c_tags.append(r_tags[i])
	
	rst = []
	for i in range(0, len(words)):
		pair = words[i]+"/"+c_tags[i]
		rst.append(pair)
	return " ".join(rst)

"""
	Call the Viterbi algorithm.

	@line: String of the input line
	return: Tagged line
"""
def viterbi(line):
	line = line.strip()
	words = line.split(" ")
	probabilities = []
	backpointers = []
	rst = initialization(words[0])
	probabilities.append(rst[0])
	backpointers.append(rst[1])

	for i in range(1, len(words)):
		rst = get_probability(words[i], probabilities[-1])
		probabilities.append(rst[0])
		backpointers.append(rst[1])

	rst = add_ending(words[len(words)-1], probabilities[-1])
	probabilities.append(rst[0])
	backpointers.append(rst[1])

	rline = get_path(backpointers, words)
	return rline


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

# Construct model from the model text file.
model_path = "hmmmodel.txt"
fmodel = open(model_path, 'r')
line = fmodel.readline()
transition_dic = json.loads(line)
line = fmodel.readline()
emission_dic = json.loads(line)

# Apply the algorithm to the input file, generate tagged output
fin = codecs.open(path, encoding='utf-8')
# fin = open(path, 'r')
with open("hmmoutput.txt", "w") as fout:
	while 1:
		line = fin.readline()
		if not line:
			break
		rstline = viterbi(line)
		fout.write(rstline)
		fout.write("\n")