#!/usr/bin/python
import sys
import pickle,pdb
import numpy
from nltk.cluster import KMeansClusterer, GAAClusterer, euclidean_distance, cosine_distance
import nltk.corpus
from nltk import decorators
import nltk.stem
import os
import pprint 
import re
from scipy import cluster
from matplotlib import pyplot as plt


stemmer_func = nltk.stem.snowball.EnglishStemmer().stem
stopwords = set(nltk.corpus.stopwords.words('english'))
stop_list=['what','how','to','a','the','find','can','could','should','i']
for i in stop_list:
	stopwords.add(i)
#print stopwords
 
def normalize_word(word):
    return stemmer_func(word.lower())
WORD = re.compile(r'\w+') 
def get_words(job_titles):
    words = set()
    for title in job_titles:
    	title = WORD.findall(title)
        for word in title:
            
            words.add(normalize_word(word))
    #print "hello",list(words)
    return list(words)
 
def vectorspaced(title,l_no,words,dict_tf_idf):
    title_components = [normalize_word(word) for word in title.split()]
    vectors=[] 
    for word in words:
        if word not in stopwords and word in title_components:
            vectors.append(float(dict_tf_idf[0][l_no][word] * dict_tf_idf[1][word]))
        else:
            vectors.append(float("0"))
    x = numpy.array(vectors)	
    #print x
    return x

def getDump(question_file):
    #print question_file
    os.system("./tf_and_idf_dump.py "+question_file)        
    
def ClusterQuestions(args):
    qs_dict = {}	
    with open("Question_Map","r") as qm:
		qs_dict = pickle.load(qm)			 
    filename = 'SuperQuestionSet_PosTagged.txt'
    dumpFile="tf_idf.dump"
    if len(args) >= 2:
        filename = args[1]
    if len(args)>=3:
        dumpFile=args[2]
    getDump(filename) 
    with open(filename) as title_file:
 
        job_titles = [line.strip() for line in title_file.readlines()]
         
        words = get_words(job_titles) 	
      	with open("ClusterCount","r") as cc:
      		no_of_clusters=pickle.load(cc)
        with open(dumpFile,"r") as inf:
	        dict_tf_idf=pickle.load(inf)
	        #pprint.pprint(dict_tf_idf)
        
        cluster = KMeansClusterer(no_of_clusters, cosine_distance,repeats = 10,avoid_empty_clusters=True)
        #cluster = GAAClusterer(4)
        print "Generating clusters"

        clusters =  cluster.cluster([vectorspaced(title,i,words,dict_tf_idf) for i,title in enumerate(job_titles) if title],True)
        
        # NOTE: This is inefficient, cluster.classify should really just be
        # called when you are classifying previously unseen examples!
        #classified_examples = [
        #        cluster.classify(vectorspaced(title,i,words,dict_tf_idf)) for i,title in enumerate(job_titles)
        #    ]
 
        # Saving the cluster:
        print "Generating graph"
        
        
       
        chart = plt.figure()
        splot = chart.add_subplot(111)

        #x = classified_examples
	x = clusters
        cols = len(cluster.means())
        splot.hist(x,cols,color='blue',alpha=0.6)
        
        QuestMap={}
        #print("Clustered as",clusters)
        for cluster_id, title in sorted(zip(clusters, job_titles)):
                
       		title=title.split()            
		
		if cluster_id in QuestMap:
		        QuestMap[cluster_id].append(qs_dict[title[0]])
		else:
		        QuestMap[cluster_id]=[qs_dict[title[0]]]
		
		
	clusObj={"cl":cluster,"cls":clusters,"QuestMap":QuestMap}	
        with open("kMeansModel.km",'wb') as f:
		pickle.dump(clusObj,f)
        plt.show()    
if __name__ == '__main__':

    ClusterQuestions(sys.argv)
