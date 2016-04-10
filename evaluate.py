#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

cc = 0
tc = 0

fcorrect = open("./hw6-dev-train/catalan_corpus_dev_tagged.txt", 'r')
flabeled = open("hmmoutput.txt", 'r')

while 1:
	correct_line = fcorrect.readline()
	labeled_line = flabeled.readline()
	if not correct_line:
		break
	correct_line = correct_line.strip()
	labeled_line = labeled_line.strip()
	c_tags = correct_line.split(" ")
	l_tags = labeled_line.split(" ")
	for i in range(0, len(c_tags)):
		if c_tags[i] == l_tags[i]:
			cc += 1
		tc += 1
print cc, tc
	