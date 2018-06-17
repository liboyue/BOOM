from .BiRanker import BiRanker
from .SimilarityJaccard import *


'''
@Author: Khyathi Raghavi Chandu
@Date: October 17 2017
This code contains the implementation of Abstract method for BiRanker.
'''

class CoreMMR(BiRanker):
    def __init__(self):
        super(CoreMMR, self).__init__()
        self.jaccard = SimilarityJaccard()

    #implementation of the abstract method that takes question as input and returns a ranked list of sentences as output
    def getRankedList(self, question, alpha, beta):
        self.alpha = alpha
        self.beta = beta
        selectedSentences = []
        snippets = question['snippets']
        #This is the class method from the BiRanker that is used to compute the positional scores of the sentences in the snippets.
        pos_dict = {}
        best = []
        current_best = None
        summaryFinal = ""
        length=0
        #class method from abstract class that tokenizes all the snippets to sentences.
        sentences = self.getSentences(question)
        for i in range(self.numSelectedSentences):
            best_sim = -99999999
            for sentence in sentences:
                #similarityJaccard is an extension of Similarity Measure that takes 2 sentences ansd returns the float (similarity)
                ques_sim = self.jaccard.calculateSimilarity(sentence, question['body'])
                max_sent_sim = -99999999
                for other in best:
                    similarity = self.jaccard.calculateSimilarity(sentence, other)
                    if self.beta!=0:
                        try:
                            current_sent_sim = (self.beta*similarity.calculateSimilarity())+((1-self.beta)*self.pos_dict[sentence])
                        except:
                            current_sent_sim = (self.beta*similarity.calculateSimilarity())+((1-self.beta)*self.pos_dict[sentence.lstrip().rstrip()])
                    else: # since the value of beta is set to 0
                        current_sent_sim = similarity
                    if current_sent_sim > max_sent_sim:
                        max_sent_sim = current_sent_sim
                #equation for mmr to balance between similarity with already selected sentences and similarity with question
                final_sim = ((1-self.alpha)*ques_sim)-(self.alpha*max_sent_sim)
                if final_sim > best_sim:
                    best_sim = final_sim
                    current_best = sentence
            best.append(current_best)
            #maintaining a list of sentences that are not already selected so they can be used for selection for next iteration
            sentences = set(sentences).difference(set(best))
            if current_best!=None:
                    selectedSentences.append(current_best)
            else:
                break
        return selectedSentences
