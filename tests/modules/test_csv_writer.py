from boom import Job
from boom.modules import CSVWriter
import yaml
import json
import glog as log
from boom.utils import rabbitmq_status, mongodb_status, execute_cmd
import gflags
import sys 
import os
import time

with open('test_conf.yaml') as f:
    conf = yaml.load(f)

pipeline_conf = conf['pipeline']
module_conf = conf['modules'][1]

pipeline_conf_mongo = conf['pipeline'].copy()
pipeline_conf_mongo['use_mongodb'] = True

data = {'test': 1}

def test_init():
    global m
    m = CSVWriter(0, module_conf['name'], 'TEST_EXP', '127.0.0.1', pipeline_conf, module_conf)

def test_init_mongo():
    global m_m
    m_m = CSVWriter(0, module_conf['name'], 'TEST_EXP_MONGO', '127.0.0.1', pipeline_conf_mongo, module_conf)

def test_process():
    job = Job(1, 'uri', 'modules', '')
    m.process(job, data)

def test_process_mongo():
    job = Job(1, 'uri', 'modules', '')
    m_m.process(job, data)

def test_save_job_data():
    job = Job(1, 'uri', 'modules', '')
    m.save_job_data(job, data)

def test_save_job_data_mongo():
    job = Job(1, 'uri', 'modules', '')
    m_m.save_job_data(job, data)
