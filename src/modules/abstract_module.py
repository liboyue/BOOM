import abc
import uuid

class Abstract_module():
    """The base module class. Every actual module should be derived from this class."""
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self._id = uuid.uuid4()
        self._name = name

    def get_n_inputs(self):
        return self._n_inputs

    def get_n_outputs(self):
        return self._n_outputs

    def get_input_types(self):
        return self._input_types

    def get_output_types(self):
        return self._output_types

    def get_n_params(self):
        return self._n_params

    def get_param_types(self):
        return self._param_types

    def get_param_interval(self):
        return self._param_interval

    def get_param_step(self):
        return self._param_step

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

    def set_input_types(self, name):
        try:
            self._name = name
            return True
        except:
            return False

    @abc.abstractmethod
    def run(self):
        """This function needs to be implemented in each class and should run the
        core algorithm for the module and return the module's output."""
        return

if __name__ == '__main__':
    pass
