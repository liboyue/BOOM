import abc
from abc import abstractmethod

'''
This code contains the abstract class for SentenceOrderer.
'''

'''
This is an Abstract class that serves as a template for implementations for ordering sentences.
'''


class SentenceOrderer(object):
    __metaclass__ = abc.ABCMeta

    # abstract method that should be implemented by the subclass that extends this abstract class
    @abstractmethod
    def __init__(self):
        pass

    # abstract method that should be implemented by the subclass that extends this abstract class
    @abstractmethod
    def orderSentences(self, sentences, snippets, info_dict):
        pass

    # DEPRICATED method to tile sentences. Tiling should NOT be done withing ordering module 
    def tileSentences(self, sentences):
        answer = ''
        for sentence in sentences:
            answer += sentence[0].upper()
            answer += sentence[1:]
            if answer[-1] not in ['.', '!', '?']:
                answer += '.'
            answer += ' '
        return answer[:-1]
