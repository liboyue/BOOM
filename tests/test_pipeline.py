from boom import Pipeline
from boom import Parameter
import os
import pika

from boom import Job
from boom.modules import Module
import yaml
import json

from time import sleep

with open('tests/test_conf.yaml') as f:
    conf = yaml.load(f)

conf_mongo = conf.copy()
conf_mongo['pipeline']['use_mongodb'] = True

data = {'test': 'test'}

def test_init():
    global p
    p = Pipeline('tests/test_conf.yaml')

def test_init_mongo():
    sleep(1) # Pause for 1 sec in case two piplines would use the same directory.
    global p_m
    p_m = Pipeline('tests/test_conf_mongo.yaml')

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
