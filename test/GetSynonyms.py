#!/usr/bin/python
import xml.etree.ElementTree as ET
import sys,pdb,urllib
from nltk.corpus import wordnet as wn

def getForm(form):
        if form=="0":
                return "0"
        if form=="JJ":
                return "adjective"
        if form=="V":
                return "verb"      

def GetSynonyms(arg):
        synonymList=[]
        service=1
        form="0"
        service=int(arg[1])
        #pdb.set_trace()
        if len(arg) > 3:
                form=arg[3]
        
        formType=getForm(form)
        
        
        if service==1:
                serviceurl = 'http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/'+arg[2]+'?key=3d90b21c-2e74-4f9d-abc8-962904de14ce'     
                res = urllib.urlopen(serviceurl)
                data = res.read()  
                xmlDoc = ET.fromstring(data)
                entries=xmlDoc.findall("entry")
                for entry in entries:
                        tag=entry.find("fl")
                        
                        if tag.text==formType:
                        
                                sens= entry.find("sens")
                                sen= sens.find("syn")
                                synonymList.extend(sen.text.split(","))
                                break
              #  print data    
        
        if service==2:
                syns=wn.synsets(arg[2])
                for syn in syns:
                        #print syn
                        if syn:
                               lems=syn.lemma_names('eng')
                               if lems:
                                       synonymList.extend(lems)
        
        print (synonymList)
        return synonymList
if __name__ == '__main__':
        if len(sys.argv)<2:
                print("Parameter expected")   
        else:        
                GetSynonyms(sys.argv)
 
