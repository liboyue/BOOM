import json
import pika
import glog as log
from ..data import Data

class Module():
    """The base module class. Every actual module should be derived from this class."""

    def __init__(self, conf, host):

        ## The configuration file.
        self.conf = conf

        ## The module's name.
        self.name = conf['name']

        ## The module's input file path. None if not exists.
        self.input_file = conf['input_file'] if 'input_file' in conf else None

        ## The module's output file path. None if not exists.
        self.output_file = conf['output_file'] if 'output_file' in conf else None

        ## The module's input module's name. None if not exists.
        self.input_module = conf['input_module'] if 'input_module' in conf else None

        ## The module's output module's name. None if not exists.
        self.output_module = conf['output_module'] if 'output_module' in conf else None

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
        return json.dumps(self.conf)


    ## The function to handle incoming jobs.
    def receive_job(self, ch, method, properties, body):

        # Parse request body.
        data = Data.from_json(body.decode('ascii'))
        log.info(self.name + ' received job: ' + str(data))

        # Process data.
        data = self.process(data)
        data.update_timestamp()

        # Update timestampe and processing time.

        # Send back resulting data.
        ch.basic_publish(
                exchange = self.exchange,
                routing_key = properties.reply_to,
                properties = pika.BasicProperties(),
                body = data.to_json()
                )

        ch.basic_ack(delivery_tag = method.delivery_tag)
        log.info(self.name + ' sent back job: ' + str(data))


    ## Get the configuration of the mdoule.
    def get_conf(self):
        return self.conf


    ## Get the name of the mdoule.
    def get_name(self):
        return self.name

    ## Load data from path.
    #  @param path The path to load data.
    #  @return The data to loaded.
    def read_from(self, path):
        with open(path) as f:
            return json.load(f)


    ## Save data object to path.
    #  @param data The data to be saved.
    #  @param path The path to save data.
    def save_to(self, data, path):
        with open(path, 'w') as f:
            json.dump(data, f)


    ## The function to run the algorithm and process data objects.
    #  This function needs to be implemented in each class and should run the
    #  core algorithm for the module, save intermediate results and return the resulting data object.
    #  @param data Data object to be processed.
    #  @return The processed data object.
    def process(self, data):
        pass


    ## The function to start the service.
    def run(self):
        log.info('Module ' + self.name + ' started, awaiting for requests.')
        self.channel.start_consuming()


if __name__ == '__main__':
    pass
