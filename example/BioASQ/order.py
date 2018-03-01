#!/usr/bin/env python
# coding=utf-8

from src.modules.OrdererModule import OrdererModule

import yaml
import json
import glog as log

with open('BioASQ_conf.yaml') as f:
    conf = yaml.load(f)

## The exchange the pipeline uses.
m2 = OrdererModule(conf['modules'][1], conf['host'])
m2.run()
