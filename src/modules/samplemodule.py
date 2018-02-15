import sys, json
import glog as log
from .module import Module

class SampleModule(Module):

    def __init__(self, conf):
        super().__init__(conf)

    def run(self, out_dir, data=None):
        if data == None:
            if hasattr(self, 'input_files'):
                log.info('Processing files from ' + str(self.input_files))
                data = json.load(open(self.input_files[0]))
        data['string_list'] = [x + ' processed by ' + self.name for x in data['string_list']]

        log.info(data)
        if hasattr(self, 'output_files'):
            self.save_to(data, out_dir + '/' + self.output_files[0])
        else:
            self.save_to(data, out_dir + '/' + self.name + '.json')

        return data

if __name__ == '__main__':
    pass
