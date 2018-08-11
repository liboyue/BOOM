# Toy Example
## Configuring a pipeline for simple data processing in BOOM

This toy example will show you all that is necessary to get started in BOOM.

The first step is to create a module for your pipeline to use.
You can find the following code in `examples/toy/extra_modules/Sample.py`.

```
import glog as log
from boom.modules import Module

class Sample(Module):

    def __init__(self, module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):
        super(Sample, self).__init__(module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs)

    def process(self, job, data):

        log.debug(job)
        result = [x + ' processed by ' + self.name + ', params ' + str(job.params) for x in data['string_list']]
        data['string_list'] = result
        log.debug(data)

        return data
```

In this example, we define a class `Sample` that extends the base `Module` class.
The `__init__()` method in this case simply passes all the parameters up to the parent class, but a more complicated module may also have additionally initialization requirements that needs to be met here.

The only other requirement of our module is that it implements the process function which returns data for the next module to use.
The pipeline for this module will consist of several `Sample` modules chained together, so this module will output data in the same format it reads it in.

The data is made available to the module as an argument to the `process()` method.
The parameters are available as attributes of the job argument, which are expanded by the ``pipeline`` class.
This example will process each line in the dataset and append the phrase: "processed by [module name], params [parameter values]".

In order to make use of this module, a pipeline needs to be defined in a configuration file.
The configuration file for this example is shown here.
The modules section declares a list of three `Sample` modules, that we have already implemented.
The first module gets its data from the `data.json` file and the rest get their input from the preceding modules.
The first module has two parameters: collection `p1` and integer `p2`.
The second module has a float parameter, and the third module has no parameters at all.
The final module is a standard CSVWriter module that will write the final output in CSV format, it does not take parameters.

```

pipeline:
    mode: docker # Running mode, local or docker
    name: toy_pipeline # Name of the pipeline
    rabbitmq_host: 127.0.0.1 # RabbitMQ's host's uri
    clean_up: false # Whether the pipeline cleans up after finished running, true or false
    use_mongodb: true # Whether to use MongoDB, true or false
    mongodb_host: 127.0.0.1 # MongoDB's host's uri

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
```

To run this example, navigate to `example/toy` and run `boom`.
