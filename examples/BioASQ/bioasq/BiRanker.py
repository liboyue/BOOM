import abc
from abc import abstractmethod

from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

'''
@Author: Khyathi Raghavi Chandu
@Date: October 17 2017

This code contains the abstract class for the BiRanker.
'''

'''
This is an Abstract class that serves as a template for implementations for:
ranking among sentences and ranking with question.
'''
class BiRanker(object):
	__metaclass__ = abc.ABCMeta
	@classmethod
	def __init__(self):
		self.alpha = 0.5
		self.numSelectedSentences = 10

	@abstractmethod
	def getRankedList(self):
		pass

	@classmethod
	def getSentences(self, question):

		sentences = []
		snippetsText = []
		for snippet in question['snippets']:
			text = snippet
			snippetsText.append(text)
			if text == "":
				continue
			try:
				sentences += sent_tokenize(text)
			except:
				sentences += text.split(". ") # Notice the space after the dot
		return sentences

	@classmethod
	def computePositions(self,snippets):
		pos_dict = {}
		max_rank = len(snippets)
		rank = 0
		for snippet in snippets:
			snippet = snippet
			more_sentences = [i.lstrip().rstrip() for i in sent_tokenize(snippet)]

			for sentence in more_sentences:
				if sentence not in pos_dict:
				  pos_dict[sentence] = 1-(float(rank)/max_rank)
			rank += 1

		return pos_dict
