import sys, json
import glog as log
from .module import Module
from src.bioasq_modules.KMeansOrderer import KMeansOrderer

class OrdererModule(Module):

    def __init__(self, conf, host):
        super().__init__(conf, host)

    def process(self, job):
        job.producer = self.name
        job.consumer = self.output_module
        job.save_uri = job.save_uri + self.name + '_' + json.dumps(job.params) + '_'

        log.info(job.data_uri)
        data = self.read_from(job.data_uri)

        orderer = KMeansOrderer()
        result = []
        for question in data:
            try:
                ordered = orderer.orderSentences(question[0], job.params['k'])
                result.append((ordered, question[1]))
            except:
                pass
        log.info(data)

        job.data_uri = job.save_uri + '.json'
        self.save_to(result, job.save_uri + '.json')
        return job

if __name__ == '__main__':
    pass
