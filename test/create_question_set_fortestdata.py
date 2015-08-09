#!/usr/bin/python

import os
import sys
import re
import pickle
if(len(sys.argv) == 3):
	input_file = str(sys.argv[1])
	output_file = str(sys.argv[2])
else:
	input_file="test.in"
	output_file="SuperQuestionSet_Test.txt"

no_of_files=0
tf = open(output_file,"w")
no_of_q = 0
qs_dict_test={}
with open(input_file.replace('\n',''),"r") as fh:
	for singleline in fh:
		no_of_q+=1
		contents = singleline
		id='qtid:'+str(no_of_q)
		tf.write(id+" "+contents)
		qs_dict_test[id]=id+' '+contents
	
with open("Question_Map_Test","w") as qm:
	pickle.dump(qs_dict_test,qm)	


			


