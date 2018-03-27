from .SimilarityMeasure import SimilarityMeasure
from nltk.tokenize import word_tokenize


class SimilarityJaccard(SimilarityMeasure):
    def __init__(self):
        super().__init__('', '')

    def calculateSimilarity(self, s1, s2):
        s1 = word_tokenize(s1.lower())
        s2 = word_tokenize(s2.lower())
        #s1_u_s2 = set()
        #s1_i_s2 = set()
        set1 = {i for i in s1 if i not in self.stopWords}
        set2 = {i for i in s2 if i not in self.stopWords}
        self.score = len(set1.intersection(set2)) / len(set1.union(set2))
        return self.score

"""
instance = SimilarityJaccard("apple banana cat dog", "apple elephant cat dog")
print instance.calculateSimilarity()
"""
