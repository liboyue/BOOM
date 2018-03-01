import glog as log
import json
from .module import Module
from src.bioasq_modules.coreMMR import CoreMMR

class MMRModule(Module):

    def __init__(self, conf, host):
        super().__init__(conf, host)

    def process(self, job):
        job.producer = self.name
        job.consumer = self.output_module
        job.save_uri = job.save_uri + self.name + '_' + json.dumps(job.params) + '_'

        log.info(job.data_uri)
        data = self.read_from(job.data_uri)

        ranker = CoreMMR()
        question = data['questions'][0]
        question['snippets'] = question['contexts']['long_snippets']
        data = ranker.getRankedList(question)
        log.info(data)

        job.data_uri = job.save_uri + '.json'
        self.save_to(data, job.save_uri + '.json')
        return job

if __name__ == '__main__':
    pass
