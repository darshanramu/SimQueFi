#!/usr/bin/python
import sys
import pickle 
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
import pdb


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
    return list(words)

def vectorspaced_t(title,l_no,words,dict_tf_idf):
    title_components = [normalize_word(word) for word in title.split()]
    vectors=[] 
    for word in words:
        if word not in stopwords and word in title_components and word in dict_tf_idf[1]:
            vectors.append(float(dict_tf_idf[1][word]))
        else:
            vectors.append(float("0"))
    x = numpy.array(vectors)	
    return x
    

def vectorspaced(title,l_no,words,dict_tf_idf):
    title_components = [normalize_word(word) for word in title.split()]
    vectors=[] 
    for word in words:
        if word not in stopwords and word in title_components and word in dict_tf_idf[1]:
            vectors.append(float(dict_tf_idf[0][l_no][word] * dict_tf_idf[1][word]))
        else:
            vectors.append(float("0"))
    x = numpy.array(vectors)	
    return x
    
def ClusterQuestions(args):
    qs_dict_test = {}	
    qs_dict = {}    
    with open("../K-means/Question_Map","r") as qm1:
		qs_dict = pickle.load(qm1)    

    with open("Question_Map_Test","r") as qm:
    #with open("../K-means/Question_Map","r") as qm:    
		qs_dict_test = pickle.load(qm)			 
    filename = 'SuperQuestionSet_PosTagged_Test.txt'
    #filename = 'sup'        
    
    if len(args) >= 2:
        filename = args[1]

    with open("../K-means/SuperQuestionSet_PosTagged.txt") as title_file:    
        job_titles1 = [line.strip() for line in title_file.readlines()]
         
        words = get_words(job_titles1)    
    with open(filename) as title_file:
        job_titles = [line.strip() for line in title_file.readlines()]
          	
        with open("../K-means/tf_idf.dump","r") as inf:
	        dict_tf_idf=pickle.load(inf)
	
        with open("../K-means/kMeansModel.km",'rb') as f:
		clus = pickle.load(f)  
        cluster=clus["cl"]
        main_cluster_dict = clus["QuestMap"]        
     
        # NOTE: This is inefficient, cluster.classify should really just be
        # called when you are classifying previously unseen examples!
        
        classified_examples = [
                cluster.classify(vectorspaced_t(title,i,words,dict_tf_idf)) for i,title in enumerate(job_titles)
            ]

        # cluster 
         
        chart = plt.figure()
        splot = chart.add_subplot(111)

        x = classified_examples
	cols = len(cluster.means())
        splot.hist(x,cols,color='green',alpha=0.6)
        QuestMap={};
        qId=0
        #pdb.set_trace()
        ar=sorted(zip(classified_examples, job_titles))
        for cluster_id, title in ar:
                title=title.split()   
                print title  
                QuestMap[qId]={}
                QuestMap[qId]["Question"]=qs_dict_test[title[0]] 
                QuestMap[qId]["Sims"]=[]		
                question_array = main_cluster_dict[cluster_id]
                question_array.append(qs_dict_test[title[0]])
                
                file1 = open("Temp_tf_idf_File","w")
                for line in question_array:
                        file1.write(line)
                file1.close()       
                os.system("./tf_and_idf_dump.py "+" Temp_tf_idf_File")        
                
                with open("tf_idf.dump","r") as inf:
	                dict_tf_idf=pickle.load(inf)        
                
                
                words_newarray = get_words(question_array)        
                lenght_cluster = len(question_array)
                no_of_new_clusters = 1
                if 0 == lenght_cluster/5:
                	no_of_new_clusters = 1
		else:
                        no_of_new_clusters = (lenght_cluster/5)
                new_cluster = KMeansClusterer(no_of_new_clusters, cosine_distance,repeats = 10,avoid_empty_clusters=True)
                #print  question_array
                varr=[]
                for i,title_new in enumerate(question_array):
                        if title_new:
                                varr.append(vectorspaced(title_new,i,words_newarray,dict_tf_idf))
                print "reclsuter"
                clusters =  new_cluster.cluster(varr,True)   
                print "reclsuter1"             
                res=sorted(zip(clusters, question_array))
                
                #get test Q's cluster ID:
                cid=-1
                for cluster_id_newcluster, title_newcluster in res:
       		        title_newcluster=title_newcluster.split()            
		        if title_newcluster[0]==title[0]:
                                cid=cluster_id_newcluster
                                break
                
                for cluster_id_newcluster, title_newcluster in res:
       		        if cid==cluster_id_newcluster:
       		                title_newcluster=title_newcluster.split()
                                if title_newcluster[0] in qs_dict:
                                        QuestMap[qId]["Sims"].append(qs_dict[title_newcluster[0]])
                print "###"
                
                qId+=1
        pprint.pprint(QuestMap)
        plt.show()    
if __name__ == '__main__':

    ClusterQuestions(sys.argv)
