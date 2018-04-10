import pika
import glog as log
from ..logger import Logger

class LogCollector():

    def __init__(self, rabbitmq_host):

        ## The RabbitMQ server name/IP/url.
        self.rabbitmq_host = rabbitmq_host

        ## The connection the module instance uses.
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))

        ## The channel the module instance uses.
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='log', exchange_type='direct')
        self.channel.queue_declare(queue='log')
        self.channel.basic_qos(prefetch_count=1)
        self.channel.queue_bind(exchange='log', queue='log')
        self.channel.basic_consume(self.receive_job, queue='log')

        self.f = open('log.txt', 'w+')
        

    ## The function to handle incoming jobs.
    def receive_job(self, ch, method, properties, body):

        print('\n\nhahahahah                ' + body.decode('ascii') + '\n\n')
        self.f.write(body.decode('ascii'))
        return

        if data['type'] == 'job':
            pass
        elif data['type'] == 'command':
            cmd = json.loads(data['body'])
            ch.basic_ack(delivery_tag = method.delivery_tag)
            if cmd['module'] == self.id or cmd['module'] == -1:
                log.warn('Module ' + str(self.id) + ' ' + self.name + ' received command ' + cmd['command'])

                if cmd['command'] == 'shutdown':
                    self.channel.stop_consuming()
                    quit()

    ## The function to start the service.
    def run(self):
        log.warn('LogCollector started, awaiting for requests.')
        self.channel.start_consuming()

    def __del__(self):
        self.f.close()

if __name__ == '__main__':
    pass
