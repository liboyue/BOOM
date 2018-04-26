from boom import Job
import json

json_str = json.dumps({
    'id': 0,
    'input_uri': 'uri',
    'output_base': 'output_base',
    'output_path': 'output_path',
    'params': None,
    'timestamp': str(None),
    'producer': 'producer',
    'consumer': 'consumer',
    'processing_time': 'processing_time',
    })

def test_init():
    job = Job(1, 'uri', 'output_base', 'output_path')

def test_from_json():
    job = Job.from_json(json_str)
    job.timestamp = None
    assert str(job) == json_str

def test_to_json():
    job = Job(0, 'uri', 'output_base', 'output_path')
    job.timestamp = None
    assert str(job) == json.dumps({
        'id': 0,
        'input_uri': 'uri',
        'output_base': 'output_base',
        'output_path': 'output_path',
        'params': None,
        'timestamp': str(None),
        'producer': None,
        'consumer': None,
        'processing_time': str(None)
        })
