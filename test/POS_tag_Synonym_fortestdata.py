#!/usr/bin/python
import nltk
import sys
from GetSynonyms import GetSynonyms
import re,pdb
import pickle

stopwords = set(nltk.corpus.stopwords.words('english'))
stop_list=['what','how','to','a','the','find','can','could','should','i']
for i in stop_list:
	stopwords.add(i)


synonym = {}
regular = re.compile("^V.*")
	
try:
	if len(sys.argv) == 1:		 	
		file1 = open("SuperQuestionSet_Test.txt","r")
	else:
		file1 = open(sys.argv[1],"r")
except FileNotFoundError:
	print "File to read from does not exist"
	sys.exit()

try:
	file2 = open("SuperQuestionSet_PosTagged_Test.txt","w")
except FileNotFoundError:
	print "File to write from does not exist"
	sys.exit()

j = 0
for line in file1:
	synonym = {}	
	with open("../K-means/Synonym_Map.km","rb") as qm: 
		synonym = pickle.load(qm)

	tokens = nltk.word_tokenize(line)
	tag = nltk.pos_tag(tokens)
	flag = 0				
	for i in range(0,len(tag)):		
		if (tag[i][1] == "JJ" or regular.match(tag[i][1])) and tag[i][0] not in stopwords:
			if tag[i][0] in synonym:				
				newword = synonym[tag[i][0]]
				flag = 1					
		if flag == 1:			
			file2.write(bytes(newword))	
		else:
			file2.write(bytes(tag[i][0]))		
		file2.write(bytes(" "))
		flag = 0
	file2.write(bytes("\n"))

file1.close()
file2.close()
