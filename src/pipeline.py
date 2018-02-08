import json

class pipeline:
    "The pipeline class creates the pipeline, and manages execution."
    
    def __init__(self, conf_path):
        self._conf_path = conf_path
        self._create_pipeline()

    def __str__(self):
        return ''

    def _create_pipeline(self):
        conf = json.loads(open(self._conf_path).read())
        self._name = conf['name']
        self._n_modules = len(conf['modules'])
        self._modules = conf['modules']
        print(self._modules)

    def _check_type(self, modules):
        pass

    def run(self):
        pass

    def plot(self, path):
        pass
