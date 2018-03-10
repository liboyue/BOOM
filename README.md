# BOOM
An easy-to-use multi-process question answering pipeline framework.

## Features
- Easy to use: you only need to write your configuration file, we will handle everything else!
- Flexible: we (will) offer common modules for QA pipelines, and it is very easy to develop your own module.
- Tuning parameters: automatically experiment on all possible parameter combinations and saves the results.
- High efficiency: we use multiple processes to run the whole pipeline.

## Installation
First, install [RabbitMQ](https://www.rabbitmq.com/download.html) and Python3.

Then, clone the repository, run

	make install

It will install dependencies using `pip`, and install this framework to your `PATH`.

## Run
We offer a command-line executable program `boom`.
When executing, it will load `conf.yaml` from the current directory.
You can also specify the configuration file to use by adding option `-conf PATH_TO_CONF_FILE`.

For more options, run `boom --help`.

## Examples
There are two examples for now.
One is a toy pipeline showing how to use this framework, the other is an actual pipeline for BioASQ challenge.

## Warning
This framework is still under heavy developments,
please be careful.
