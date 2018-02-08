#!/usr/bin/env python
# coding=utf-8
import src


configure_path = './configure1.json'
plot_path = './plot.png'

p = src.pipeline(configure_path)
print(p)
p.draw(plot_path)
