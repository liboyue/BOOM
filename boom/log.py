import logging
import sys
import json

import glog as log
import pika
import gflags as flags

FLAGS = flags.FLAGS

# Disable Pika's debugging messages.
logging.getLogger("pika").propagate = False

class RabbitHandler(logging.Handler):

    ## The terminator.
    terminator = '\n'

    ##  Initialization.
    #  @param rabbitmq_host The RabbitMQ server's name/IP/url.
    def __init__(self, rabbitmq_host, exp_name):
        super(RabbitHandler, self).__init__()
        super(RabbitHandler, self).setLevel(FLAGS.verbosity)

        ## The interanl variable passing messages between functions.
        self.msg = ''

        ## The RabbitMQ server's name/IP/url.
        self.rabbitmq_host = rabbitmq_host

        ## The experiment's name.
        self.exp_name = exp_name

        # Connect to RabbitMQ server.
        self.connect()

    ## The function to connect to RabbitMQ server.
    def connect(self):

        ## The connection the pipeline instance uses.
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))

        ## The channel the logger instance uses.
        self.channel = self.connection.channel()

        ## The exchange the logger uses.
        self.channel.exchange_declare(exchange='job', exchange_type='direct')

        ## The queue to logger module.
        self.queue = self.channel.queue_declare(queue='logger').method.queue

        # Bind queue.
        self.channel.queue_bind(exchange='job', queue=self.queue)

    ## Flush function.
    def flush(self):
        self.acquire()

        try:
            if self.msg != '':
                self.channel.basic_publish(
                    exchange='job',
                    routing_key=self.queue,
                    properties=pika.BasicProperties(),
                    body=json.dumps({
                        'type': 'log',
                        'body': self.msg
                        })
                    )
        finally:
            self.msg = ''
            self.release()

    ## Emit function.
    def emit(self, record):

        try:
            self.msg = self.format(record)
            self.flush()

        except Exception:
            self.handleError(record)

## The function that updates the logger.
#  @param rabbitmq_host The RabbitMQ host.
#  @param exp_name The experiment's name.
def set_logger(rabbitmq_host=None, exp_name=None):
    FLAGS(sys.argv)
    if rabbitmq_host != None:
        log.logger.addHandler(RabbitHandler(rabbitmq_host, exp_name))
