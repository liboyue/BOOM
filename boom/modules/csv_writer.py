import os
import csv

import glog as log

from .module import Module


class CSVWriter(Module):
    "The CSVWriter class saves results to a csv file."

    def __init__(self, module_id, name, exp_name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):
        super(CSVWriter, self).__init__(module_id, name, exp_name, rabbitmq_host,
                                        pipeline_conf, module_conf, **kwargs)

        self.content = []
        self.header = []

    def process(self, job, data):
        # Create header when first called.
        if self.header == []:
            self.header = [k for k in data]
            #log.info("The header is " + str(self.header))
        self.content.append([job.output_path] + [data[k] for k in self.header])
        return data

    ## Save csv file, overriding the default saving function.
    #  @param job The job to be saved.
    #  @param data The data to be saved.
    #  @return the path to data.
    def save_job_data(self, job, data):
        path = job.output_base + '/' + self.output_file
        log.info('Save csv to ' + path)

        if not os.path.exists(job.output_base):
            os.mkdir(job.output_base)

        with open(path, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['configuration'] + self.header)
            for row in self.content:
                writer.writerow(row)
        return path


if __name__ == '__main__':
    pass
