from datetime import datetime
import json

import glog as log


class Job(object):
    """The information object class."""

    def __init__(self, job_id, input_uri, output_base, output_path, params=None,
                 producer=None, consumer=None, processing_time=None):

        ## The id of this job
        self.id = job_id
        ## The uri to the data file.
        self.input_uri = input_uri
        ## The base uri/db to save a new data file.
        self.output_base = output_base
        ## The path/key to save a new data file.
        self.output_path = output_path
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

        log.debug('Creating data object: ' + str(self))


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
            'id': self.id,
            'input_uri': self.input_uri,
            'output_base': self.output_base,
            'output_path': self.output_path,
            'params': self.params,
            'timestamp': str(self.timestamp),
            'producer': self.producer,
            'consumer': self.consumer,
            'processing_time': str(self.processing_time)
            })


    ## Deserialize the object from a json formatted string.
    #  @param json_str the json formatted string.
    #  @return the deserialize Job object.
    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return Job(
            data['id'],
            data['input_uri'],
            data['output_base'],
            data['output_path'],
            data['params'],
            data['producer'],
            data['consumer'],
            data['processing_time'],
            )
