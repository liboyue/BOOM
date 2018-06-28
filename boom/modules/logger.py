import json
import glog as log
from .module import Module

class Logger(Module):
    "The Logger module saves logs sent to it to a file."

    def __init__(self, module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):
        super(Logger, self).__init__(module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs)
        ## The buffer for logs
        self.buf = []

    ## The function to handle incoming logs
    def receive_job(self, ch, method, properties, body):

        # Parse request body.
        data = json.loads(body.decode('ascii'))
        if data['type'] == 'log':
            ch.basic_ack(delivery_tag = method.delivery_tag)
            self.channel.stop_consuming()
            self.buf.append(data['body'])

            if len(self.buf) == 500:
                self.save()

            # Connect
            self.connect()

        elif data['type'] == 'command':
            cmd = json.loads(data['body'])
            ch.basic_ack(delivery_tag = method.delivery_tag)
            if cmd['module'] == self.id or cmd['module'] == -1:
                log.info('Module ' + str(self.id) + ' ' + self.name + ' received command ' + cmd['command'])

                if cmd['command'] == 'shutdown':
                    self.channel.stop_consuming()
                    self.is_finished = True
                    self.cleanup()

    ## The function to save files.
    def save(self):
        with open('log.txt', 'w+') as f:
            f.write('\n'.join(self.buf) + '\n')
        self.buf = []
        log.info('Saved logs')

    ## Clean up before exiting.
    def cleanup(self):
        if len(self.buf) > 0:
            self.save()

if __name__ == '__main__':
    pass
