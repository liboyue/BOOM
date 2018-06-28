from .Tiler import Tiler

from nltk.tokenize import sent_tokenize, word_tokenize

'''
@Author: Khyathi Raghavi Chandu
@Date: October 17 2017

This code contains the implementation of Abstract method for Tiler.
'''

'''
This is a subclass that extends the abstract class Tiler.
'''
class Concatenation(Tiler):

	#Abstract method from Tiler class that takes a list of sentences as arguments and returns the final summary in a single string.
	def tileSentences(self, sentences, pred_length=200):
		length = 0
		summaryFinal = ""
		for sentence in sentences:
			#BioAsq ideal generation guideline imposes an upper word limit of 200. The following command maintains that restriction.
			if (len(word_tokenize(sentence)) + length) <= pred_length:
					summaryFinal += sentence
					length += len(word_tokenize(sentence))

		return summaryFinal

'''
instance = Concatenation()
print instance.tileSentences(["John"," has cancer"])
'''
