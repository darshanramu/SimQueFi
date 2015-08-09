#!/usr/bin/python
import sys
from wordnik import *

word = sys.argv[1]
#wordnik url
apiUrl = 'http://api.wordnik.com/v4'
#To test the words, temp api key
apiKey = '70538348db6b42e43a5181e32070feebc0b303e293ed13a97'

client = swagger.ApiClient(apiKey, apiUrl)
wordApi = WordApi.WordApi(client)

definitions = wordApi.getDefinitions(word,
                                     partOfSpeech='verb',
                                     sourceDictionaries='wiktionary',
                                     limit=1)
print definitions[0].text
"""
word_syn = wordApi.getTopExample(word)
print word_syn.text
"""
