from .SimilarityMeasure import SimilarityMeasure
from nltk.tokenize import word_tokenize


class SimilarityJaccard(SimilarityMeasure):
    def __init__(self):
        super(SimilarityJaccard, self).__init__('', '')

    def calculateSimilarity(self, s1, s2):

        s1 = word_tokenize(s1.lower())
        s2 = word_tokenize(s2.lower())

        set1 = set([i for i in s1 if i not in self.stopWords])
        set2 = set([i for i in s2 if i not in self.stopWords])

        intersection = len(set1.intersection(set2))
        union = len(set1) + len(set2) - intersection

        return intersection / union

"""
instance = SimilarityJaccard("apple banana cat dog", "apple elephant cat dog")
print instance.calculateSimilarity()
"""
