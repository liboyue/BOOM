from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from src.bioasq_modules.SentenceOrderer import SentenceOrderer
from scipy.spatial.distance import cosine
import re, sys
import numpy as np


# TODO: Should we account for sentence length somehow? Seems like longer sentences will be heavily advantaged.
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
					dist = cosine(pair[0], centroids[j])
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

	def orderSentences(self, sentences, snippets=None, info_dict={'k':2,'max_iter':10,'max_tokens':300}):
		self.setup(sentences, snippets, info_dict['k'], info_dict['max_iter'],
		           info_dict['max_tokens'])

		if len(self.sentences) < 2:
			return self.tileSentences(self.sentences)
		vecs = self.vectorize()
		clusters = self.kmeans(vecs)
		return self.toText(clusters)

# Unit Test
"""
sentences = ['Although not definitive, available data suggest an association between the use of hormone replacement therapy and increased meningioma risk.', 'BACKGROUND: Previous studies on association of exogenous female sex hormones and risk for meningioma have yielded conflicting results.', 'There was no significant difference between glioma and meningioma risk in users of estrogen-only HT.', 'Among women who had been using estradiol-only therapy for at least 3 years, the incidence of meningioma was 1.40-fold higher (95% confidence interval: 1.18, 1.64; P<0.001) than in the background population.', 'Estradiol-only therapy was accompanied with a slightly increased risk of meningioma.', 'A retrospective study including more than 350,000 women, about 1400 of whom had developed meningioma, showed that the risk of meningioma was about twice as high in users of postmenopausal hormone replacement therapy as in non-users.', 'Likewise, risk of meningioma was only weakly associated with past use of HRT (OR = 0.7, 95% CI 0.4 - 1.3), and not at all with current use of HRT (OR = 1.0, 95% CI 0.5 - 2.2).', 'Results from several prospective, large-scale studies indicate that postmenopausal hormone therapy may increase the risk for diagnosing meningioma by 30-80%, but there is no effect in regard to glioma.', 'The increased odds ratios with African Americans was retained in post-menopausal women, while the protective odds ratios for pregnancy, smoking and oral contraceptives (OCs) became stronger in pre-menopausal women.', 'RESULTS: Postmenopausal hormonal treatment, use of contraceptives, or fertility treatment did not influence the risk of meningioma.']
# snippets are not used in KMeansSimilarityOrderer
snippets = None
tiler_info = {'max_length': 200, 'max_tokens': 200, 'k': 2, 'max_iter': 20}
orderer = KMeansOrderer()
print(orderer.orderSentences(sentences, snippets, tiler_info))
"""
