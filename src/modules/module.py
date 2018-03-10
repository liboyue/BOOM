import json
import pika
import glog as log
from ..job import Job

class Module():
    """The base module class. Every actual module should be derived from this class."""

    def __init__(self, module_id, name, host, **kwargs):

        ## The module's id.
        self.id = module_id

        ## The module's name.
        self.name = name

        ## The module's input file path. None if not exists.
        self.input_file = kwargs['input_file'] if 'input_file' in kwargs else None

        ## The module's output file path. None if not exists.
        self.output_file = kwargs['output_file'] if 'output_file' in kwargs else None

        ## The module's input module's name. None if not exists.
        self.input_module = kwargs['input_module'] if 'input_module' in kwargs else None

        ## The module's output module's name. None if not exists.
        self.output_module = kwargs['output_module'] if 'output_module' in kwargs else None

        ## The RabbitMQ server name/IP/url.
        self.host = host

        ## The exchange the pipeline uses.
        self.exchange = ''
 
        ## The connection the module instance uses.
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))

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

            # Process job.
            job.producer = self.name
            job.consumer = self.output_module
            job.save_uri = job.save_uri + self.name + '_' + json.dumps(job.params) + '_'

            job = self.process(job)
            job.update_timestamp()

            # Update timestampe and processing time.

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
                    quit()
                    


    ## Get the name of the mdoule.
    def get_name(self):
        return self.name

    ## Load Job from path.
    #  @param path The path to load job.
    #  @return The job to loaded.
    def read_from(self, path):
        with open(path) as f:
            return json.load(f)


    ## Save Job object to path.
    #  @param job The job to be saved.
    #  @param path The path to save the job.
    def save_to(self, job, path):
        with open(path, 'w') as f:
            json.dump(job, f)


    ## The function to run the algorithm and process data objects.
    #  This function needs to be implemented in each class and should run the
    #  core algorithm for the module, save intermediate results and return the resulting data object.
    #  @param job Job object to be processed.
    #  @return The processed data object.
    def process(self, job):
        pass


    ## The function to start the service.
    def run(self):
        log.info('Module ' + self.name + ' started, awaiting for requests.')
        self.channel.start_consuming()


if __name__ == '__main__':
    pass
