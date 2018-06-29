import glog as log
from boom.modules import Module
from multiprocessing import Pool
from .bioasq.coreMMR import CoreMMR as BioASQCoreMMR

def multi_process_helper(args):
    questions, alpha = args
    ranker = BioASQCoreMMR()
    result = []
    for question in questions:
        if 'snippets' in question:
            question['snippets'] = [s['text'] for s in question['snippets']]
            result.append((ranker.getRankedList(question, alpha, 0), question['ideal_answer'][0]))
    #log.debug(result)
    return result

class CoreMMR(Module):

    def __init__(self, module_id, name, exp_name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):
        super(CoreMMR, self).__init__(module_id, name, exp_name, rabbitmq_host, pipeline_conf, module_conf, **kwargs)
        self.processes = module_conf['processes'] if 'processes' in module_conf else 1
        self.pool = Pool(processes=self.processes)

    ## Override the cleanup function to make sure close the process pool.
    def cleanup(self):
        self.pool.close()
        self.pool.join()

    def process(self, job, data):

        questions = data['questions']
        N = len(questions)
        step_size = int(N / float(self.processes))
        slices = [(questions[i:i+step_size], job.params['alpha']) for i in range(0, N, step_size)]
        tmp = self.pool.map(multi_process_helper, slices)

        result = []
        for x in tmp:
            result += x

        return result
