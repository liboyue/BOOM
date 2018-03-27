import json
import pika
import glog as log
from ..job import Job
import yaml

from ast import literal_eval

class Module():
    """The base module class. Every actual module should be derived from this class."""

    def __init__(self, module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):

        ## The module's id.
        self.id = module_id

        ## The module's name.
        self.name = name

        ## The module's input file path. None if not exists.
        self.use_mongodb = pipeline_conf['use_mongodb'] if 'use_mongodb' in pipeline_conf else False

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

        ## The connection the module instance uses.
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))

        ## The channel the module instance uses.
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.name)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.receive_job, queue=self.name)


    def __str__(self):
        return json.dumps({
            'name': self.name,
            'id': self.id,
            })


    ## The function to handle incoming jobs.
    def receive_job(self, ch, method, properties, body):

        # Parse request body.
        data = json.loads(body.decode('ascii'))
        if data['type'] == 'job':
            job = Job.from_json(data['body'])
            log.info(self.name + ' received job: ' + str(job.id))
            log.debug(job)

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

            # Send back resulting job.
            ch.basic_publish(
                    exchange = 'job',
                    routing_key = properties.reply_to,
                    properties = pika.BasicProperties(),
                    body = job.to_json()
                    )

            ch.basic_ack(delivery_tag = method.delivery_tag)
            log.info(self.name + ' sent back job: ' + str(job.id))
            log.debug(job)

        elif data['type'] == 'command':
            cmd = json.loads(data['body'])
            ch.basic_ack(delivery_tag = method.delivery_tag)
            if cmd['module'] == self.id or cmd['module'] == -1:
                log.warn('Module ' + str(self.id) + ' ' + self.name + ' received command ' + cmd['command'])

                if cmd['command'] == 'shutdown':
                    self.channel.stop_consuming()


    ## Get the name of the mdoule.
    def get_name(self):
        return self.name

    ## Load Job from path or MongoDB.
    #  @param job The job object to load.
    #  @return The data loaded.
    def load_job_data(self, job):
        if self.use_mongodb == False:
            log.info('Load data from ' + job.input_uri)
            with open(job.input_uri) as f:
                return json.load(f)


    ## Save Job and data to file or MongoDB.
    #  @param job The job to be saved.
    #  @param data The data to be saved.
    #  @return the path to data.
    def save_job_data(self, job, data):
        if self.use_mongodb == False:
            path = job.output_base + job.output_path + '.json'
            log.info('Save data to ' + path)
            with open(path, 'w') as f:
                json.dump(data, f)
            return path


    ## The function to run the algorithm and process data objects.
    #  This function needs to be implemented in each class and should run the
    #  core algorithm for the module, save intermediate results and return the resulting data object.
    #  @param job The Job object to be processed.
    #  @param data The data to be processed.
    #  @return The processed data object.
    def process(self, job, data):
        pass


    ## The function to start the service.
    def run(self):
        log.info('Module ' + self.name + ' started, awaiting for requests.')
        self.channel.start_consuming()


if __name__ == '__main__':
    pass
