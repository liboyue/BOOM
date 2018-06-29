#!/usr/bin/env python
# coding=utf-8

import json

with open('BioASQ-trainingDataset6b.json') as f:
    data = json.load(f)

with open('train_1000.json', 'w') as f:
    data['questions'] = data['questions'][:1000]
    json.dump(data, f)

with open('train_500.json', 'w') as f:
    data['questions'] = data['questions'][:500]
    json.dump(data, f)

with open('train_200.json', 'w') as f:
    data['questions'] = data['questions'][:200]
    json.dump(data, f)

with open('train_100.json', 'w') as f:
    data['questions'] = data['questions'][:100]
    json.dump(data, f)

with open('train_50.json', 'w') as f:
    data['questions'] = data['questions'][:50]
    json.dump(data, f)
