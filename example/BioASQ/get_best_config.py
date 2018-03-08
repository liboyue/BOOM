import os, sys
import json

dir_path = sys.argv[1]

best_score = -1
best_config = None
for filename in os.listdir(dir_path):
    if 'rouge' in filename:
        data = json.load(open(dir_path + '/' + filename, 'r'))
        score = data['average']
        if score > best_score:
            best_score = score
            best_config = filename

print(best_config)
