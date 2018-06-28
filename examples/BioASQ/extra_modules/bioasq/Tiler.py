import abc
from abc import abstractmethod

'''
@Author: Khyathi Raghavi Chandu
@Date: October 17 2017

This code contains the abstract class for Tiler.
'''


'''
This is an Abstract class that serves as a template for implementations for tiling sentences.
Currently there is only one technique implemented which is simple concatenation.
'''
class Tiler(object):
	__metaclass__ = abc.ABCMeta
	@classmethod
	def __init__(self):
		pass
	
	#abstract method that should be implemented by the subclass that extends this abstract class
	@abstractmethod
	def tileSentences(self, sentences, pred_length):
		pass
	

'''
instance = Tiler(["John"," has cancer"])
print instance.sentenceTiling()
'''
