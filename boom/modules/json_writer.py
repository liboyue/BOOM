import json
import os

import glog as log

from .module import Module


class JSONWriter(Module):
    """The JSONWriter class saves results to a csv file."""

    def __init__(self, module_id, name, exp_name, rabbitmq_host, pipeline_conf,
                 module_conf, **kwargs):
        super(JSONWriter, self).__init__(module_id, name, exp_name,
                                        rabbitmq_host, pipeline_conf,
                                        module_conf, **kwargs)

        self.content = []
        self.header = []

    def process(self, job, data):
        # Create header when first called.
        if not self.header:
            self.header = [k for k in data]
        record = {
            'output_path': job.output_path,
            'config': job.config
        }
        for each_header in self.header:
            record[each_header] = data[each_header]
        self.content.append(record)
        return data

    ## Save json file, overriding the default saving function.
    #  @param job The job to be saved.
    #  @param data The data to be saved.
    #  @return the path to data.
    def save_job_data(self, job, data):
        path = job.output_base + '/' + self.output_file
        log.info('Save json to ' + path)

        if not os.path.exists(job.output_base):
            os.mkdir(job.output_base)

        with open(path, 'w') as jsonfile:
            for row in self.content:
                jsonfile.write(json.dumps(row) + '\n')
        return path


if __name__ == '__main__':
    pass
