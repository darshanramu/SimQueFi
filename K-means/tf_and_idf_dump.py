#!/usr/bin/python
import re, math
from collections import Counter
import sys
import pickle
import nltk.stem
 
stemmer_func = nltk.stem.snowball.EnglishStemmer().stem

def normalize_word(word):
    return stemmer_func(word.lower())

WORD = re.compile(r'\w+')
input_file = sys.argv[1]
def text_to_vector(text):
     words = WORD.findall(text)
     title_components = [normalize_word(word) for word in words] 
     #print Counter(words)
     return Counter(title_components)

def test_text_file_input(tf,vocab_set):
	with open(input_file,"r") as ipf:
		
		for line in ipf:
			tf.append(text_to_vector(line.lower()))
		#print vector_list
		#print "No.Of.Qs=",len(vector_list)
		for i in tf:
			[vocab_set.add(x) for x in i.keys()]
		#print vocab_set

def calculate_idf(tf,no_of_documents,vocab_set,idf):
	for word in vocab_set:
		for doc in tf:
			if word in doc:
				if idf.get(word):
					idf[word]+=1
				else:
					idf[word]=1
	for i in idf.keys():
		#print "word,value=",i,idf[i]
		x=float(no_of_documents)/idf[i]
		idf[i]=math.log10(1+x)
		
tf=[]
vocab_set=set()
test_text_file_input(tf,vocab_set)
no_of_documents=len(tf)
idf={}
calculate_idf(tf,no_of_documents,vocab_set,idf)
with open("tf_idf.dump","w") as out:
	#print tf
	#print idf
	dump_list=[tf,idf]
	#print dump_list
	pickle.dump(dump_list,out)

""" Place this in read dump file 	
with open("tf_idf.dump","r") as inf:
	new_dump=pickle.load(inf)
	print new_dump
"""
	

	
	
	
	
	
	
	
	
