import glog as log
from boom.modules import Module
from boom.log import set_logger

class Sample(Module):

    def __init__(self, module_id, name, exp_name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):
        super(Sample, self).__init__(module_id, name, exp_name, rabbitmq_host, pipeline_conf, module_conf, **kwargs)

        # Initialize logger.
        set_logger(rabbitmq_host, exp_name)

    def process(self, job, data):

        log.debug(job)
        result = [x + ' processed by ' + self.name + ', params ' + str(job.params) for x in data['string_list']]
        data['string_list'] = result
        log.debug(data)

        return data
