#!/usr/bin/env python
# coding=utf-8
import glog as log
from src.modules import Module
from bioasq.KMeansOrderer import KMeansOrderer

class Orderer(Module):

    def __init__(self, module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):
        super().__init__(module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs)
        self.orderer = KMeansOrderer()

    def process(self, job, data):

        #log.debug(job.input_uri)
        result = []
        for question, ideal_answer in data:
            try:
                ordered = self.orderer.orderSentences(question, job.params['k'])
                result.append((ordered, ideal_answer))
            except:
                pass
        #log.debug(result)

        return result


from rouge import Rouge as RougeLib

class Rouge(Module):

    def __init__(self, module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):
        super().__init__(module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs)
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
        result = {'average': sum(f_scores)/len(f_scores)}
        log.info(result)

        return result


from multiprocessing import Pool
from bioasq.coreMMR import CoreMMR as BioASQCoreMMR

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

    def __init__(self, module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):
        super().__init__(module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs)
        self.processes = module_conf['processes'] if 'processes' in module_conf else 1
        self.pool = Pool(processes=self.processes)

    ## Override the cleanup function to make sure close the process pool.
    def cleanup(self):
        self.pool.close()
        self.pool.join()

    def process(self, job, data):

        questions = data['questions']
        N = len(questions)
        step_size = int(N / self.processes)
        slices = [(questions[i:i+step_size], job.params['alpha']) for i in range(0, N, step_size)]
        tmp = self.pool.map(multi_process_helper, slices)

        result = []
        for x in tmp:
            result += x

        return result

from bioasq.Concatenation import Concatenation

class Tiler(Module):

    def __init__(self, module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):
        super().__init__(module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs)
        self.concatenator = Concatenation()

    def process(self, job, data):

        #log.debug(job.input_uri)

        result = {}
        for i, (question, ideal_answer) in enumerate(data):
            key = "result_" + str(i)
            result[key] = (self.concatenator.tileSentences(question, job.params['word_limit']), ideal_answer)
        #log.debug(result)

        return result
