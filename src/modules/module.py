import abc
import json
from ..parameter import Parameter

class Module():
    """The base module class. Every actual module should be derived from this class."""

    ## Metaclass
    __metaclass__ = abc.ABCMeta

    def __init__(self, conf):
        """Initialization."""

        ## Original configuration file.
        self.conf = conf

        ## The module's name.
        self.name = conf['name']

        ## The module's parameters.
        self.params = self._init_params(conf['params'])

        if 'output_files' in conf:
            self.output_files = conf['output_files']

        if 'input_files' in conf:
            self.input_files = conf['input_files']

        self.output_modules = []
        self.input_modules = []

        ## The status of this module. If finished running, this value would be set to True
        self.finished = False

    def __str__(self):
        return 'Module name: ' + self.name + '\n' \
                + 'Module params: ' + '\n'.join([str(x) for x in self.params]) + '\n' \
                + 'Output modules: ' + '    \n'.join([str(child) for child in self.output_modules])

    def _init_params(self, params):
        """This function converts a dict of configurations to a dict of Param objects"""
        return [Parameter(param) for param in params]

    def get_output_modules(self):
        return self.output_modules

    def add_output_module(self, module):
        for tmp in self.output_modules:
            if tmp.get_name() == module.get_name():
                return
        self.output_modules.append(module)

    def add_input_module(self, module):
        for tmp in self.input_modules:
            if tmp.get_name() == module.get_name():
                return
        self.input_modules.append(module)

    def get_conf(self):
        return self.conf

    def get_name(self):
        return self.name

    def get_n_inputs(self):
        return len(self.input_modules)

    def get_n_outputs(self):
        return len(self.output_modules)

    def get_input_types(self):
        return self.input_types

    def get_output_types(self):
        return self.output_types

    def get_n_params(self):
        return len(self.params)

    def get_param(self, idx):
        return self.params[idx]

    def set_param(self, idx, value):
        try:
            self.params[idx] = value
            return True
        except:
            return False

    def get_id(self):
        return self.id

    def get_module_name(self):
        return self.name

    def read_from(self, path):
        pass

    def save_to(self, data, path):
        with open(path, 'w') as f:
            json.dump(data, f)


    ## The function to run the algorithm and process data.
    #  This function needs to be implemented in each class and should run the
    #  core algorithm for the module and return the path of module's output file.
    #  @param out_dir Directory to store intermediate files.
    #  @param data Dataset object to be processed (optional). If not provided, the module will load file from 'input_files'.
    #  @return The processed Dataset object.
    @abc.abstractmethod
    def run(self, out_dir, data=None):
        pass

if __name__ == '__main__':
    pass
