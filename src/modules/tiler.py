import sys, json
import glog as log
from .module import Module
from .bioasq.Concatenation import Concatenation

class Tiler(Module):

    def __init__(self, module_id, name, host, **kwargs):
        super().__init__(module_id, name, host, **kwargs)

    def process(self, job):

        log.debug(job.data_uri)
        data = self.read_from(job.data_uri)

        concatenator = Concatenation()
        result = []
        for question in data:
            result.append((concatenator.tileSentences(question[0], job.params['word_limit']), question[1]))
        log.debug(data)

        job.data_uri = job.save_uri + '.json'
        self.save_to(result, job.data_uri)

        return job

if __name__ == '__main__':
    pass
