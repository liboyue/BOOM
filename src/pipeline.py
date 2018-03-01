import yaml
import json
import glog as log
import os
import time
import pika
from .data import Data
from .modules import *
from .parameter import Parameter
import pydotplus

class Pipeline:
    "The pipeline class creates the pipeline, and manages execution."
    
    ##  Initialization.
    #  @param conf_path The path to the configuration file.
    def __init__(self, conf_path):

        ## The path to the configuration file.
        self.conf_path = conf_path

        with open(conf_path) as f:
            ## Content of the configuration file.
            self.conf = yaml.load(f)

        log.info('Loading configuration file from ' + conf_path)
        log.info(json.dumps(self.conf, indent = 4))

        ## Name of the pipeline.
        self.name = self.conf['name']

        ## The RabbitMQ server name/IP/url.
        self.host = self.conf['host']

        ## The exchange the pipeline uses.
        self.exchange = ''
        
        ## The configuration of each module.
        self.modules = {mod_conf['name']: mod_conf for mod_conf in self.conf['modules']}
        log.info('Module list: ' + str(self.modules))

        ## The connection the pipeline instance uses.
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))

        ## The channel the pipeline instance uses.
        self.channel = self.connection.channel()

        ## The confirmation queue the pipeline instance uses.
        self.callback_queue = self.channel.queue_declare(queue='call_back').method.queue

        # Set parameters.
        self.channel.basic_consume(
                self.on_call_back,
                queue=self.callback_queue
                )

        ## The queue to each module.
        self.module_queues = {
                mod['name']: self.channel.queue_declare(queue=mod['name']).method.queue for mod in self.conf['modules']
                }

        ## The directory to save results.
        self.save_dir = time.strftime("%Y-%m-%d_%Hh%Mm%Ss", time.localtime()) + '/'
        os.mkdir(self.save_dir)


    def __str__(self, module=None, indent=0):
        return json.dumps(self.conf, indent = 4)


    ## Check if the configuration is valid.
    #  @return True if valid, False otherwise.
    def _check_pipeline(self, ind=0, parents=[]):
        if len(self.modules) == 0:
            return False

        self.modules[ind]
        children = self.modules[ind]

        if name not in modules:
            return False

        if "output_files" in modules[name]:
            return True

        for next_name in modules[name]['outputs']:
            if self._check_pipeline(next_name, modules) == False:
                return False

        return True

    def plot(self):
        fig = pydotplus.Dot(graph_name=self.conf['name'],rankdir="LR", labelloc='b', labeljust='r', ranksep=1)
        fig.set_node_defaults(shape='square')

        modules = []

        for module in self.conf['modules']:

            if 'input_file' in module:
                modules.append(
                    pydotplus.Node(
                        name='input_file',
                        texlbl='Input file\n' + module['input_file'],
                        label='Input file\n' + module['input_file']
                        )
                    )

            label = ''
            for params in module['params']:
                label += 'param ' + params['name'] + ' range: [' + str(params['start']) + ', ' + str(params['step_size']) + ', ' + str(params['end']) + ']\n' 

            modules.append(
                pydotplus.Node(
                    name=module['name'],
                    texlbl=module['name'],
                    label=module['name'] + '\ntype: ' + module['type'] + '\n' + label
                    )
                )

            if 'output_file' in module:
                modules.append(
                    pydotplus.Node(
                        name='output_file',
                        texlbl='Output file' + module['output_file'],
                        label='Output file\n' + module['output_file']
                        )
                    )

        for node in modules:
            fig.add_node(node)

        for i in range(len(modules)-1):
            fig.add_edge(pydotplus.Edge(modules[i], modules[i+1]))

        fig.write_png(self.conf['name'] + '.png')


    ## The function to generate practical configurations for modules to run.
    #  @return Data objects. 
    def expand_params(self, mod_conf, i = 0):
        if i < len(mod_conf['params']):
            for tmp in self.expand_params(mod_conf, i+1):
                for val in range(
                        mod_conf['params'][i]['start'],
                        mod_conf['params'][i]['end'] + mod_conf['params'][i]['step_size'],
                        mod_conf['params'][i]['step_size']
                        ):
                    yield {**{mod_conf['params'][i]['name']: val}, **tmp}
        else:
            yield {}


    ## The function to handle call back jobs.
    def on_call_back(self, ch, method, props, body):
        data = Data.from_json(body.decode('ascii'))

        if data.consumer != None:
            # Send job to the following module
            self.send_job(data.consumer, data)
        else:
            # Job compeleted
            log.info('Job completed ' + str(data))

        ch.basic_ack(delivery_tag = method.delivery_tag)


    ## Send one job to one module.
    #  @param module_name The name of target module.
    #  @param data The data object.
    def send_job(self, module_name, data):
        self.channel.basic_publish(
                exchange = self.exchange,
                routing_key = self.module_queues[module_name],
                properties = pika.BasicProperties(
                    reply_to = self.callback_queue
                    ),
                body = data.to_json()
                )
        log.info('Sent job to module ' + module_name)


    ## The function to run the pipeline
    def run(self):

        # Send the first job.
        for params in self.expand_params(self.conf['modules'][0]):
            self.send_job(
                    self.conf['modules'][0]['name'],
                    Data(
                        self.conf['modules'][0]['input_file'],
                        self.save_dir,
                        params,
                        self.conf['modules'][0]['input_file'],
                        self.conf['modules'][0]['name'],
                        self.conf['modules'][0]['output_module']
                        )
                    )

        # Start running
        self.channel.start_consuming()
