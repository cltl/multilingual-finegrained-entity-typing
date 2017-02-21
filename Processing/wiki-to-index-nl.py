#!/usr/bin/python 

# This script makes an index of the cleaned up Dutch Wikipedia articles 
# and creates a file that contains a wikilink, a surface form, and the offsets in the text of the surface form
# marieke.van.erp@vu.nl
# 17 February 2017 

import sys 
import re
from bs4 import BeautifulSoup
from urllib.parse import unquote 
from nltk import word_tokenize, sent_tokenize
import nltk 
import glob 

from nltk.tag.perceptron import PerceptronTagger

# Dutch POS tagger from https://github.com/evanmiltenburg/Dutch-tagger
# Make sure the model.perc.dutch_tagger_small.pickle is in the same directory 
tagger = PerceptronTagger(load=False)
tagger.load('model.perc.dutch_tagger_small.pickle')

dbpedia_types = {} 
with open('dbpedia-wikipedia-type.tsv', 'r') as f:
	for line in f:
		line = line.rstrip()
		elems = line.split('\t') 
		elems[1] = elems[1].lstrip('<http://nl.wikipedia.org/wiki/')
		elems[1] = elems[1].rstrip('>')
		if 'dbpedia' in elems[2]:
			elems[2] = elems[2].lstrip('<http://dbpedia.org/ontology/')
			elems[2] = elems[2].rstrip('>')
			dbpedia_types[elems[1]] = elems[2]
		
def analyse_and_store_links(text):
	soup = BeautifulSoup(text, "lxml")
	tags = [] 
	links = []
	surface_forms = [] 
	tokenised_sentences =[]
	#pos_tags = []  
	for tag in soup.findAll('a', href=True):
		#print(tag['href'] + "\t" +  tag.string + "\t" + str(tag))
		# Ok, so you can get the tag, the link and the string, now you can loop through those 
		# match them in the text, and get the offsets. Not the neatest way to do it, but it should work.
		tags.append(str(tag))
		link = unquote(tag['href'])
		link = link[0].upper()+link[1:].replace(' ', '_')
	   # link = link.replace("_(hoofdbetekenis)", "")
		links.append(link)
		surface_forms.append(tag.string)
		cleantext = re.sub('<[^>]*>', '', text) 
		sents = sent_tokenize(cleantext)
		for sent in sents:
			tokens = word_tokenize(sent)
			pos = tagger.tag(tokens)
			postags = ''
			for i in pos:
				postags = postags + i[1] + " " 
			#pos_tags.append(postags)
			tokenised_sentences.append(' '.join(tokens) + "\t" + postags) 	
    	
   
	for idx, val in enumerate(surface_forms):
		#print(surface_forms[idx], links[idx])
		for sent in tokenised_sentences: 
			match = re.search(val, sent)
			type = ""
			if links[idx] in dbpedia_types:
				type = dbpedia_types[links[idx]]
			if(len(type) > 1) and match:
				outputstring = surface_forms[idx] + "\t" + type + "\t" + str(match.start()) + "\t" + str(match.end()) +  "\t" +  sent
				return outputstring
				break

files = glob.glob('/mnt/scistor1/group/marieke/text-nl/AA/wiki*')
for file in files:
	f = open(file, 'r')
	print(file)
	outputname = file + ".stripped" 
	outputfile = open(outputname, 'w')
	title = ''
	wikiurl = ''
	for line in f:
		line = line.rstrip()
		if len(line) > 1:
			if 'nl.wikipedia.org/wiki?curid' in line:
				try:
					elems = line.split('"')
					title = elems[5]
					wikiurl = elems[3]
				except:
					pass
			try:
				result = analyse_and_store_links(line)
				if result is not None:
					#print(result)
					outputfile.write(result + "\t" + title + "\t" + wikiurl + "\n")
			except:
				pass
	



    
