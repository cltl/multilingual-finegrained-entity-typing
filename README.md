Multilingual Entity Typing 
====================

This repo contains the scripts to generate a fine-grained entity typing system for Dutch and Spanish as described in Multilingual Fine-Grained Entity Typing (Presented at: http://ldk2017.org/)

When using this package in a publication, please cite:
van Erp M., Vossen P. (2017) [Multilingual Fine-Grained Entity Typing][https://link.springer.com/chapter/10.1007%2F978-3-319-59888-8_23]. In: Gracia J., Bond F., McCrae J., Buitelaar P., Chiarcos C., Hellmann S. (eds) Language, Data, and Knowledge. LDK 2017. Lecture Notes in Computer Science, vol 10318. Springer, Cham

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

Pre-trained models
===============
The pre-trained models generated for this paper can be found at:
http://kyoto.let.vu.nl/multilingual-entity-typing/

To run those, you need to format your input data as a CSV file with the following columns:
label, entity mention, entity shape, head of the entity phrase, non-head words entity phrase, word before the entity, word after, entity head trigrams 

For example:
 
\_\_label\_\_Species , vliesvleugelig insect , aaaaaaaaaaaaaa aaaaaa , insect , vliesvleugelig , een, uit , \_in ins nse sec ect ct\_
\_\_label\_\_VideoGame , Unreal Tournament , Aaaaaa Aaaaaaaaaa , Tournament , Unreal , uitgebrachte, van ,\_To Tou our urn rna nam ame men ent nt\_

Note that fastText expects the label to start with "\_\_label\_\_" 

To do: create a wrapper that can do this so a normal text can be tagged. 

Contact: marieke.van.erp@vu.nl 
