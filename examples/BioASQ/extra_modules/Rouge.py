import glog as log
from boom.modules import Module
from rouge import Rouge as RougeLib

class Rouge(Module):

    def __init__(self, module_id, name, exp_name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):
        super(Rouge, self).__init__(module_id, name, exp_name, rabbitmq_host, pipeline_conf, module_conf, **kwargs)
        self.evaluator = RougeLib()

    def process(self, job, data):
        #log.debug(data)

        all_scores = []
        f_scores = []

        for result in data:
            score = self.evaluator.get_scores(data[result][0], data[result][1])[0]['rouge-1']
            all_scores.append(score)
            f_scores.append(score['f'])

        #result = {'individual': all_scores, 'average': sum(f_scores)/len(f_scores)}
        result = {'average': sum(f_scores)/len(f_scores) if len(f_scores) > 0 else 0} 
        log.info(result)

        return result
