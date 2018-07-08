import json
import logging

import glog as log
import pika
import pymongo
import gridfs

from ..log import set_logger
from ..job import Job

# Disable Pika's debugging messages
logging.getLogger("pika").propagate = False


class Module(object):
    """The base module class. Every actual module should be derived from this class."""

    ## Initialization.
    def __init__(self, module_id, name, exp_name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):

        ## The module's id.
        self.id = module_id

        ## The module's name.
        self.name = name

        ## The experiment's name.
        self.exp_name = exp_name

        # Initialize logger.
        set_logger(rabbitmq_host, self.exp_name)

        ## The module's input file path. None if not exists.
        self.use_mongodb = pipeline_conf['use_mongodb'] if 'use_mongodb' in pipeline_conf else False
        if self.use_mongodb:
            ## MongoDB's host.
            self.mongodb_host = pipeline_conf['mongodb_host']
            ## The gridfs object used by the pipeline.
            self.fs = gridfs.GridFS(
                pymongo.MongoClient(self.mongodb_host).boom
                )

        ## The module's input file path. None if not exists.
        self.input_file = module_conf['input_file'] if 'input_file' in module_conf else None

        ## The module's output file path. None if not exists.
        self.output_file = module_conf['output_file'] if 'output_file' in module_conf else None

        ## The module's input module's name. None if not exists.
        self.input_module = module_conf['input_module'] if 'input_module' in module_conf else None

        ## The module's output module's name. None if not exists.
        self.output_module = module_conf['output_module'] if 'output_module' in module_conf else None

        ## The RabbitMQ server name/IP/url.
        self.rabbitmq_host = rabbitmq_host

        ## The exchange the pipeline uses.
        self.exchange = ''

        # Work around for the time out problem.
        self.is_finished = False

        # Connect
        self.connect()


    def __str__(self):
        return json.dumps({
            'name': self.name,
            'id': self.id,
            })


    ## The function to (re)connect to RabbitMQ server.
    def connect(self):

        ## The connection the module instance uses.
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.rabbitmq_host,
                heartbeat_interval=0,
                blocked_connection_timeout=0
                )
            )

        ## The channel the module instance uses.
        self.channel = self.connection.channel()

        ## The queue the module instance uses.
        self.queue = self.channel.queue_declare(queue=self.name)
        self.channel.basic_qos(prefetch_count=1)

        # Connect to RabbitMQ
        self.channel.basic_consume(self.receive_job, queue=self.name)


    ## The function to handle incoming jobs.
    def receive_job(self, ch, method, properties, body):

        # Parse request body.
        data = json.loads(body.decode('ascii'))
        if data['type'] == 'job':
            ch.basic_ack(delivery_tag=method.delivery_tag)
            self.channel.stop_consuming()
            job = Job.from_json(data['body'])
            log.info(self.name + ' received job: ' + str(job.id))

            # Load data.
            data = self.load_job_data(job)

            # Process data.
            data = self.process(job, data)

            # Update job info.
            job.producer = self.name
            job.consumer = self.output_module
            job.output_path += self.name + '_' + json.dumps(job.params) + '_'

            # Save data and update the data uri.
            job.input_uri = self.save_job_data(job, data)

            # Update timestampe and processing time.
            job.update_timestamp()

            # Connect
            self.connect()
            # Send back resulting job.
            self.channel.basic_publish(
                exchange='job',
                routing_key=properties.reply_to,
                properties=pika.BasicProperties(),
                body=job.to_json()
                )

            log.info(self.name + ' sent back job: ' + str(job.id))

        elif data['type'] == 'command':
            cmd = json.loads(data['body'])
            ch.basic_ack(delivery_tag=method.delivery_tag)
            if cmd['module'] == self.id or cmd['module'] == -1:
                log.warn('Module ' + str(self.id) + ' ' + self.name + ' received command ' + cmd['command'])

                if cmd['command'] == 'shutdown':
                    self.channel.stop_consuming()
                    self.is_finished = True
                    self.cleanup()


    ## Get the name of the mdoule.
    def get_name(self):
        return self.name

    ## Clean up before exiting.
    def cleanup(self):
        pass

    ## Load Job from path or MongoDB.
    #  @param job The job object to load.
    #  @return The data loaded.
    def load_job_data(self, job):
        if self.use_mongodb is False:
            path = job.output_base + '/' + job.output_path if job.output_path != "" else job.input_uri
            log.info('Load data from file ' + path)
            with open(path) as f:
                return self.parse_data(f.read())
        else:
            log.info('Load data from MongoDB ' + job.output_path)
            data = self.fs.find_one({"filename": job.output_path, "metadata": job.output_base}, no_cursor_timeout=True) \
                    .read() \
                    .decode("utf-8")
            return self.parse_data(data)



    ## Save Job and data to file or MongoDB.
    #  @param job The job to be saved.
    #  @param data The data to be saved.
    #  @return the path to data.
    def save_job_data(self, job, data):
        if self.use_mongodb is False:
            path = job.output_base + '/' + job.output_path
            log.info('Save data to file ' + path)
            with open(path, 'w') as f:
                f.write(self.dump_data(data))
        else:
            log.info('Save data to MongoDB ' + job.output_path)
            self.fs.put(
                str.encode(self.dump_data(data)),
                filename=job.output_path,
                metadata=job.output_base
                )
        return job.output_path


    ## Parse the loaded data
    #  @param data The data to be parsed.
    #  @return the parsed data.
    def parse_data(self, data):
        return json.loads(data)


    ## Dump the data to string
    #  @param data The data to be dumped.
    #  @return the dumped data.
    def dump_data(self, data):
        return json.dumps(data)


    ## The function to run the algorithm and process data objects.
    #  This function needs to be implemented in each class and should run the
    #  core algorithm for the module, save intermediate results and return the
    #  resulting data object.
    #  @param job The Job object to be processed.
    #  @param data The data to be processed.
    #  @return The processed data object.
    def process(self, job, data):
        pass


    ## The function to start the service.
    def run(self):
        log.info('Module ' + self.name + ' started, awaiting for requests.')

        while self.is_finished is False:
            self.channel.start_consuming()


if __name__ == '__main__':
    pass
