import abc
from abc import abstractmethod

import os
from pymedtermino import *
from pymedtermino.snomedct import *
from pymedtermino.umls import *
from pymetamap import MetaMap

from singletonConceptId import *

import logging
from logging import config

'''
@Author: Khyathi Raghavi Chandu
@Date: October 17 2017

This is an Abstract Class to perform Concept Expansions. This class cannot be instantiated as all the abstract methods are not
implemented.
The subclass that extends the abstract class is valid if and only if all the abstract methods are implemented.
'''

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('bioAsqLogger')

class Expander:
	__metaclass__ = abc.ABCMeta
	@classmethod
	def __init__(self): #constructor for the abstract class
		pass

	#This is the abstract method that is implemented by the subclasses.
	@abstractmethod
	def getExpansions(self,sentence):
		pass
	
	#Given a sentence as input, this method gives a list of all the biomedical concepts identified by the metamap
	@classmethod
	def getMetaConcepts(self, sentence):
		logger.info('retrieving meta concepts from MetaMap')
		try:
			sents = [sentence]
			cuiList = []
			#Following line is an example of how the variable sents (string) has to be passed into extract_concepts as a list.
			#sents = ['John had a leukemia']# and heart attack']
			self.mm = SingletonMetaMap.Instance().mm
			metaConcepts,error = self.mm.extract_concepts(sents,[1,2])
			return metaConcepts
		except Exception as e:
			logger.debug('Metamap exception '+ str(e))
			return []


#If this part is uncommented in the code and run then it should throw an error because the abstract methods are not implemented.
'''
instance = Expander("John has cancer")
print instance.getExpansions()
'''
