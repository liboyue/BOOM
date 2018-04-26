from boom import Job
from boom.modules import Module
import yaml
import json

with open('tests/test_conf.yaml') as f:
    conf = yaml.load(f)

pipeline_conf = conf['pipeline']
module_conf = conf['modules'][0]

pipeline_conf_mongo = conf['pipeline'].copy()
pipeline_conf_mongo['use_mongodb'] = True

data = {'test': 'test'}

def test_init():
    global m
    m = Module(0, module_conf['name'], '127.0.0.1', pipeline_conf, module_conf)

def test_init_mongo():
    global m_m
    m_m = Module(0, module_conf['name'], '127.0.0.1', pipeline_conf_mongo, module_conf)

def test_get_name():
    assert m.get_name() == module_conf['name']

def test_parse_data():
    assert m.parse_data(json.dumps(data)) == data

def test_dump_data():
    assert m.dump_data(data) == json.dumps(data)

def test_save_job_data():
    job = Job(1, 'uri', 'tests/modules', 'temp.json')
    m.save_job_data(job, data)

def test_load_job_data():
    job = Job(1, 'uri', 'tests/modules', 'temp.json')
    assert m.load_job_data(job) == data

def test_save_job_data_mongo():
    job = Job(1, 'uri', 'tests/modules', 'temp.json')
    m_m.save_job_data(job, data)

def test_load_job_data_mongo():
    job = Job(1, 'uri', 'tests/modules', 'temp.json')
    assert m_m.load_job_data(job) == data

def test_process():
    pass
