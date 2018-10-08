import os
import shutil
import time
import json
import logging

import pika
import pydotplus
import glog as log
import gridfs
import pymongo

from .log import set_logger
from .job import Job
from .parameter import Parameter

# Disable Pika's debugging messages
logging.getLogger("pika").propagate = False


class Pipeline(object):
    "The pipeline class creates the pipeline, and manages execution."

    ##  Initialization.
    #  @param conf The Json serialized configuration file.
    #  @param exp_name The name of the experiment.
    def __init__(self, conf, exp_name):

        ## The internal job ID counter. It is the id of next job to use.
        self.cur_job_id = 0

        ## Content of the configuration file.
        self.conf = json.loads(conf)

        # Initialize logger.
        set_logger(self.conf['pipeline']['rabbitmq_host'], exp_name)

        log.info('Loading configuration file')
        log.info(json.dumps(self.conf, indent=4))

        ## Name of the pipeline.
        self.name = self.conf['pipeline']['name']

        ## Name of the experiment.
        self.exp_name = exp_name

        ## Clean up or not after running.
        self.clean_up = self.conf['pipeline']['clean_up'] if 'clean_up' in self.conf['pipeline'] else False

        ## Use MongoDB or not.
        self.use_mongodb = self.conf['pipeline']['use_mongodb'] if 'use_mongodb' in self.conf['pipeline'] else False

        if self.use_mongodb:
            ## MongoDB's host.
            self.mongodb_host = self.conf['pipeline']['mongodb_host']

        ## The configuration of each module.
        self.modules = {mod_conf['name']: mod_conf for mod_conf in self.conf['modules']}
        log.info('Module list: ' + str(self.modules))

        ## The total number of jobs.
        self.n_jobs = self.calculate_total_jobs(self.conf)
        log.info('Total jobs: ' + str(self.n_jobs))

        ## Set of all running jobs.
        self.job_status = set()

        ## The RabbitMQ server name/IP/url.
        self.rabbitmq_host = self.conf['pipeline']['rabbitmq_host']

        ## The connection the pipeline instance uses.
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.rabbitmq_host)
            )

        ## The channel the pipeline instance uses.
        self.channel = self.connection.channel()

        ## The exchange the pipeline uses.
        self.channel.exchange_declare(exchange='job', exchange_type='direct')

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

        self.module_queues['logger'] = self.channel.queue_declare(queue='logger').method.queue

        ## Bind queues
        for queue in self.module_queues:
            self.channel.queue_bind(exchange='job', queue=queue)

        self.channel.queue_bind(exchange='job', queue=self.callback_queue)


        ## The name of dir or database to save results.
        self.output_base = self.exp_name
        time.strftime("%Y-%m-%d_%Hh%Mm%Ss", time.localtime())

        # Clean up data dir if needed
        if os.path.isdir(self.output_base) is True:
            shutil.rmtree(self.output_base)

        # Create data dir
        os.mkdir(self.output_base)


    def __str__(self, module=None, indent=0):
        return json.dumps(self.conf, indent=4)

    ## The function to calculate total number of jobs.
    #  @param conf the pipeline's configuration.
    #  @return the total number of jobs.
    def calculate_total_jobs(self, conf):
        total = 0
        level = 1
        for mod in conf['modules']:
            if 'params' in mod and mod['params'] != None:
                for param in mod['params']:
                    level *= Parameter(param).get_n_choices()
            total += level
        return int(total)

    ## The function to plot the pipeline.
    def plot(self):
        fig = pydotplus.Dot(graph_name=self.conf['pipeline']['name'], rankdir="LR",
                            labelloc='b', labeljust='r', ranksep=1)
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
            if 'params' in module:
                for param in module['params']:
                    if param['type'] == 'collection':
                        label += 'param ' + param['name'] + ' values: [' + ','.join(param['values']) + ']\n'
                    else:
                        label += 'param ' + param['name'] + ' range: [' + str(param['start']) + ', ' + str(param['step_size']) + ', ' + str(param['end']) + ']\n'

            modules.append(
                pydotplus.Node(
                    name=module['name'],
                    texlbl=module['name'],
                    label=module['name'] + '\ntype: ' + module['type'] + '\n' + label + 'instances: ' + str(module['instances'])
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

        fig.write_png(self.conf['pipeline']['name'] + '.png')


    ## The function to generate practical configurations for modules to run.
    #  @return Job objects.
    def expand_params(self, mod_conf, i=0):
        if 'params' in mod_conf and mod_conf['params'] != None and i < len(mod_conf['params']):
            for tmp in self.expand_params(mod_conf, i+1):
                for val in Parameter(mod_conf['params'][i]).get_values():
                    tmp[mod_conf['params'][i]['name']] = val
                    yield tmp
        else:
            yield {}


    ## The function to handle call back jobs.
    def on_call_back(self, ch, method, props, body):
        job = Job.from_json(body.decode('ascii'))
        self.job_status.remove(job.id)

        if job.consumer != None:
            # Send job to the following module.
            conf = {}
            for module in self.conf['modules']:
                if module['name'] == job.consumer:
                    conf = module
                    break

            for params in self.expand_params(conf):
                job.params = params
                job.id = self.cur_job_id
                self.cur_job_id += 1
                self.send_job(job.consumer, job)

            ch.basic_ack(delivery_tag=method.delivery_tag)

        else:
            # Job compeleted
            log.info('Job ' + str(job.id) + ' completed.')
            #log.debug(job)
            ch.basic_ack(delivery_tag=method.delivery_tag)

            # When received the last job.
            if job.id == self.n_jobs - 1:

                # Make sure all jobs finished.
                flag = True
                while flag:
                    flag = False
                    #log.debug(self.job_status)
                    if len(self.job_status) > 0:
                        flag = True
                        time.sleep(1)

                # Shut down the pipeline.
                for module in self.conf['modules']:
                    for _ in range(module['instances']):
                        self.send_command(module['name'], -1, 'shutdown')
                self.send_command('logger', -1, 'shutdown')


                log.warn('All jobs are completed, shutting down the pipeline')
                self.channel.stop_consuming()

                if self.clean_up:
                    log.warn('Cleaning up intermediate files')
                    if self.use_mongodb:
                        fs = gridfs.GridFS(
                            pymongo.MongoClient(self.mongodb_host).boom
                            )
                        for grid_out in fs.find({"metadata": self.output_base}, no_cursor_timeout=True):
                            fs.delete(grid_out._id)
                    else:
                        os.system('rm ' + self.output_base + '/*.json')
                quit()


    ## Send one job to one module.
    #  @param module_name The name of target module.
    #  @param job The job object.
    def send_job(self, module_name, job):
        self.channel.basic_publish(
            exchange='job',
            routing_key=self.module_queues[module_name],
            properties=pika.BasicProperties(
                reply_to=self.callback_queue
                ),
            body=json.dumps({'type': 'job', 'body': job.to_json()})
            )
        self.job_status.add(job.id)
        log.info('Sent job ' + str(job.id) + ' to module ' + module_name)


    ## Send one job to one module.
    #  @param module_name The name of target module.
    #  @param job The job object.
    def send_command(self, module_name, module_id, command):
        self.channel.basic_publish(
            exchange='job',
            routing_key=self.module_queues[module_name],
            properties=pika.BasicProperties(
                reply_to=self.callback_queue
            ),
            body=json.dumps({
                'type': 'command',
                'body': json.dumps({
                    'module': module_id,
                    'command': command})
                })
        )
        log.info('Sent command ' + command + ' to module ' + module_name + ', ' + str(module_id))


    ## The function to move data to MongoDB.
    def move_data_to_mongodb(self):
        gridfs.GridFS(pymongo.MongoClient(self.conf['pipeline']['mongodb_host']).boom) \
                .put(
                    str.encode(open(self.conf['modules'][0]['input_file']).read()),
                    filename=self.conf['modules'][0]['input_file'],
                    metadata=self.exp_name
                    )
        log.info('Saved data to MongoDB')


    ## The function to run the pipeline
    def run(self):

        # Move data to the exp folder.
        if self.conf['pipeline']['use_mongodb'] is True:
            self.move_data_to_mongodb()
        else:
            shutil.copyfile(self.conf['modules'][0]['input_file'], self.exp_name + '/' + self.conf['modules'][0]['input_file'])

        # Send the first job.
        for params in self.expand_params(self.conf['modules'][0]):
            self.send_job(
                self.conf['modules'][0]['name'],
                Job(
                    self.cur_job_id,
                    self.conf['modules'][0]['input_file'],
                    self.output_base,
                    self.conf['modules'][0]['input_file'],
                    params,
                    self.conf['modules'][0]['name'],
                    self.conf['modules'][0]['output_module']
                    )
                )
            self.cur_job_id += 1

        # Start running
        self.channel.start_consuming()

    ## The function to get the output directory of the pipeline.
    #  @return the path of the output directory
    def get_output_dir(self):
        return self.output_base

if __name__ == '__main__':
    pass
