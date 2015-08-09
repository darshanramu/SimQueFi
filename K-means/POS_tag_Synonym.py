#!/usr/bin/python
import nltk
import sys
from GetSynonyms import GetSynonyms
import re,pdb,pickle

stopwords = set(nltk.corpus.stopwords.words('english'))
stop_list=['what','how','to','a','the','find','can','could','should','i']
for i in stop_list:
	stopwords.add(i)


synonym = {}
regular = re.compile("^V.*")
	
try:
	if len(sys.argv) == 1:		 	
		file1 = open("SuperQuestionSet.txt","r")
	else:
		file1 = open(sys.argv[1],"r")
except FileNotFoundError:
	print "File to read from does not exist"
	sys.exit()

try:
	file2 = open("SuperQuestionSet_PosTagged.txt","w")
except FileNotFoundError:
	print "File to write from does not exist"
	sys.exit()

j = 0
iCounter=1
for line in file1:
	tokens = nltk.word_tokenize(line)
	#print line
	tag = nltk.pos_tag(tokens)
	arg = []
	l = []
	flag = 0
	if iCounter%250==1:
	        print "Processed lines: "+str(iCounter)	
	iCounter+=1		
	for i in range(0,len(tag)):		
		if (tag[i][1] == "JJ" or regular.match(tag[i][1])) and tag[i][0] not in stopwords:
			if tag[i][0] not in synonym:				
				# ignoring the first position	
				arg=[" ",1,tag[i][0],tag[i][1][0]]
				
				#print arg
				#pdb.set_trace()
				l = GetSynonyms(arg)
				synonym[tag[i][0]] = "X"+str(j)
				flag = 1				
				newword = "X"+str(j)				
				#print tag[i][0],j
				# Now add synonyms of the given words into the synonym dictionary 				
				if len(l) != 0:
					for word in l:
						#print word
						word_split = word.split(" ")						
						# for each word we need to check if it already exists in the dictionary else add it
						if word_split[0] not in synonym:
							synonym[word_split[0]] = "X"+str(j)
							#print word,j			
				# initialising arg list	and l
				
				j = j + 1
			else:
				# if the word is already present use the previous tag
				flag = 1				 				
				newword = synonym[tag[i][0]]	
		if flag == 1:			
			file2.write(bytes(newword))	
		else:
			file2.write(bytes(tag[i][0]))		
		#file2.write(bytes("/"))	
		#file2.write(bytes(tag[i][1]))
		file2.write(bytes(" "))
		flag = 0
	file2.write(bytes("\n"))
        
with open("Synonym_Map.km","wb") as qm:
        pickle.dump(synonym,qm)
        
file1.close()
file2.close()
