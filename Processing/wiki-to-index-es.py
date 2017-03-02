#!/usr/bin/python 

# This script makes an index of the cleaned up Spanish Wikipedia articles 
# and creates a file that contains a wikilink, a surface form, and the offsets in the text of the surface form
# marieke.van.erp@vu.nl
# 19 February 2017 

from __future__ import print_function
import sys 
import re
from bs4 import BeautifulSoup
from urllib.parse import unquote 
from nltk import word_tokenize, sent_tokenize
import nltk 
import glob 
import spaghetti as sgt

nltk.data.path.append("/data/nltk_data")

dbpedia_types = {} 
with open('dbpedia-wikipedia-type-es.tsv', 'r') as f:
	for line in f:
		line = line.rstrip()
		elems = line.split('\t') 
		elems[1] = elems[1].lstrip('<http://es.wikipedia.org/wiki/')
		elems[1] = elems[1].rstrip('>')
		if 'dbpedia' in elems[2]:
			elems[2] = elems[2].lstrip('<http://dbpedia.org/ontology/')
			elems[2] = elems[2].rstrip('>')
			dbpedia_types[elems[1]] = elems[2]
		
def analyse_and_store_links(text):
	outputstring = []
	soup = BeautifulSoup(text, "lxml")
	tags = [] 
	links = []
	surface_forms = [] 
	tokenised_sentences =[]
	pos_tags = []
	sents = []  
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
		#print(tag.string + "\t" + cleantext) 
		sents = sent_tokenize(cleantext)
		for sent in sents:
			tokens = word_tokenize(sent)
			pos = sgt.pos_tag(tokens)
			postags = ''
			for i in pos:
				#print(i[1])
				postags = postags + str(i[1]) + " " 
			pos_tags.append(postags)
			tokenised_sentences.append(' '.join(tokens) + "\t" + postags) 
	
	#print(len(surface_forms))
	for idx, val in enumerate(surface_forms):
		#print(idx)
		for sent in tokenised_sentences: 
			#print(sent)
			match = re.search(surface_forms[idx].rstrip(), sent)
		#	if match:
		#		print("blablaba", surface_forms[idx],sent)
			type = ""
			if links[idx] in dbpedia_types:
				type = dbpedia_types[links[idx]]
				#print(surface_forms[idx],type)
			if(len(type) > 1) and match:
				output = surface_forms[idx] + "\t" + type + "\t" + str(match.start()) + "\t" + str(match.end()) +  "\t" +  sent
				outputstring.append(output)
				break
	return outputstring
			#	
		#outputstring = "bla"
		#return outputstring
				#break

#text = """Tiene una extensión de 468 <a href="km%C2%B2">km</a> y está situado en los <a href="Pirineos">Pirineos</a>, entre <a href="Espa%C3%B1a">España</a> y <a href="Francia">Francia</a>, con una altitud media de 1996 <a href="Altitud">m s. n. m.</a> Limita por el sur con <a href="Espa%C3%B1a">España</a> —con las comarcas <a href="Catalu%C3%B1a">catalanas</a> de <a href="Cerda%C3%B1a">Cerdaña</a>, <a href="Alto%20Urgel">Alto Urgel</a> y <a href="Pallars%20Sobir%C3%A1">Pallars Sobirá</a>— y por el norte con <a href="Francia">Francia</a> —con los departamentos de <a href="Ari%C3%A8ge">Ariège</a> y <a href="Pirineos%20Orientales">Pirineos Orientales</a> (<a href="Occitania%20%28regi%C3%B3n%29">Occitania</a>)—."""

#print(text)
#result = analyse_and_store_links(text)
#for item in result:
#	print(item)

files = glob.glob('text-es/' + sys.argv[1] + '/wiki_*')
#files = ['text-es/BL/wiki_00']
#files = glob.glob('wikiextractor/text-es/AA/wiki*')
for file in files:
	f = open(file, 'r')
#	print(file)
	outputname = file + ".stripped" 
#	outputfile = open(outputname, 'w')
	title = ''
	wikiurl = ''
	for line in f:
		line = line.rstrip()
		if len(line) > 1:
			if 'es.wikipedia.org/wiki?curid' in line:
				try:
					elems = line.split('"')
					title = elems[5]
					wikiurl = elems[3]
				except:
					pass
			try:
				result = analyse_and_store_links(line)
				if result is not None:
#					#print(result)
					for item in result:
						print(item + "\t" + title + "\t" + wikiurl)
						outputfile.write(item + "\t" + title + "\t" + wikiurl + "\n")
#					#outputfile.write(result + "\t" + title + "\t" + wikiurl + "\n")
			except:
				pass
	



    
