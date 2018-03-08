import glog as log
import json
import sys
from .module import Module

class SampleModule(Module):

    def __init__(self, module_id, name, host, **kwargs):
        super().__init__(module_id, name, host, **kwargs)

    def process(self, job):
        job.producer = self.name
        job.consumer = self.output_module
        job.save_uri = job.save_uri + self.name + '_' + json.dumps(job.params) + '_'

        data = self.read_from(job.data_uri)

        data['string_list'] = [x + ' processed by ' + self.name + ', params ' + str(job.params) for x in data['string_list']]
        log.debug(data)

        job.data_uri = job.save_uri + '.json'
        self.save_to(data, job.save_uri + '.json')
        return job

if __name__ == '__main__':
    pass
