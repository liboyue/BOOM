class Parameter:
    """This class."""

    def __init__(self, conf):
        ## Name of the parameter.
        self.name = conf['name']
        ## Starting value of the parameter.
        self.start = conf['start']
        ## Ending value of the parameter.
        self.end = conf['end']
        ## Step size for each update.
        self.step_size = conf['step size']
        ## Value of the parameter.
        self.val = self.start

    def __str__(self):
        return 'name: ' + str(self.name) \
                + ', start: ' + str(self.start) \
                + ', end: ' + str(self.end) \
                + ', step size:' + str(self.step_size)

    ## Return current value.
    def get_value(self):
        return self.val

    ## Return current value.
    #  @param val New value for the parameter.
    def set_value(self, val):
        self.val = val

    ## Update the parameter to the next value.
    #  @return True if successfully updated, False if the next value is invalid.
    def next_value(self):
        if self.val + self.step_size <= self.end:
            self.val += self.step_size
            return True
        else:
            return False


    ## Reset the parameter to the starting value.
    def reset_value(self):
        self.val = self.start
