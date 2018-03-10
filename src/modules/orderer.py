import json
import glog as log
from .module import Module
from .bioasq.KMeansOrderer import KMeansOrderer

class Orderer(Module):

    def __init__(self, module_id, name, host, **kwargs):
        super().__init__(module_id, name, host, **kwargs)
        self.orderer = KMeansOrderer()

    def process(self, job):

        log.debug(job.data_uri)
        data = self.read_from(job.data_uri)

        result = []
        for question in data:
            try:
                ordered = self.orderer.orderSentences(question[0], job.params['k'])
                result.append((ordered, question[1]))
            except:
                pass
        log.debug(data)

        job.data_uri = job.save_uri + '.json'
        self.save_to(result, job.data_uri)
        return job

if __name__ == '__main__':
    pass
