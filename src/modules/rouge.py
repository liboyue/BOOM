import glog as log
from .module import Module
from rouge import Rouge as RougeLib

class Rouge(Module):

    def __init__(self, module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):
        super().__init__(module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs)
        self.evaluator = RougeLib()

    def process(self, job, data):
        log.info(data)

        all_scores = []
        f_scores = []

        for question in data:
            score = self.evaluator.get_scores(question[0], question[1])[0]['rouge-1']
            all_scores.append(score)
            f_scores.append(score['f'])

        #result = {'individual': all_scores, 'average': sum(f_scores)/len(f_scores)}
        result = {'average': sum(f_scores)/len(f_scores)}
        log.info(result)

        return result

if __name__ == '__main__':
    pass
