import glog as log
import json
import sys
from .module import Module

class Sample(Module):

    def __init__(self, module_id, name, message_host, **kwargs):
        super().__init__(module_id, name, message_host, **kwargs)

    def process(self, job):

        data = self.read_from(job.data_uri)
        data['string_list'] = [x + ' processed by ' + self.name + ', params ' + str(job.params) for x in data['string_list']]
        log.debug(data)

        job.data_uri = job.save_uri + '.json'
        self.save_to(data, job.data_uri)

        return job

if __name__ == '__main__':
    pass
