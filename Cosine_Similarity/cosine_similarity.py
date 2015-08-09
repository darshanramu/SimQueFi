#!/usr/bin/python
import re, math
from collections import Counter

WORD = re.compile(r'\w+')

#Cosine similarity measure
# cos(0) = a.b / ||a|| ||b||

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     print intersection
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([(vec1[x])**2 for x in vec1.keys()])
     sum2 = sum([(vec2[x])**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)
     #print denominator
     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def get_cosine_idf(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     print intersection
     numerator = sum([vec1[x]*idf[x] * vec2[x]*idf[x] for x in intersection])

     sum1 = sum([(vec1[x]*idf[x])**2 for x in vec1.keys()])
     sum2 = sum([(vec2[x]*idf[x])**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)
     #print denominator
     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     #print Counter(words)
     return Counter(words)

def test_small_input():
	#The value is not so accurate since only tf is used as features 
	text1 = 'Find the least value in an array'
	text2 = 'Find the minimum element in the array'
	text3 = 'Find the maximum value in an array'
	text4 = 'Find the smallest element in the array'
	text5 = 'Find the largest element in the linked list'

	vector1 = text_to_vector(text1)
	vector2 = text_to_vector(text2)
	vector3 = text_to_vector(text3)
	vector4 = text_to_vector(text4)
	vector5 = text_to_vector(text5)

	print 'Cosine: 1 & 2', get_cosine(vector1, vector2)
	print 'Cosine: 1 & 4', get_cosine(vector1, vector4)
	print 'Cosine: 1 & 3', get_cosine(vector1, vector3)
	print 'Cosine: 3 & 4', get_cosine(vector3, vector4)
	print 'Cosine: 2 & 4', get_cosine(vector2, vector4)
	print 'Cosine: 1 & 5', get_cosine(vector1, vector5)
	print 'Cosine: 2 & 5', get_cosine(vector2, vector5)
	print 'Cosine: 3 & 5', get_cosine(vector3, vector5)
	print 'Cosine: 4 & 5', get_cosine(vector4, vector5)

#test_small_input()

def test_text_file_input(vector_list,vocab_set):
	with open("sample_questions_for_cos_sim.txt","r") as ipf:
		
		for line in ipf:
			vector_list.append(text_to_vector(line))
		print vector_list
		print "No.Of.Qs=",len(vector_list)
		for i in vector_list:
			[vocab_set.add(x) for x in i.keys()]
		print vocab_set

def calculate_idf(vector_list,no_of_documents,vocab_set,idf):
	for word in vocab_set:
		for doc in vector_list:
			if word in doc:
				if idf.get(word):
					idf[word]+=1
				else:
					idf[word]=1
	for i in idf.keys():
		print "word,value=",i,idf[i]
		x=float(no_of_documents)/idf[i]
		idf[i]=math.log10(1+x)
		
vector_list=[]
vocab_set=set()
test_text_file_input(vector_list,vocab_set)
no_of_documents=len(vector_list)
idf={}
calculate_idf(vector_list,no_of_documents,vocab_set,idf)
print idf	
print 'Cosine: 1 & 2',vector_list[1], vector_list[2], get_cosine_idf(vector_list[1], vector_list[2])	
	
	
	
	
	
	
	
	
