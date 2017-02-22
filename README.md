Multilingual Entity Typing 
====================

This repo contains the scripts to generate a fine-grained entity typing system for Dutch and Spanish as described in Multilingual Fine-Grained Entity Typing (currently under review) 

Prerequisites:
* Python3
	* BeautifulSoup 
	* NLTK3 
	* Scikit-learn 
* https://github.com/attardi/wikiextractor (to clean up Wikipedia data)
* https://github.com/evanmiltenburg/Dutch-tagger (POS tagger for Dutch)
* https://github.com/alvations/spaghetti-tagger (POS tagger for Spanish) 
* https://github.com/facebookresearch/fastText (the machine learning library) 

Data used:

Dutch 
* https://dumps.wikimedia.org/nlwiki/20170201/nlwiki-20170201-pages-articles-multistream.xml.bz2
* http://downloads.dbpedia.org/2016-04/core-i18n/nl/instance_types_nl.ttl.bz2
* http://downloads.dbpedia.org/2016-04/core-i18n/nl/wikipedia_links_nl.ttl.bz2

Spanish
* https://dumps.wikimedia.org/eswiki/20170201/eswiki-20170201-pages-articles-multistream.xml.bz2
* http://downloads.dbpedia.org/2016-04/core-i18n/es/instance_types_es.ttl.bz2
* http://downloads.dbpedia.org/2016-04/core-i18n/es/wikipedia_links_es.ttl.bz2


What's in this package
==================

In Processing, you find the scripts and instructions to generate the training and test datasets 

In Experiments, you find the scripts and setup of the Dutch and Spanish experiments



Contact: marieke.van.erp@vu.nl 
