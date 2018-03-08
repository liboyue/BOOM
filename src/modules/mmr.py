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
        result = []
        for i, question in enumerate(data['questions']):
            question['snippets'] = question['contexts']['long_snippets']
            answer = question['ideal_answers'][0]
            result.append((ranker.getRankedList(question, job.params['alpha']/100, 0), answer))
        log.debug(data)

        job.data_uri = job.save_uri + '.json'
        self.save_to(result, job.save_uri + '.json')
        return job

if __name__ == '__main__':
    pass
