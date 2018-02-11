import sys, json
from . import Module

class Toy_Selector(Module):

    def __init__(self, name, string_list, number):
        Abstract_module.__init__(self, name)
        self.string_list = string_list
        self.number = number

    def reorder(self):
        return sorted(self.string_list, key=lambda x: -1*x[1])

    def run(self):
        return self.reorder()[:self.number]

if __name__ == '__main__':
    data = json.load(open(sys.argv[1]))
    m = Toy_Selector("Toy Selector", data["output"], int(sys.argv[2]))
    result = {"output" : m.run()}
    outfile = open("toy_selector_out.json", "w")
    json.dump(result, outfile)
    outfile.close()
