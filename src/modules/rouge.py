import json
import glog as log
from .module import Module
from rouge import Rouge as RougeLib

class Rouge(Module):

    def __init__(self, module_id, name, host, **kwargs):
        super().__init__(module_id, name, host, **kwargs)

    def process(self, job):

        log.debug(job.data_uri)
        data = self.read_from(job.data_uri)

        evaluator = RougeLib()
        all_scores = []
        f_scores = []
        for question in data:
            score = evaluator.get_scores(question[0], question[1])[0]['rouge-1']
            all_scores.append(score)
            f_scores.append(score['f'])

        result = {'individual': all_scores, 'average': sum(f_scores)/len(f_scores)}
        log.debug(data)

        job.data_uri = job.save_uri + '.json'
        self.save_to(result, job.data_uri)
        return job

if __name__ == '__main__':
    pass
