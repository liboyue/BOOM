#!/usr/bin/env python
# coding=utf-8
import src
import glog as log

p = src.Pipeline('BioASQ_conf.yaml')
log.warn('Pipeline:\n' + str(p))
p.run()
