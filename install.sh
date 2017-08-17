#!/bin/bash
# Installation commands for multilingual finegrained entity typing 
# August 2017
# Big thanks to Filip Ilievski 

if [ -z "$1" ]; then
    echo "No argument supplied. Please supply 'es' for Spanish, 'nl' for Dutch, or 'all' for both."
    exit
elif [ "$1" = "es" ]; then
    es=true
    nl=false
    echo "Preparing your installation for entity typing on Spanish"
elif [ "$1" = "nl" ]; then
    es=false
    nl=true
    echo "Preparing your installation for entity typing on Dutch"
elif [ "$1" = "all" ]; then
    es=true
    nl=true
    echo "Preparing your installation for both Dutch and Spanish"
else
    echo "Argument not recognized. Please supply 'es' for Spanish, 'nl' for Dutch, or 'all' for both."
    exit
fi

#Install python3 prerequisites
pip3 install Cython
pip3 install -r requirements.txt

#Clone external packages
git clone https://github.com/attardi/wikiextractor
#git clone https://github.com/facebookresearch/fastText


# DUTCH
if [ "$nl" = true ]; then
    # POS tagger for Dutch (only needed if you want to train your own model, then uncomment the next line) 
    #git clone https://github.com/evanmiltenburg/Dutch-tagger
    #Download data (uncomment the next three lines if you want to train your own models)
   # wget -nc https://dumps.wikimedia.org/nlwiki/20170201/nlwiki-20170201-pages-articles-multistream.xml.bz2
   # wget -nc http://downloads.dbpedia.org/2016-04/core-i18n/nl/instance_types_nl.ttl.bz2
   # wget -nc http://downloads.dbpedia.org/2016-04/core-i18n/nl/wikipedia_links_nl.ttl.bz2
    
    # Download models (if you don't want to train your own)
    wget -nc http://kyoto.let.vu.nl/multilingual-entity-typing/dutch_DBpedia_types_model.bin
    wget -nc http://kyoto.let.vu.nl/multilingual-entity-typing/dutch_GFT_Types_model.bin 

    # Test
    python3 NAFWrapper_file.py -f test/dutch.naf -m dutch_GFT_Types_model.bin
    python3 NAFwrapper_batch.py -d test/dutch/ -m dutch_GFT_Types_model.bin
fi


#SPANISH
if [ "$es" = true ]; then
    # POS tagger for Spanish (only needed if you want to train your own model, then uncomment the next line)
   # git clone https://github.com/alvations/spaghetti-tagger
    #Download data (uncomment the next three lines if you want to train your own models)
   # wget -nc https://dumps.wikimedia.org/eswiki/20170201/eswiki-20170201-pages-articles-multistream.xml.bz2
   # wget -nc http://downloads.dbpedia.org/2016-04/core-i18n/es/instance_types_es.ttl.bz2
   # wget -nc http://downloads.dbpedia.org/2016-04/core-i18n/es/wikipedia_links_es.ttl.bz2
    
    # Download models (if you don't want to train your own)
    wget -nc http://kyoto.let.vu.nl/multilingual-entity-typing/spanish_DBpedia_types_model.bin
    wget -nc http://kyoto.let.vu.nl/multilingual-entity-typing/spanish_GFT_model.bin

    # Test
    python3 NAFWrapper_file.py -f test/spanish.naf -m spanish_GFT_model.bin
    python3 NAFwrapper_batch.py -d test/spanish/ -m spanish_GFT_model.bin
fi
