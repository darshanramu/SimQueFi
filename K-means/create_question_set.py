#!/usr/bin/python

import os
import sys
import re
import pickle
if(len(sys.argv) == 3):
	input_file = str(sys.argv[1])
	output_file = str(sys.argv[2])
else:
	input_file="../Database/"
	output_file="SuperQuestionSet.txt"

no_of_files=0
tf = open(output_file,"w")
no_of_q = 0
qs_dict={}
for line in sorted(os.listdir(input_file)):
	with open(input_file+line.replace('\n',''),"r") as fh:
		for singleline in fh:
			no_of_q+=1
			#contents = singleline.decode('utf-8','replace').replace('\r\n','')
			contents = singleline
			id='qid:'+str(no_of_q)
			tf.write(id+" "+contents)
			qs_dict[id]=id+' '+contents
	
	no_of_files+=1

with open("Question_Map","w") as qm:
	pickle.dump(qs_dict,qm)	
	
with open("ClusterCount","w") as cc:
	pickle.dump(no_of_files,cc)	


			


