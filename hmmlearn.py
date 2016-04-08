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
import re

"""
Main Function
"""
# Deal with wrong argument number situation
if len(sys.argv) != 2:
    print "Wrong argument number"
    sys.exit()

# Get input file path
path = sys.argv[1]
# print path
transition_dic = {}

with open(path, 'r') as fin:
	while 1:
		line = fin.readline()
		if not line:
			break
		# print line
		line = line.strip()
		lst = line.split(' ')
		slst = []
		slst.append("q0")
		# print lst
		for item in lst:
			tag = item.split('/')[-1]
			# print item, tag
			slst.append(tag)
		# print slst
		for i in range(0, len(slst)-2):
			key = slst[i]+","+slst[i+1]
			if transition_dic.has_key(key):
				transition_dic[key] += 1
			else:
				transition_dic[key] = 1
print transition_dic
print len(transition_dic)