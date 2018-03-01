import re, math
from collections import Counter

from SimilarityMeasure import *


class SimilarityCosine(SimilarityMeasure):

    def text_to_vector(self, text):
        words = self.WORD.findall(text)
        return Counter(words)

    def calculateSimilarity(self):
        self.WORD = re.compile(r'\w+')
        vec1 = self.text_to_vector(self.sentence1)
        vec2 = self.text_to_vector(self.sentence2)

        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])

        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator
