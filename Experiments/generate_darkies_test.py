#!/usr/bin/python

# This script filters out all the 'known' entities from the test data
# Just to check how we are doing on 'dark' entities 

# Marieke van Erp 
# 21 February 2017

import sys

entities = {}
with open('nlwiki_entities_in_train.tsv' , 'r') as f:
	for line in f:
		line = line.rstrip()
		entities[line] = 1 
f.close 

with open('nlwiki_test.tsv', 'r') as f:
	for line in f:
		line = line.rstrip()
		elems = line.split(",")
		if elems[1].rstrip().lstrip() in entities:
			pass
		else:
			print(line)
