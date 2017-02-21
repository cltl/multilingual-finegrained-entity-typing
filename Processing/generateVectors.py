#!/usr/bin/python 

# This script generates test data from the Stripped Wikipedia-nl test set 

# marieke.van.erp@vu.nl
# 18 February 2017

import sys 
import re 
import nltk 
import unicodedata


def word2ngrams(text, n=3, exact=True):
	return ["".join(j) for j in zip(*[text[i:] for i in range(n)])]
	
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

types = {'CelestialBody' : 'location/celestial', 'City':'location/city', 'Settlement':'location/city', 'Municipality':'location/city', 'Country':'location/country', 'NaturalPlace':'location/geography', '':'location/geography/body_of_water', 'Island':'location/geography/island', 'Mountain':'location/geography/mountain',  'MountainPass':'location/geography/mountain',  'MountainRange':'location/geography/mountain', 'Park':'location/park', 'Building':'location/structure', 'Airport':'location/structure/airport',  'Hotel':'location/structure/hotel', 'Restaurant':'location/structure/restaurant', 'SportFacility':'location/structure/sports_facility', 'Infrastructure':'location/transit', 'Bridge':'location/transit/bridge', 'RailwayLine':'location/transit/railway', 'Road':'location/transit/road', 'Company':'organization/company', 'Organisation': 'organization', 'BroadcastNetwork':'organization/company/broadcast', 'Newspaper':'organization/company/news','EducationalInstitution':'organization/education', 'GovernmentAgency':'organization/government', 'MilitaryUnit':'organization/military', 'RecordLabel':'organization/music', 'PoliticalParty':'organization/political_party', 'SportsLeague':'organization/sports_league', 'SportsTeam':'organization/sports_team', 'PublicTransitSystem':'organization/transit', 'Artwork':'other/art', 'RadioProgram':'other/art/broadcast', 'TelevisionShow':'other/art/broadcast', 'Film':'other/art/film', 'MusicalWork':'other/art/music','Play':'other/art/stage', 'WrittenWork':'other/art/writing', 'Award':'other/award', 'AnatomicalStructure':'other/body_part', 'Currency':'other/currency', 'Event':'other/event', 'Election':'other/event/election', 'Holiday':'other/event/holiday', 'NaturalEvent':'other/event/natural_disaster', 'SportsEvent':'other/event/sports_event', 'Rebellion':'other/event/protest', 'MilitaryConflict':'other/event/violent_conflict', 'Attack':'other/event/violent_conflict', 'Food':'other/food', 'Disease':'other/health/malady', 'Medicine':'other/health/treatment', 'Ethnicity':'other/heritage', 'EthnicGroup': 'other/heritage', 'Website':'other/internet', 'Language':'other/language', 'ProgrammingLanguage':'other/language/programming_language', 'Law':'other/legal',  'Animal':'other/living_thing/animal', 'Device':'other/product', 'Software':'other/product/software', 'Weapon':'other/product/weapon', 'ReligiousOrganisation':'other/religion', 'Scientist':'other/scientific', 'Sport':'other/sports_and_leisure', 'FictionalCharacter':'other/supernatural', 'Artist':'person/artist', 'Actor':'person/artist/actor', 'Writer':'person/artist/author', 'TelevisionDirector':'person/artist/director', 'MovieDirector':'person/artist/director', 'TheatreDirector':'person/artist/director', 'MusicalArtist':'person/artist/music', 'Athlete':'person/athlete', 'BusinessPerson':'person/business', 'Medician':'person/doctor', 'Lawyer':'person/legal', 'Judge':'person/legal', 'Politician':'person/political_figure', 'Cleric' : 'person/religious_leader','Religious':'person/religious_leader', 'OfficeHolder':'person/title', 'Person':'person', }
                    
 # Not present '':'location/structure/government',   '':'organization/stock_exchange', '':'other/health',  '':'other/living_thing',     '':'other/product/car', '':'other/product/computer',  '':'person/education', '':'person/education/student','':'person/education/teacher',
                    

with open(sys.argv[1], 'r') as f:
	for line in f:
		line = line.rstrip()
		elems = line.split('\t')
		start_offset = int(elems[2])
		stop_offset = int(elems[3])
		entity_start = 0
		entity_stop = 0 
		entity_start = elems[4][0:start_offset].count(' ')
		entity_stop = entity_start + elems[0].count(' ')
		elems[4] = re.sub(r'[0-9]','0', elems[4])
		tokens = elems[4].split(' ') 
		pos_tags = elems[5].split(' ')
		# Get the entity shape 
		entity_shape = remove_accents(elems[0])
		entity_shape = re.sub(r'[a-z]','a', entity_shape)
		entity_shape = re.sub(r'[A-Z]','A', entity_shape)
		entity_shape = remove_accents(entity_shape)
		# Get the type (this is where the classes are selected and must be mapped) 
		if elems[1] in types:
			type = types[elems[1]]
		else:
			continue
		# Get the head of the Chunk 
		start = int(elems[2])
		stop = int(elems[3])
		chunktags = pos_tags[int(entity_start):int(entity_stop)+1]
		chunk = tokens[int(entity_start):int(entity_stop)+1]
		head = ''
		nh = '_'
		for i, e in reversed(list(enumerate(chunktags))):
			if e.startswith('n'):
				head = chunk[i]
				del chunk[i]
			#nh = ' '.join(chunk)
			#	print(nh)
				break
		if head == '':
			head = chunk[0]
			del chunk[0]
		nh = ' '.join(chunk)
		nh = nh.rstrip()
		if nh == '':
			nh = "_"
		# To do:
		# character trigrams head word (should be easy) 
		trigraminput = "_" + head + "_"
		trigrams = word2ngrams(trigraminput)
		# Gather the context window 
		window_start = int(int(entity_start)) - 5
		window_before = []
		winb = '_'
		window_after = []
		wina = '_'
		if window_start < 0:
			 window_start = 0 
		for x in range(window_start, entity_start):
			window_before.insert(0, tokens[x])
		for i in window_before:
			if i.isalpha():
				winb = i
				break 
		window_end = int(int(entity_stop)+1) + 5
		if window_end > len(tokens):
			window_end = len(tokens) 
		for x in range(entity_stop+1, window_end):
			window_after.append(tokens[x])
		for i in window_after:
			if i.isalpha():
				wina = i
				break
		#for x in range(window_start, window_end):
		#	window = window + tokens[x] + ' ' 
		#window = window.replace(",", '=C=')
		# Print the whole shebang 
		#print(entity_start, entity_stop, elems[0],tokens,tokens[int(entity_start):int(entity_stop)+1], pos_tags[int(entity_start):int(entity_stop)+1])
		#print(current_start,current_stop,elements[3],elements[4])
		print("__label__"+ type + " , " + elems[0].replace(",", '=C=') + " , " + entity_shape.replace(",", '') + " , " + head.replace(",", '') + " , " + nh.replace(",", '') +  " , " +   winb + ", " + wina + ' , '+ ' '.join(trigrams).replace(",", "") )
		#print(elements[2] + "\t" + ','.join(elements[5:]).rstrip(',') + "\t"  + str(entity_start) + "\t" + str(entity_stop) + "\t" + text[current_start:current_stop].rstrip() + "\t" + postags + "\t0\t" + filename)
		#exit()
f.close()