import glog as log
import json
from .module import Module
from .bioasq.coreMMR import CoreMMR as bioMMR

class CoreMMR(Module):

    def __init__(self, module_id, name, host, **kwargs):
        super().__init__(module_id, name, host, **kwargs)

    def process(self, job):
        job.producer = self.name
        job.consumer = self.output_module
        job.save_uri = job.save_uri + self.name + '_' + json.dumps(job.params) + '_'

        log.debug(job.data_uri)
        data = self.read_from(job.data_uri)

        ranker = bioMMR()
        question = data['questions'][0]
        question['snippets'] = question['contexts']['long_snippets']
        data = ranker.getRankedList(question)
        log.debug(data)

        job.data_uri = job.save_uri + '.json'
        self.save_to(data, job.save_uri + '.json')
        return job

if __name__ == '__main__':
    pass
