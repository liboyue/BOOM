#!/usr/bin/env python
# coding=utf-8
import src
import glog as log


configure_path = './conf.yaml'

p = src.Pipeline(configure_path)
log.warn('Pipeline sturcture:\n' + str(p))
p.run()


# plot_path = './plot.png'
# p.plot(plot_path)
