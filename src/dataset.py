import json
import glog as log

# a = json.load(open('bioasq_train_formatted.json'))
class Dataset:
    
    def __init__(self, path):

        self.path = path
        log.info('Loading dataset from ' + path)

        with open(path) as f:
            data = json.load(f)
            self.origin = data['origin']
            self.meta_data = data['meta_data']

    def __str__(self):
        return ''
