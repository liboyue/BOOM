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

### BOOM Basics
There are two main components to your BOOM pipeline: the modules and the configuration file. Each pipeline can have an arbitrary number of modules (n >= 1) but there is only one configuration file that defines the pipeline. BOOM works by instantiating each module and passing data along from one module to the next, allowing each to process and transform the data along the way.

#### Modules
The building block of a BOOM pipeline is the [Module class](https://bioasq.boyue.li/classsrc_1_1modules_1_1module_1_1_module.html). Each module in the pipeline takes in the data in the exact format returned by the previous module and return the data for the next module in its `process()` method. At a minimum, each user-defined module must subclass `Module` and implement the `__init__()` and `process()` methods.

#### Configuration Files
The configuration file defines the structure and composition of the pipeline and allows the user to define a parameter space for the pipeline to be executed over. The configuration is written is a YAML file and contains two core components: `pipeline`, where pipeline metadata is declared, and `modules`, where the pipeline composition is defined.

![YAML Pipeline Declaration](/images/toy_yaml_pipeline.png)

Under the `pipeline` key, there are 5 key-value pairs that need to be declared:

    name: bioasq_pipeline
    rabbitmq_host: 127.0.0.1
    clean_up: false
    use_mongodb: false
    mongodb_host: 127.0.0.1

`name` allows the user to declare a name for the pipeline. `rabbitmq_host` and `mongodb_host` are simply the host addresses for RabbitMQ and MongoDB, respectively. `clean_up` is a boolean value that will delete intermediate output files if declared `true`. `use_mongodb` is a boolean value that will write data to MongoDB instead of files if declared `true`.

- TODO: explain modules section

### Toy Example: Configuring a pipeline for simple data processing in BOOM
This toy example will show you all that is necessary to get started in BOOM. You can explore all the code associated with this example under `/example/toy`.

The first step is to create a module for your pipeline to use.

![Toy extra_modules.py](/images/toy_extra_modules.png)

In this toy example, we define a class `Sample` that is a subclass of `Module`. The `__init__()` method in this case simply passes all the parameters up to the parent class, but a more complicated module may also have additionally initialization requirements that would be met here.

The only other requirement of our module is that it implement the process function which `return`s data for the next module to use. The pipeline for this module will consist of several `Sample` modules chained together, so this module will output data in the same format it reads it in.

The data are made available to the module as an argument to the `process()` method. The parameters are available as a dictionary attribute of the job argument. The key is user-defined in the configuration file. This example will process each line in the dataset and append the phrase: "processed by [module name], params [parameter]".

In order to make use of this module, a pipeline needs to be defined in a configuration file. The configuration file for this example is shown here. The modules section declares a list of three `Sample` modules, that we have already written. The first module gets its data from the `data.json` file and the rest get their input from the preceding modules. The first `Sample` module has two parameters, one a collection and one an integer. The second module has one floating point parameter, and the third module has no parameters at all. The final module is a standard CSVWriter module that will write the final output in CSV format, it does not take parameters.

![Toy extra_modules.py](/images/toy_extra_modules.png)

To run this example start in the top level directory and run `./start_services`. Then navigate to `/example/toy/` and run `boom`. When you are finished, navigate back to the top level directory and run `./stop_services`.

### BioASQ Example: Exploring a Configuration Space and Adapting pre-existing modules
This example will show you how to configure your pipeline to explore a parameter space and take advantage of modules you already have on hand. You can explore all the code associated with this example under `/example/BioASQ`.

The BioASQ example was adapted from a pre-existing codebase. If your system is already modularized it is extremely easy to implement it as a BOOM pipeline as shown by this example module:

(IMAGE OF ANY BioASQ MODULE HERE)

Just make sure the parameters are taken as function arguments to the function called to do the processing and BOOM will handle generating the parameter combinations necessary for exploring the parameter space.

Because most of the processing occurs in the `Ranker` module, we have additional code to parallelize the processing. This requires us to override the `cleanup()` function of the `Module` class so the process pool gets closed.

(IMAGE OF RANKER CODE HERE)

The configuration file for this pipeline is similar to the one in toy module. In this case, each module is an instantiation of a different user-defined module type. Additionally, we create extra instances of the modules to take advantage of parallel processing. Each module has its own parameters associated with it and we can easily define the parameter space we want to execute over.

(IMAGE OF CONFIG FILE HERE)

To run this example start in the top level directory and run `./start_services`. Then navigate to `/example/BioASQ/` and run `boom`. When you are finished, navigate back to the top level directory and run `./stop_services`.

## Warning
This framework is still under heavy development,
please be careful.

## API documentation
You can find the API documentation [here](https://bioasq.boyue.li).
