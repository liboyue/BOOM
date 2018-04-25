# BOOM
An easy-to-use multi-process question answering pipeline framework.

## Features
- Easy to use: you only need to write your configuration file and modules, we will handle everything else!
- Flexible: we (will) offer common modules for QA pipelines, and it is very easy to develop your own modules.
- Parameter tuning: automatically experiment on all possible parameter combinations and saves the results.
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

## Tutorial
There are two examples for now.
One is a toy pipeline showing how to use this framework, the other is an actual pipeline for the BioASQ challenge.

### BOOM Basics
There are two main components to your BOOM pipeline: the modules and the configuration file. Each pipeline can have an arbitrary number of modules (n >= 1) but there is only one configuration file that defines the pipeline. BOOM works by instantiating each module and passing data along from one module to the next, allowing each to process and transform the data along the way.

#### Modules
The building block of a BOOM pipeline is the [Module class](https://bioasq.boyue.li/classsrc_1_1modules_1_1module_1_1_module.html). At a minimum, each user-defined module must subclass the module class and implement the `__init__()` and `process()` functions.


#### Configuration Files
The configuration file defines the structure and composition of the pipeline and allows the user to define a parameter space for the pipeline to be executed over.

### Toy Example: Configuring a pipeline for simple data processing in BOOM
This toy example will walk show you all that is necessary to get started in BOOM. You can explore all the code associated with this example under `/example/toy`.

### BioASQ Example: Exploring a Configuration Space and Adapting pre-existing modules
This example will show you how to configure your pipeline to explore a parameter space and take advantage of modules you already have on hand.

## Warning
This framework is still under heavy development,
please be careful.

## API documentation
You can find the API documentation [here](https://bioasq.boyue.li).
