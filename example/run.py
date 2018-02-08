#!/usr/bin/env python
# coding=utf-8
import src


configure_path = './configure1.json'
plot_path = './plot.png'

a = src.pipeline(configure_path)

a.plot(plot_path)
