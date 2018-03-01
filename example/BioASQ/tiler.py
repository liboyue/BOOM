#!/usr/bin/env python
# coding=utf-8

from src.modules.TilerModule import TilerModule

import yaml
import json
import glog as log

with open('BioASQ_conf.yaml') as f:
    conf = yaml.load(f)

## The exchange the pipeline uses.
m3 = TilerModule(conf['modules'][2], conf['host'])
m3.run()
