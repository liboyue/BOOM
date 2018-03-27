import glog as log
from .module import Module
from .bioasq.coreMMR import CoreMMR as bioMMR

class CoreMMR(Module):

    def __init__(self, module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):
        super().__init__(module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs)
        self.ranker = bioMMR()

    def process(self, job, data):

        result = []
        for i, question in enumerate(data['questions']):
            #log.info(i/len(data['questions']))
            #question['snippets'] = question['contexts']['long_snippets']
            #answer = question['ideal_answers'][0]
            #log.warn(str(i) + ", " + str(question))
            if 'snippets' in question:
                question['snippets'] = [s['text'] for s in question['snippets']]
                result.append(self.ranker.getRankedList(question, job.params['alpha']/100, 0))

        log.debug(result)

        return result

if __name__ == '__main__':
    pass
