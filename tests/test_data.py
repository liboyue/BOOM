from src import Data
import json

json_str = json.dumps({
        'data_uri': 'uri',
        'timestamp': str(None),
        'producer': 'producer',
        'consumer': 'consumer',
        'processing_time': 'processing_time',
        })

def test_init():
    data = Data('uri')

def test_from_json():
    data = Data.from_json(json_str)
    data.timestamp = None
    assert str(data) == json_str

def test_to_json():
    data = Data('uri')
    data.timestamp = None
    assert str(data) == json.dumps({
            'data_uri': 'uri',
            'timestamp': str(None),
            'producer': None,
            'consumer': None,
            'processing_time': str(None)
            })
