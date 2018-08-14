from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from .SentenceOrderer import SentenceOrderer
import re, sys
import numpy as np


class KMeansOrderer(SentenceOrderer):

	def __init__(self):
		pass

	def setup(self, sentences, snippets=None, k=2, max_iter=10, max_tokens=300):
		self.k = k
		self.max_iter = max_iter
		self.max_tokens = max_tokens
		self.uniq_sentences = list(set(sentences))
		self.snippets = snippets
		self.sentences = []
		self.word_length = 0
		self.stopwords = set(stopwords.words('english'))
		for sentence in self.uniq_sentences:
			if self.word_length + len(word_tokenize(sentence)) <= self.max_tokens and len(sentence) > 3:
				self.sentences.append(sentence)
				self.word_length += len(word_tokenize(sentence))
		self.vocab_size, self.indices = self.index()

	def index(self):
		word_count = 0
		word2idx = {}

		for sentence in self.sentences:
			for word in sentence.split(' '):
				token = re.sub(r'\W+', '', word).lower()
				if token not in self.stopwords and token != '':
					if token not in word2idx:
						word2idx[token] = word_count
						word_count += 1
		return word_count, word2idx

	def vectorize(self):
		vecs = []
		for sentence in self.sentences:
			arr = np.zeros(self.vocab_size, dtype=np.int8)
			for word in sentence.split(' '):
				token = re.sub(r'\W+', '', word).lower()
				if token not in self.stopwords and token != '':
					arr[self.indices[token]] += 1
			vecs.append(arr)
		return vecs

	def kmeans(self, vecs):
		pairs = list(zip(vecs, range(0, len(vecs))))

		centroid_all = np.mean(vecs, axis=0)

		centroids = vecs[-self.k:]
		for i in range(0, self.max_iter):
			clusters = []
			for j in range(0, self.k):
				clusters.append([])

			for pair in pairs:
				min_dist = 2.0
				min_centroid = -1
				for j in range(0, len(centroids)):
					dist = np.cos(pair[0], centroids[j])
					if dist < min_dist:
						min_dist = dist
						min_centroid = j
				clusters[min_centroid].append(pair)
			for j in range(0, self.k):
				arr = list(map(lambda x: x[0], clusters[j]))
				centroids[j] = np.mean(arr, axis=0)

		ordered_sentences = []
		ordered_clusters = sorted(clusters, key=lambda x: cosine(centroid_all, np.mean(list(map(lambda y: y[0], x)), axis=0)))
		for i in range(0, len(ordered_clusters)):
			for j in sorted(ordered_clusters[i], key=lambda x: cosine(x[0], centroids[i])):
				ordered_sentences.append(j)

		return ordered_sentences

	def toText(self, clusters):
		result = []
		for c in clusters:
			result.append(self.sentences[c[1]])
		return result

	def orderSentences(self, sentences, snippets=None, k=2, info_dict={'k':2,'max_iter':10,'max_tokens':300}):
		self.setup(sentences, snippets, k, info_dict['max_iter'],
		           info_dict['max_tokens'])

		if len(self.sentences) < 2:
			return self.tileSentences(self.sentences)
		vecs = self.vectorize()
		clusters = self.kmeans(vecs)
		return self.toText(clusters)
