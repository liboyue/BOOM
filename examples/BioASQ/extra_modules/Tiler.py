import glog as log
from boom.modules import Module
from .bioasq.Concatenation import Concatenation

class Tiler(Module):

    def __init__(self, module_id, name, exp_name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):
        super(Tiler, self).__init__(module_id, name, exp_name, rabbitmq_host, pipeline_conf, module_conf, **kwargs)
        self.concatenator = Concatenation()

    def process(self, job, data):

        #log.debug(job.input_uri)

        result = {}
        for i, (question, ideal_answer) in enumerate(data):
            key = "result_" + str(i)
            result[key] = (self.concatenator.tileSentences(question, job.params['word_limit']), ideal_answer)
        #log.debug(result)

        return result
