import abc
import json

class Module():
    """The base module class. Every actual module should be derived from this class."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, conf):
        self._conf = conf
        self._name = conf['name']
        self._params = conf['params']

        if 'output_files' in conf:
            self._output_files = conf['output_files']

        if 'input_files' in conf:
            self._input_files = conf['input_files']

        self._output_modules = []
        self._input_modules = []

    def __str__(self):
        return 'Module name: ' + self._name + '\n' \
                + 'Module params: ' + json.dumps(self._params) + '\n' \
                + 'Output modules: ' + '    \n'.join([str(child) for child in self._output_modules])

    def get_output_modules(self):
        return self._output_modules

    def add_output_module(self, module):
        for tmp in self._output_modules:
            if tmp.get_name() == module.get_name():
                return
        self._output_modules.append(module)

    def add_input_module(self, module):
        for tmp in self._input_modules:
            if tmp.get_name() == module.get_name():
                return
        self._input_modules.append(module)

    def get_conf(self):
        return self._conf

    def get_name(self):
        return self._name

    def get_n_inputs(self):
        return len(self._input_modules)

    def get_n_outputs(self):
        return len(self._output_modules)

    def get_input_types(self):
        return self._input_types

    def get_output_types(self):
        return self._output_types

    def get_n_params(self):
        return len(self._params)

    def get_param(self, idx):
        return self._params[idx]

    def set_param(self, idx, value):
        try:
            self._params[idx] = value
            return True
        except:
            return False

    def get_id(self):
        return self._id

    def get_module_name(self):
        return self._name

    @abc.abstractmethod
    def run(self):
        """This function needs to be implemented in each class and should run the
        core algorithm for the module and return the module's output."""
        return

if __name__ == '__main__':
    pass
