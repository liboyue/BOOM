class Parameter(object):
    """This class handles parameters."""

    def __init__(self, conf):
        ## Name of the parameter.
        self.name = conf['name']
        ## Type of the parameter. It is one of 'float', 'int' or 'collection'.
        self.type = conf['type']
        if self.type == 'collection':
            self.values = conf['values']
        else:
            ## Starting value of the parameter.
            self.start = conf['start']
            ## Ending value of the parameter.
            self.end = conf['end']
            ## Step size for each update.
            self.step_size = conf['step_size']

    def __str__(self):
        s = 'name: ' + str(self.name) + ', type: ' + self.type
        if self.type == 'float' or self.type == 'int':
            s += ', start: ' + str(self.start) \
            + ', end: ' + str(self.end) \
            + ', step size: ' + str(self.step_size)
        else:
            s += ', values: ' + str(self.values) \

        return s


    ## The generator for all possible values.
    #  @return The generator for all possible values.
    def get_values(self):
        if self.type == 'float':
            import numpy as np
            for val in np.arange(
                    self.start,
                    self.end + self.step_size,
                    self.step_size):
                yield val.astype(float)

        elif self.type == 'int':
            for val in range(
                    self.start,
                    self.end + self.step_size,
                    self.step_size):
                yield val

        else:
            for val in self.values:
                yield val

    ## Calculate the number of possible choices.
    def get_n_choices(self):
        if self.type == 'collection':
            return len(self.values)
        else:
            return (self.end - self.start) / self.step_size + 1
