#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import math
import json
import codecs

# Global
word_dic = {}

def decode(line):
	line = line.strip()
	lst = line.split(' ')
	rst = []
	for word in lst:
		if word_dic.has_key(word):
			item = word+"/"+word_dic[word]
			rst.append(item)
		else:
			item = word+"/NC"
			item = unicode(item, "utf-8")
			rst.append(item)
	return " ".join(rst)

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

model_path = "basemodel.txt"
fmodel = open(model_path, 'r')
line = fmodel.readline()
word_dic = json.loads(line)

fin = open(path, 'r')
with codecs.open("hmmoutput.txt", 'w', encoding="utf-8") as fout:
	while 1:
		line = fin.readline()
		if not line:
			break
		tmpline = decode(line)
		fout.write(tmpline)
		fout.write("\n")
