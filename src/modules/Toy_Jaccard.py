import sys, json
from abstract_module import Abstract_module

class Toy_Jaccard(Abstract_module):

    def __init__(self, name, primary_string, string_list):
        Abstract_module.__init__(self, name)
        self.primary = primary_string
        self.string_list = string_list

    def jac_similarity(self, string1, string2):
        set1 = set(string1)
        set2 = set(string2)
        return len(set1.intersection(set2))/len(set1.union(set2))

    def run(self):
        return [(x, self.jac_similarity(self.primary, x)) for x in self.string_list]

if __name__ == '__main__':
    data = json.load(open(sys.argv[1]))
    m = Toy_Jaccard("Toy Jaccard", data["base_string"], data["string_list"])
    result = {"output" : m.run()}
    outfile = open("toy_jaccard_out.json", "w")
    json.dump(result, outfile)
    outfile.close()
