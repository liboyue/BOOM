import uuid

class abstract_module():
    "The base module class. Every actual module should be derived from this class."

    def __init__(self, name):
        self._id = uuid.uuid4()
        self._name = name

    def get_n_inputs(self):
        return self._n_inputs

    def get_n_outputs(self):
        return self._n_outputs

    def get_module_name(self):
        return self._name

    def get_id(self):
        return self._id


if __name__ == '__main__':
    pass
