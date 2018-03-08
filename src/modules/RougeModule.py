import glog as log
import json
from .module import Module
from rouge import Rouge

class RougeModule(Module):

    def __init__(self, conf, host):
        super().__init__(conf, host)

    def process(self, job):
        job.producer = self.name
        job.consumer = self.output_module
        job.save_uri = job.save_uri + self.name + '_' + json.dumps(job.params) + '_'

        log.info(job.data_uri)
        data = self.read_from(job.data_uri)

        evaluator = Rouge()
        all_scores = []
        f_scores = []
        for question in data:
            score = evaluator.get_scores(question[0], question[1])[0]['rouge-1']
            all_scores.append(score)
            f_scores.append(score['f'])

        result = {'individual': all_scores, 'average': sum(f_scores)/len(f_scores)}
        log.info(data)

        job.data_uri = job.save_uri + '.json'
        self.save_to(result, job.save_uri + '.json')
        return job

if __name__ == '__main__':
    pass
