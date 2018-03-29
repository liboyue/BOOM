#!/bin/bash
mkdir -p data
rabbitmq-server &
mongod --dbpath ./data &
