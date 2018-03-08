from src import Job
import json

json_str = json.dumps({
    'id': 0,
    'data_uri': 'uri',
    'save_uri': 'save_uri',
    'params': None,
    'timestamp': str(None),
    'producer': 'producer',
    'consumer': 'consumer',
    'processing_time': 'processing_time',
    })

def test_init():
    job = Job(1, 'uri', 'save_uri')

def test_from_json():
    job = Job.from_json(json_str)
    job.timestamp = None
    assert str(job) == json_str

def test_to_json():
    job = Job(0, 'uri', 'save_uri')
    job.timestamp = None
    assert str(job) == json.dumps({
        'id': 0,
        'data_uri': 'uri',
        'save_uri': 'save_uri',
        'params': None,
        'timestamp': str(None),
        'producer': None,
        'consumer': None,
        'processing_time': str(None)
        })
