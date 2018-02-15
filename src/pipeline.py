import yaml
import json
import glog as log
import os
import time
from .modules import *

class Pipeline:
    "The pipeline class creates the pipeline, and manages execution."
    
    ##  @param conf_path The path to the configuration file.
    def __init__(self, conf_path):

        ## The path to the configuration file.
        self.conf_path = conf_path

        with open(conf_path) as f:
        # with open('conf.yaml') as f:
            # a = yaml.load(f)

            ## Content of the configuration file.
            self.conf = yaml.load(f)

        log.info('Loading configuration file from ' + conf_path)
        log.info(json.dumps(self.conf, indent=4))

        ## Name of the pipeline.
        self.name = self.conf['name']

        ## List of all Module objects.
        self.modules = [eval(mod_conf['type'])(mod_conf) for mod_conf in self.conf['modules']]
        log.info('Module list: \n' + '\n\n'.join([str(x) for x in self.modules]))

        ## Head node of the pipeline.
        self.pipeline = None
        self._create_pipeline()

    def __str__(self, module=None, indent=0):
        if module == None:
            return 'Pipeline name: ' + self.name + '\n' \
                    + '  Modules:\n' \
                    + self.__str__(self.pipeline, 1)
        else:
            ans = '    | ' * (indent) + module.get_name() + '\n'
            if module.get_n_outputs() > 0:
                for child in module.get_output_modules():
                    ans += self.__str__(child, indent+1)
            return ans

    ## The function recursively creates the pipeline.
    #  A pipeline is a graph, every node is a module. This function recursively creates the pipeline.
    #  @param moudle The head node to create a pipeline.
    def _create_pipeline(self, module=None):
        if module == None:
            self.pipeline = self.modules[0]
            self._create_pipeline(self.pipeline)

        elif hasattr(module, 'output_files'):
            log.info('Output module encountered')
            return module

        else:
            for tmp in self.modules:
                if not tmp in module.get_output_modules() and tmp.get_name() in module.get_conf()['output_modules']:
                    log.warn(tmp)
                    module.add_output_module(tmp)
                    tmp.add_input_module(module)
                    self._create_pipeline(tmp)

    def _check_pipeline(self, ind=0, parents=[]):
        if len(self.modules) == 0:
            return False

        self.modules[ind]
        children = self.modules[ind]

        if name not in modules:
            return False

        if "output_files" in modules[name]:
            return True

        for next_name in modules[name]['outputs']:
            if self._check_pipeline(next_name, modules) == False:
                return False

        return True

    def _check_types(self, name, modules):
        if "output_files" in modules[name]:
            return True

        for next_name in modules[name]['outputs']:
            if modules[name]['output_type'] != modules[next_name]['input_type']:
                return False

        for next_name in modules[name]['outputs']:
            if self._check_types(next_name, modules) == False:
                return False

        return True

    ## The function to run the pipeline
    def run(self):
        out_dir = time.strftime("%Y-%m-%d_%Hh%Mm%Ss", time.localtime())
        os.mkdir(out_dir)
        cursor = self.pipeline
        data = None
        while True:
            log.info(cursor)
            log.info(data)
            data = cursor.run(out_dir, data)
            cursor = cursor.get_output_modules()
            if cursor == []:
                break
            else:
                cursor = cursor[0]
        log.info(cursor)
        log.info(data)

