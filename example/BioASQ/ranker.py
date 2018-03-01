#!/usr/bin/env python
# coding=utf-8

from src.modules.MMRModule import MMRModule

import yaml
import json
import glog as log

with open('BioASQ_conf.yaml') as f:
    conf = yaml.load(f)

## The exchange the pipeline uses.
ranker = MMRModule(conf['modules'][0], conf['host'])
ranker.run()
