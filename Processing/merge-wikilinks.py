#!/usr/bin/python

# Quick little conversion script that merges wikipedia links with dbpedia instance types
# comment out lines 8 and 19 for Spanish
# comment out lines 9 and 20 for Dutch  
# marieke.van.erp@vu.nl

wikipedia_links = {} 
with open('wikipedia_links_es.ttl', 'r') as f:
#with open('wikipedia_links_nl.ttl', 'r') as f:
	for line in f:
		line = line.rstrip()
		elems = line.split(' ')
		if 'dbpedia' in elems[0]:
			wikipedia_links[elems[0]] = elems[2]
		#	print(elems[2], elems[0])
f.close()

with open('instance_types_es.ttl', 'r') as f:
#with open('instance_types_nl.ttl', 'r') as f:
	for line in f:
		line = line.rstrip()
		elems= line.split(' ')
		if elems[0] in wikipedia_links:
			print(elems[0] + "\t" + wikipedia_links[elems[0]] + "\t" + elems[2])
f.close()
			
