#!/usr/bin/py

# This script extracts the different levels from the types to score
# the system per level in the hierarchy 

# marieke.van.erp@vu.nl
# 21 February 2017

import sys 


outputl1 = sys.argv[1] + ".l1"
outputfilel1 = open(outputl1, 'w')
outputl2 = sys.argv[1] + ".l2"
outputfilel2 = open(outputl2, 'w')
outputl3 = sys.argv[1] + ".l3"
outputfilel3 = open(outputl3, 'w')

with open(sys.argv[1], 'r') as f:
	for line in f:
		line = line.rstrip()
		line = line.replace("__label__","")
		elems = line.split("\t")
		levels_gold = elems[0].split("/")
		levels_pred = elems[1].split("/")
		levels_gold.append(" ")
		levels_gold.append(" ")
		levels_pred.append(" ")
		levels_pred.append(" ")
		outputfilel1.write(levels_gold[0] + "\t" + levels_pred[0] + "\n")
		outputfilel2.write(levels_gold[1] + "\t" + levels_pred[1] + "\n")
		outputfilel3.write(levels_gold[2] + "\t" + levels_pred[2] + "\n")
