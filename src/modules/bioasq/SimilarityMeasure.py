from nltk import word_tokenize
from nltk.corpus import stopwords

class SimilarityMeasure(object):
	def __init__(self, sentence1, sentence2):
		self.sentence1 = sentence1
		self.sentence2 = sentence2
		self.stopWords = set(stopwords.words('english'))

	def calculateSimilarity(self):
		pass
	
