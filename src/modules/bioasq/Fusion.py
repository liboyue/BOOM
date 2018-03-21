from Tiler import Tiler
from SimilarityCosine import *
from SimilarityJaccard import *



import logging
from logging import config

from collections import Counter
import takahe
import multiprocessing
import document
from pulp import GLPK
import pulp
import nltk
import string
import re
from nltk.tokenize import sent_tokenize, word_tokenize


logging.config.fileConfig('logging.ini')
logger = logging.getLogger('bioAsqLogger')

def _dofuse(sentenceL):
    """
    Extracts the call to takahe to interrupt it if it's taking too long.
    """
    fuser = takahe.word_graph(sentenceL,
                              nb_words=6,
                              lang="en",
                              punct_tag="PUNCT")
    # get fusions
    fusions = fuser.get_compression(50)
    # rerank and keep top 10
    reranker = takahe.keyphrase_reranker(sentenceL, fusions, lang="en")
    rerankedfusions = reranker.rerank_nbest_compressions()[0:5]
    return rerankedfusions


def _fuseSentence(sentenceL):

    """
    Creates alternatives to sentences by fusing them.
    """
    # fuse only if we have 2 or more sentences
    if len(set(sentenceL)) < 2:
        return sentenceL

    # small hack. takahe module may not finish.
    # We give it 15 seconds to compute the result
    if True:
        process = multiprocessing.Pool(processes=1)
        res = process.apply_async(_dofuse, (sentenceL,))
        rerankedfusions = _dofuse(sentenceL)
        rerankedfusions = res.get(timeout=15)
        process.terminate()
    else:
        # may fail if there is no verb in the cluster or illformed sentences
        rerankedfusions = []
    # recompose sentences
    finalfusions = []
    for _, fusedsentence in rerankedfusions:
        finalfusions.append(" ".join([word + '/' + pos
                                      for word, pos in fusedsentence]))
    # using sets to remove duplicates
    return list(set(finalfusions).union(set(sentenceL)))

def extractBigrams(sentence):
    """
    Extracts the bigrams from a tokenized sentence.
    Applies some filters to remove bad bigrams
    """
    bigrams = [(document.stem(tok1.lower()),  document.stem(tok2.lower()))
               for tok1, tok2 in zip(sentence, sentence[1:])]
    # filter bigrams
    bigrams = [(tok1, tok2) for tok1, tok2 in bigrams
               if not (tok1 in nltk.corpus.stopwords.words('english') and
                       tok2 in nltk.corpus.stopwords.words('english')) and
               tok1 not in string.punctuation and
               tok2 not in string.punctuation]
    return bigrams


def removePOS(sentence):
    """
    Removes the part of speech from a string sentence.
    """
    cleansentence = []
    for word in sentence.split():
        cleansentence.append(word.split('/')[0])
    return ' '.join(cleansentence)




def wellformatize(s):
    ws = re.sub(" ('[a-z]) ", "\g<1> ", s)
    ws = re.sub(" ([\.;,-]) ", "\g<1> ", ws)
    ws = re.sub(" ([\.;,-?!])$", "\g<1>", ws)
    ws = re.sub(" ' ", "' ", ws)
    ws = re.sub(" _ (.+) _ ", " -\g<1>- ", ws)
    ws = re.sub("`` ", "\"", ws)
    ws = re.sub(" ''", "\"", ws)
    ws = re.sub("\s+", " ", ws)
    # repair do n't to don't
    ws = re.sub("(\w+) n't", "\g<1>n't", ws)
    return ws.strip()

'''
This is a subclass that extends the abstract class Tiler.
'''
class Fusion(Tiler):


    def readInDocument(self,doc):
        self.document = doc
        self.updateBigrams(doc)


    #Update the bigram statistics for the summarizer
    def updateBigrams(self, doc):

        if self.bigramstats is None:
            self.bigramstats = Counter()
        seen = set()
        for sentence in doc.tokens:
            for bigram in extractBigrams(sentence):
                if bigram not in seen:
                    seen.add(bigram)
                    self.bigramstats[bigram] = 1
                else:
                    self.bigramstats[bigram] += 1


    # Create sentences with POS tags
    def createSentences(self):
        fullsentences = [sentence for sentence in self.document.taggedTokens]
        self.sentenceL = [" ".join(['/'.join(token) for token in sentence]) for sentence in fullsentences]

    def _selectSentences(self, wordlimit):

        fullsentences = list(set([removePOS(sentence)
                         for sentence in self.candidates]))

        # extract bigrams for all sentences
        bigramssentences = [extractBigrams(sentence.split())
                            for sentence in fullsentences]

        # get uniqs bigrams
        uniqbigrams = set(bigram
                          for sentence in bigramssentences
                          for bigram in sentence)
        numbigrams = len(uniqbigrams)


        # rewrite fullsentences

        fullsentences = [wellformatize(sentence) for sentence in fullsentences]

        numsentences = len(fullsentences)


        # filter out rare bigrams
        weightedbigrams = {bigram: sum([0.8**i for i in xrange(count)])
                           for bigram, count in self.bigramstats.items()}


        problem = pulp.LpProblem("Sentence selection", pulp.LpMaximize)

        # concept variables
        concepts = pulp.LpVariable.dicts(name='c',
                                         indexs=range(numbigrams),
                                         lowBound=0,
                                         upBound=1,
                                         cat='Integer')

        sentences = pulp.LpVariable.dicts(name='s',
                                          indexs=range(numsentences),
                                          lowBound=0,
                                          upBound=1,
                                          cat='Integer')

        # objective : maximize wi * ci (weighti * concepti)
        # small hack. If the bigram has been filtered out from uniqbigrams,
        # we give it a weight of 0.
        problem += sum([(weightedbigrams.get(bigram) or 0) * concepts[i]
                        for i, bigram in enumerate(uniqbigrams)])

        # constraints

        # size
        problem += sum([sentences[j] * len(fullsentences[j].split())
                       for j in xrange(numsentences)]) <= wordlimit

        # integrity constraints (link between concepts and sentences)
        for j, bsentence in enumerate(bigramssentences):
            for i, bigram in enumerate(uniqbigrams):
                if bigram in bsentence:
                    problem += sentences[j] <= concepts[i]

        for i, bigram in enumerate(uniqbigrams):
            problem += sum([sentences[j]
                            for j, bsentence in enumerate(bigramssentences)
                            if bigram in bsentence]) >= concepts[i]

        # solve the problem
        problem.solve(GLPK())

        summary = []
        # get the sentences back
        for j in range(numsentences):
            if sentences[j].varValue == 1:
                summary.append(fullsentences[j])

        return summary


    #Abstract method from Tiler class that takes a list of sentences as arguments and returns the final summary in a single string.
    def tileSentences(self, sentences, pred_length):

        self.minbigramcount = 2
        self.bigramstats = None
        self.document = None

        sentences = list(set(map(lambda s : s[0].lower() + s[1:], sentences)))

        old_summary = " ".join(sentences)
        temp_file = open("temp.txt","w")

        temp_file.write(old_summary)
        temp_file.close()

        self.readInDocument(document.Document("temp.txt"))
        self.createSentences()
        #print "------------- Sentence List --------- "
        #print self.sentenceL
        #print "------------- Sentence List --------- "

        self.candidates = []
        canDisgard = []

        for s1 in self.sentenceL:
            for s2 in self.sentenceL:
                sim = SimilarityJaccard(s1, s2).calculateSimilarity()
                if sim > 0.6 and sim < 1.0:
                    if s1 not in canDisgard and s2 not in canDisgard:
                        if len(s1.split()) > len(s2.split()):
                            canDisgard.append(s1)
                        else:
                            canDisgard.append(s2)

        self.sentenceL = list(set(self.sentenceL) - set(canDisgard))
        for s1 in self.sentenceL:
            for s2 in self.sentenceL:
                sim = SimilarityJaccard(s1, s2).calculateSimilarity()
                if sim < 0.1:
                    continue
                else:
                    self.candidates += _fuseSentence([s1,s2])
                #print "========= FUSINGGGGG ===== "
        self.candidates = list(set(self.candidates))
        #print "len candidate", len(self.candidates)

        new_sentences = self._selectSentences(pred_length)

        new_sentences = map(lambda s : s[0].upper() + s[1:], new_sentences)

        canDisgard2 = []
        for s1 in new_sentences:
            for s2 in new_sentences:
                sim = SimilarityJaccard(s1, s2).calculateSimilarity()
                #print "----"
                #print 's1', s1
                #print 's2', s2
                #print 'sim', sim
                #print "----"
                if sim > 0.7 and sim < 1.0:
                    if s1 not in canDisgard2 and s2 not in canDisgard2:
                        if len(s1.split()) > len(s2.split()):
                            canDisgard2.append(s2)
                        else:
                            canDisgard2.append(s1)
        new_sentences = list(set(new_sentences) - set(canDisgard2))

        # summary = ' '.join(new_sentences)

        if not new_sentences:
            length = 0
            summary = ""
            for sentence in sentences:
            #BioAsq ideal generation guideline imposes an upper word limit of 200. The following command maintains that restriction.
                if (len(word_tokenize(sentence)) + length) <= pred_length:
                    new_sentences += sentence
                    length += len(word_tokenize(sentence))

        return new_sentences
