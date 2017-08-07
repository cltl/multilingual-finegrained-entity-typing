#!/usr/bin/python 

# This is a wrapper for the entity typing system. It assumes a directory that contains 
# NAF files with at least an entity and terms layer. It reads the entities from the 
# entities layer and adds entity type information 

# date: 7 August July 2017
# author: marieke.van.erp@vu.nl

from KafNafParserPy import *
import sys 
import datetime
import nltk 
import unicodedata
import fasttext
import operator
import argparse 
import glob 

parser = argparse.ArgumentParser()

parser.add_argument('-d', nargs=1, help='Provide a directory with NAF files with entity layer (compulsory).', dest='dir', required=True)
parser.add_argument('-m', nargs=1, help='Specify the model to use (compulsory)', dest='modelfile', required=True)
parser.add_argument('-n', nargs=1, help='Take the NER type into account as well: y or n. Default is n.', dest='nertype', default=['n'])
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
 
args = parser.parse_args()

# load the model 
try:
	model = fasttext.load_model(args.modelfile[0])
except:
	print("Check the values of options -f and -m or request additional help with -h")
	exit(0)
	
def word2ngrams(text, n=3, exact=True):
	return ["".join(j) for j in zip(*[text[i:] for i in range(n)])]

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

# read in the directory and process each file in turn 

for file in glob.glob(args.dir[0] + '*.naf'):
	infile = open(file, 'r')
	outfile = file[0:-4] + "_finegrainedEntities.naf"
	my_parser = KafNafParser(infile)

	# Gather all words 
	words = {}
	for word in my_parser.get_tokens():
		words[word.get_id()] = word.get_text()
	
	# Gather all terms 
	terms = {}
	term_pos = {} 
	sent = {} 
	for term in my_parser.get_terms():
		terms[term.get_id()] = ""
		term_pos[term.get_id()] = term.get_pos()
		for span in term.get_span():
			terms[term.get_id()] =  terms[term.get_id()] + words[span.get_id()] + " "

	# get entities and store them into a dictionary  
	spans = {}	
	pos_tags = {} 
	types = {}
	entity_mention = {} 
	entity_start = ""
	entity_end = ""
	entity_type = ""
	for entity in my_parser.get_entities():
		#print(entity, entity.get_type())
		if entity.get_type() == 'MISC':
			entity_type = 'other'
		else:
			entity_type = entity.get_type().lower()
		# get the entity tokens and generate the feature vectors 	
		for reference in entity.get_references():
			idx = 0
			for span in reference.get_span():
				if idx is 0:
					entity_mention[entity.get_id()] = []
					entity_start = span.get_id()
					entity_mention[entity.get_id()].append(terms[span.get_id()])
					# and store the pos tags 
					pos_tags[entity.get_id()] = [] 
					pos_tags[entity.get_id()].append(term_pos[span.get_id()])
				else:
					entity_mention[entity.get_id()].append(terms[span.get_id()])
					pos_tags[entity.get_id()].append(term_pos[span.get_id()])
					entity_end = span.get_id()				
				idx=+1 
	
		# Vector:
		# label, entity, entity_shape, entity_head, entity_non_head, word before, word after, entity character trigrams 
		label = "__label__UNK"
		# entity 
		entity_string = " ".join(entity_mention[entity.get_id()])
		# shape 
		entity_shape = remove_accents(entity_string)
		entity_shape = re.sub(r'[a-z]','a', entity_shape)
		entity_shape = re.sub(r'[A-Z]','A', entity_shape)
		entity_shape = remove_accents(entity_shape)
		# head & non-head 
		chunktags = pos_tags[entity.get_id()]
		chunk = entity_mention[entity.get_id()]
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
		# word before 
		get_word_before = "t_" + str(int(entity_start.replace("t_", "")) - 1)
		try: 
			word_before = terms[get_word_before]
		except:
			word_before = ""
		# word after 
		get_word_after = "t_" + str(int(entity_end.replace("t_", "")) + 1)
		try: 
			word_after = terms[get_word_after]
		except:
			word_after = ""
		# entity character trigrams 
		trigraminput = "_" + head + "_"
		trigrams = word2ngrams(trigraminput)
		# print the whole shebang to a temp file 
		vector =  entity_string.replace(",", '=C=') + " , " +   entity_shape.replace(",", '') + " , " +  head.replace(",", '') + " , " +  nh.replace(",", '') + " , " +  word_before.replace(",", '') + " , " +  word_after.replace(",", '') + " , " +  " ".join(trigrams).replace(",", '') 
		# query the model and assign a fine-grained type 
		labels = model.predict_proba(vector)
		label_dict = {} 
		maximum = ""
		for x in labels:
			if x[0][0] in label_dict:
				if x[0][1] > label_dict[x[0][0]]:
					label_dict[x[0][0]] = x[0][1]
			else:
				label_dict[x[0][0]] = x[0][1]
		# In case the entity types from the NER module are taken into account, the retrieved 
		# entity types will be filtered on the top level, e.g. if the NER classifier assigned
		# 'person' then only subtypes of 'person' will be returned 
		if args.nertype[0] == 'y':
			to_keep = {}
			for finetype in label_dict:
				if entity_type in finetype:
					to_keep[finetype] = label_dict[finetype]
			# if the main type is not present in the types returned by the finegrained 
			# entity typing system, the highest scoring type is returned. 
			if len(to_keep) > 0:
				maximum = max(to_keep, key=to_keep.get)
			else:
				maximum = max(label_dict, key=label_dict.get)
		# When the entity types from the NER module is not taken into account, the type with 
		# the highest confidence from the finegrained system is returned 
		else:
			maximum = max(label_dict, key=label_dict.get)
		# This is the part where you create a new reference with the type information 
		my_ext_ref = CexternalReference()
		my_ext_ref.set_reference(maximum)
		my_ext_ref.set_resource('finegrained-entity-typing')
		my_ext_ref.set_confidence(str(label_dict[maximum]))
		entity.add_external_reference(my_ext_ref)


	## Create header info
	lp = Clp()
	lp.set_name('vua-multilingual-finegrained-entity-typing')
	lp.set_version('1.0')
	lp.set_timestamp()
	my_parser.add_linguistic_processor('entities', lp)

	# And print the output 
	my_parser.dump(outfile)
	