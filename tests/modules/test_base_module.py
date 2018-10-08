from boom import Job
from boom.modules import Module
import yaml
import json
from boom.utils import rabbitmq_status, mongodb_status, execute_cmd
import gflags
import sys 
import os
import time

with open('test_conf.yaml') as f:
    conf = yaml.load(f)

pipeline_conf = conf['pipeline']
module_conf = conf['modules'][0]

pipeline_conf_mongo = conf['pipeline'].copy()
pipeline_conf_mongo['use_mongodb'] = True

data = {'test': 'test'}

class TestBaseModule(object):

    def test_init(self):
        global m
        m = Module(0, module_conf['name'], 'TEST_EXP', '127.0.0.1', pipeline_conf, module_conf)

    def test_init_mongo(self):
        global m_m
        m_m = Module(0, module_conf['name'], 'TEST_EXP_MONGO', '127.0.0.1', pipeline_conf_mongo, module_conf)

    def test_get_name(self):
        assert m.get_name() == module_conf['name']

    def test_parse_data(self):
        assert m.parse_data(json.dumps(data)) == data

    def test_dump_data(self):
        assert m.dump_data(data) == json.dumps(data)

    def test_save_job_data(self):
        job = Job(1, 'uri', 'modules', 'temp.json')
        m.save_job_data(job, data)

    def test_load_job_data(self):
        job = Job(1, 'uri', 'modules', 'temp.json')
        assert m.load_job_data(job) == data

    def test_save_job_data_mongo(self):
        job = Job(1, 'uri', 'modules', 'temp.json')
        m_m.save_job_data(job, data)

    def test_load_job_data_mongo(self):
        job = Job(1, 'uri', 'modules', 'temp.json')
        assert m_m.load_job_data(job) == data
