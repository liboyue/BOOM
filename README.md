# BOOM
An easy-to-use multi-process Configuration Space Exploration pipeline framework.

## Features
- Easy to use: you only need to write your configuration file and modules, we will handle everything else!
- Flexible: we offer common modules for QA pipelines, and it is very easy to develop your own modules.
- Parameter tuning: automatically run on all possible parameter combinations and saves the results.
- High efficiency: we use multiple processes to run the whole pipeline.
- Compatibility: only compatible with Python 2.

## Installation
First, install [RabbitMQ](https://www.rabbitmq.com/download.html) and `pip`.

Then, clone the repository, run

	make install

It will install dependencies using `pip`, and install this framework to your `PATH`.

## Run
We offer a command-line executable program `boom`.
When executing, it will load `conf.yaml` from the current directory.
You can also specify the configuration file to use by adding option `-conf PATH_TO_CONF_FILE`.

For more options, run `boom --help`.

## Docker image
To build the docker image, run `make docker`.

## Tutorials
Please check out the two tutorials in `examples` folder.

## Quick tutorails

### Configuation Space Exploration
A QA pipeline may be consisted with several modules, each module may have some parameters.
Each combination of parameters corresponds to a path in the parameter space.
BOOM exhaustively run the pipeline on every possible parameter combinations, saves all intermediate results and final results.

The following figure shows a pipeline which has several modules.
The execution path is a tree which every level corresponds to a module, and each node stands for a different parameter value.
The leaf nodes are metric values.
Red arrows belongs to the best parameter combination.
![alt text](https://github.com/liboyue/BOOM/blob/master/sample_pipeline.png "The pipeline configuration and actual execution path.")

### Components
There are two main components to a BOOM pipeline: the modules and the configuration file.
Each pipeline can have an arbitrary number of modules (n >= 1) but there is only one configuration file that defines the pipeline.
BOOM works by instantiating each module and passing data along from one module to the next, allowing each to process and transform the data along the way.

#### Modules
The building block of a BOOM pipeline is the [Module class](https://bioasq.boyue.li/classsrc_1_1modules_1_1module_1_1_module.html). Each module in the pipeline takes in the data in the exact format returned by the previous module and return the data for the next module in its `process()` method. At a minimum, each user-defined module must subclass `Module` and implement the `__init__()` and `process()` methods.

#### Configuration Files
The configuration file defines the structure and composition of the pipeline and allows the user to define a parameter space for the pipeline to be executed over. The configuration is written is a YAML file and contains two core components: `pipeline`, where pipeline metadata is declared, and `modules`, where the pipeline composition is defined.

Following is the `pipeline` section of the toy example's configuration file:

    pipeline:
        name: toy_pipeline
        rabbitmq_host: 127.0.0.1
        clean_up: false
        use_mongodb: false
        mongodb_host: 127.0.0.1

Under the `pipeline` key, there are 5 key-value pairs that need to be declared:

    name
    rabbitmq_host
    clean_up
    use_mongodb
    mongodb_host

`name` allows the user to declare a name for the pipeline. `rabbitmq_host` and `mongodb_host` are simply the host addresses for RabbitMQ and MongoDB, respectively. `clean_up` is a boolean value that will delete intermediate output files if declared `true`. `use_mongodb` is a boolean value that will write data to MongoDB instead of files if declared `true`.

Following is the `modules` section of the toy example's configuration file:


    pipeline: # Pipeline section, defines pipeline's properties
        mode: docker # Running mode, local or docker, default local
        name: toy_pipeline # Name of the pipeline
        rabbitmq_host: 127.0.0.1 # RabbitMQ's host uri
        clean_up: false # Whether the pipeline cleans up after finished running, true or false
        use_mongodb: true # Whether to use MongoDB, true or false, default false
        mongodb_host: 127.0.0.1 # MongoDB's host

    modules:
        -   name: module_1 # Name of the module
            type: Sample # Type of the module
            input_file: data.json # Input file's uri
            output_module: module_2 # The following module's name
            instances: 1 # Number of instances of this module
            params:
                -   name: p1
                    type: collection # Type of the param, int, float or collection
                    values: # Possible vaules for collection param
                        - val1
                        - val2
                        - val3

                -   name: p2
                    type: int
                    start: 0
                    end: 20
                    step_size: 20

        -   name: module_2
            type: Sample
            output_module: module_3
            instances: 1
            params:
                -   name: p
                    type: float
                    start: 0.0
                    end: 80.0
                    step_size: 40.0
            
        -   name: module_3
            type: Sample
            output_module: module_4
            instances: 1

        -   name: module_4
            type: CSVWriter
            output_file: results.csv 
            instances: 1

The `modules` section of the configuration file should contain a list of modules. Each module consists of a set of key-value pairs which  must include `name`, `type`, `input_file` (first module only), `output_module` (or `output_file` for the last module), `instances`, and (optionally) `params`. `params` is a list of parameters, defined by a `name`, `type` (float, int, or collection). If the parameter is a float or int, the param should also contain `start`, `end`, and `step_size`. If the parameter is of type collection, then it should contain a `values` list.

## API documentation
You can find the API documentation [here](https://boom.boyue.li).

## Warning
This framework is still under heavy development,
please be careful.
