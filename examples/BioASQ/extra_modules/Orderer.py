#!/usr/bin/env python
# coding=utf-8
import glog as log
from boom.modules import Module
from .bioasq.KMeansOrderer import KMeansOrderer

class Orderer(Module):

    def __init__(self, module_id, name, exp_name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):
        super(Orderer, self).__init__(module_id, name, exp_name, rabbitmq_host, pipeline_conf, module_conf, **kwargs)
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
