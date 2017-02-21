#ck and dirty compute scores from fasttext output 

import sys 
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import precision_score	
from sklearn.metrics import classification_report 

y_gold = []
y_pred = []
with open(sys.argv[1], 'r') as f:
	for line in f:
		line = line.rstrip()
		elements = line.split("\t")
		if len(elements) < 1:
			continue
		if len(elements) < 2: 
			continue
		y_pred.append(elements[1].rstrip())
		y_gold.append(elements[0].rstrip())
f.close()

#tp = 0 	
#for idx, val in enumerate(y_gold):
#    print(val,y_pred[idx])
 #   if val == y_pred[idx]:
 #   	tp = tp + 1 
print(len(y_pred), len(y_gold))
#print(tp) 
#if y_pred[0] == y_gold[0]:	
#	print(y_pred[0],y_gold[0])
#else:
#	print("WTF")	
	
level2_labels = ["art","artist","athlete","body_part","business","celestial","city","company","country","currency","doctor","education","event","food","geography","government","health","heritage","legal","living_thing","military","park","political_figure","political_party","product","religion","scientific","sports_and_leisure","sports_team","stock_exchange","structure","supernatural","title","transit"]	
	
#macro = precision_score(y_gold, y_pred, average='macro')
#micro = precision_score(y_gold, y_pred, average='micro')
#weighted = precision_score(y_gold, y_pred, average='weighted')
macro = precision_recall_fscore_support(y_gold, y_pred, average='macro') #, labels=level2_labels)
print("Macro: ", macro)
micro = precision_recall_fscore_support(y_gold, y_pred, average='micro') # , labels=level2_labels)
print("Micro: ", micro)
weighted = precision_recall_fscore_support(y_gold, y_pred, average='weighted') # , labels=level2_labels)
print("Weighted: ", weighted)
print(classification_report(y_gold, y_pred))

