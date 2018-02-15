import sys, json
from .module import Module

class SampleModule(Module):

    def __init__(self, conf):
        super().__init__(conf)

    def run(self, out_dir):
        return self.reorder()[:self.number]

if __name__ == '__main__':
    pass
