#!/usr/bin/env python
# coding=utf-8

from src.modules.RougeModule import RougeModule

import yaml
import json
import glog as log

with open('BioASQ_conf.yaml') as f:
    conf = yaml.load(f)

## The exchange the pipeline uses.
m4 = RougeModule(conf['modules'][3], conf['host'])
m4.run()
