import boom
from boom import Pipeline
import os
import pika
import time

from boom import Job
from boom.modules import Module
import yaml
import json
import gflags
import sys 
import shutil
import pytest

from time import sleep
from boom.utils import rabbitmq_status, mongodb_status, execute_cmd



# Load data
with open('test_conf.yaml') as f:
    conf = yaml.load(f)

conf_mongo = conf.copy()
conf_mongo['pipeline']['use_mongodb'] = True

data = {'test': 'test'}

gflags.DEFINE_string('conf', 'conf.yaml', 'path to the configuration file')
gflags.DEFINE_string('tmp_dir', 'tmp', 'path to the temporare directory')
gflags.DEFINE_boolean('plot', False, 'plots the pipeline')
gflags.DEFINE_boolean('profile', False, 'profile each module')
gflags.DEFINE_boolean('help', False, 'print the help message')
gflags.DEFINE_boolean('info', False, 'print details about the pipeline, including how many modules, how many jobs, etc.')
gflags.DEFINE_boolean('debug', False, 'debugging mode for the pipeline. Prints all command without execution.')

# Parse args.
FLAGS = gflags.FLAGS
sys.argv = [sys.argv[0]] + sys.argv[3:]
FLAGS(sys.argv)

def test_init():
    global p
    p = Pipeline(json.dumps(conf), 'TEST_EXP')

def test_init_mongo():
    global p_m
    p_m = Pipeline(json.dumps(conf_mongo), 'TEST_EXP_MONGO')

def test_calculate_total_jobs():
    assert p.calculate_total_jobs(conf) == 36

def test_plot():
    p.plot()

def test_expand_params():
    a = p.expand_params(conf['modules'][0])
    assert len(list(a)) == 18

def test_send_job():
    job = Job(0, 'uri', 'output_base', 'output_path')
    name = conf['modules'][0]['name']
    p.send_job(name, job)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
    channel = connection.channel()
    channel.queue_declare(queue=name)
    channel.basic_qos(prefetch_count=1)

    def _callback(ch, method, properties, body):
        ch.basic_ack(delivery_tag = method.delivery_tag)
        data = json.loads(body.decode('ascii'))
        received_job = Job.from_json(data['body'])
        channel.stop_consuming()
        received_job.timestamp = job.timestamp
        assert str(job) == str(received_job)

    channel.basic_consume(_callback, queue=name)
    channel.start_consuming()

def test_get_output_dir():
    path = p.get_output_dir() 
    assert os.path.isdir(path)
