from Expander import Expander

import logging
from logging import config

'''
@Author: Khyathi Raghavi Chandu
@Date: October 17 2017

This code returns the sentence passed as argument without any concept expansion.
'''

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('bioAsqLogger')

#This is a subclass that extends the abstract class Expander.
class NoExpander(Expander):

	#The abstract method from the base class is implemeted here to return a string of the original sentence without any expansion.
	def getExpansions(self, sentence):
		logger.info('In getExpansions function of NoExpander')
		l =list(set(sentence.strip().split()))
		return sentence

#Since the abstract method from the base class Expander is implemented, uncommenting the following lines will allow this code to run
#Unit Testing to check the working of NoExpander class
'''
instance = NoExpander()
print instance.getExpansions("John has cancer")
'''