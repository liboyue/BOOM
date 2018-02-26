import json
import bson
import glog as log
from datetime import datetime

class Data:
    """The information object class."""
    
    def __init__(self, data_uri, save_uri, params = None, producer = None, consumer = None, processing_time = None):
        ## The uri to the data file.
        self.data_uri = data_uri
        ## The uri to save a new data file.
        self.save_uri = save_uri
        ## The params may be needed.
        self.params = params
        ## The timastampe when the object is created.
        self.timestamp = datetime.utcnow()
        ## The producer of the data obejct.
        self.producer = producer
        ## The consumer of the data obejct.
        self.consumer = consumer
        ## The time to process the data object.
        self.processing_time = processing_time

        log.debug('Creating data object, uri: ' + data_uri)


    def __str__(self):
        return self.to_json()


    ## Update the timestampe and processing time.
    def update_timestamp(self):
        tmp = self.timestamp
        self.timestamp = datetime.utcnow()
        self.processing_time = self.timestamp - tmp
        

    ## Serialize the object to a json formatted string.
    #  @return the serialized json string.
    def to_json(self):
        return json.dumps({
            'data_uri': self.data_uri,
            'save_uri': self.save_uri,
            'params': self.params,
            'timestamp': str(self.timestamp),
            'producer': self.producer,
            'consumer': self.consumer,
            'processing_time': str(self.processing_time)
            })


    ## Deserialize the object from a json formatted string.
    #  @param data the json formatted string.
    #  @return the deserialize data object.
    def from_json(json_str):
        data = json.loads(json_str)
        return Data(
                data['data_uri'],
                data['save_uri'],
                data['params'],
                data['producer'],
                data['consumer'],
                data['processing_time'],
                )
