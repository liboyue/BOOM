#!/usr/bin/env python
# coding=utf-8

from src.modules import SampleModule

import yaml
import json
import glog as log

with open('conf.yaml') as f:
    conf = yaml.load(f)

## The exchange the pipeline uses.
m3 = SampleModule(conf['modules'][2], conf['host'])
m3.run()
