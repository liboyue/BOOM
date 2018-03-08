from Expander import Expander

from pymedtermino import *
from pymedtermino.umls import *
from pymetamap import MetaMap
from Authentication import *

from singletonConceptId import *

from flask import Flask, request, abort
import requests
import json
import diskcache as dc

import logging
from logging import config

'''
@Author: Khyathi Raghavi Chandu
@Date: October 17 2017

This code returns the sentence passed as argument with concept expansion from UMLS ontology.
'''

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('bioAsqLogger')

#This is a subclass that extends the abstract class Expander.
class UMLSExpander(Expander):

	#Credentails to access the REST API of UMLS
	def getCredentials(self):
		#umls authentication
		self.username = "khyathi"
		self.password = "Oaqa12#$"
		self.version = "2016AB"

	'''
	The abstract method from the base class is implemeted here to return a string of the original sentence with
	expansion from UMLS.
	This method takes a string as input and returns the expanded string as output.
	'''
	def getExpansions(self, sentence):
		self.getCredentials()
		self.AuthClient = Authentication(self.username,self.password)

		logger.info('In getExpansions function of UMLSExpander')
		#get TGT for our session
		self.tgt = self.AuthClient.gettgt()
		self.uri = "https://uts-ws.nlm.nih.gov"

		self.cache = SingletonUMLSCache.Instance().cache
		synonyms = []
		synonyms = sentence.strip().split()
		metaConcepts = self.getMetaConcepts(sentence)
		for mconcept in metaConcepts:
			try:
				for el in self.cache[mconcept]:
					synonyms.append(el)
				logger.info('Found UMLS Cached Concept: '+ str(mconcept.cui))
			except:
				try:
					termSyns = []
					logger.info('Getting concept expansions from UMLS')
					#metamap has direct mapping with UMLS based on Concept Unique Identification (CUI)
					cui = mconcept.cui
					content_endpoint = "/rest/content/"+str(self.version)+"/CUI/"+str(cui)
					query = {'ticket':self.AuthClient.getst(self.tgt)}
					r = requests.get(self.uri+content_endpoint,params=query)
					r.encoding = 'utf-8'
					items  = json.loads(r.text)
					jsonData = items["result"]
					try:
						query = {'ticket':self.AuthClient.getst(self.tgt)}
						#THE REST API returns a json object that includes other concepts with different relations
						r = requests.get(jsonData["relations"],params=query)
						r.encoding = 'utf-8'
						items = json.loads(r.text)
						jsonData = items["result"]
						for el in jsonData:
							'''
							This is how to access differennt relations in UMLS
							#if el['relationLabel'] == 'RL' or el['relationLabel'] == 'RQ':
							'''
							termSyns.append(el['relatedIdName'])
							synonyms.append(el['relatedIdName'])
						self.cache[mconcept] = termSyns
						logger.info('Parsed the JSON object returned from UMLS')
					except Exception as e:
						logger.debug('Exception in UMLS Expansion '+ str(e))
						pass
				except:
					pass
		#class method of Expander that stops the metamap
		#self.stopMetaMap()
		listSynonyms = list(set(synonyms))
		ExpandedSentence = ' '.join(listSynonyms)
		return ExpandedSentence



#Since the abstract method from the base class Expander is implemented, uncommenting the following lines will allow this code to run.
#Unit Testing to check the working of UmlsExpander class
'''
instance = UMLSExpander()
print instance.getExpansions("John has cancer")
'''