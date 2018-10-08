'''The utilities functions shared within BOOM'''

import pika
import glog as log
import pymongo
import gflags
import subprocess

FLAGS = gflags.FLAGS

## The function to test if RabbitMQ is running
#  @param rabbitmq_host The host of RabbitMQ server
#  @return True if RabbitMQ is running, False otherwise
def rabbitmq_status(rabbitmq_host):
    try:
        pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        return True
    except:
        return False


## The function to test if MongoDB server is running
#  @param mongodb_host The host of MongoDB server
#  @return True if MongoDB is running, False otherwise
def mongodb_status(mongodb_host):
    try:
        pymongo.MongoClient(mongodb_host, serverSelectionTimeoutMS=1000).server_info()
        return True
    except pymongo.errors.ServerSelectionTimeoutError:
        return False

## The function to execute a command in a subprocess
#  @param cmd The command to be executed
#  @return None if in debug mode, the subprocess instance otherwise
def execute_cmd(cmd):
    if FLAGS.debug == True:
        log.info('Execute ' + ' '.join(cmd))
        return None
    else:
        log.debug('Execute ' + ' '.join(cmd))
        return subprocess.Popen(cmd)
