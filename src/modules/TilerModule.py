import sys, json
import glog as log
from .module import Module
from src.bioasq_modules.Concatenation import Concatenation

class TilerModule(Module):

    def __init__(self, conf, host):
        super().__init__(conf, host)

    def process(self, job):
        job.producer = self.name
        job.consumer = self.output_module
        job.save_uri = job.save_uri + self.name + '_' + json.dumps(job.params) + '_'

        log.info(job.data_uri)
        data = self.read_from(job.data_uri)

        concatenator = Concatenation()
        result = []
        for question in data:
            result.append((concatenator.tileSentences(question[0], job.params['word_limit']), question[1]))
        log.info(data)

        job.data_uri = job.save_uri + '.json'
        self.save_to(result, job.save_uri + '.json')
        return job

if __name__ == '__main__':
    pass
