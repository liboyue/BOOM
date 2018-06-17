# Toy Example
## Configuring a pipeline for simple data processing in BOOM

This toy example will show you all that is necessary to get started in BOOM. You can explore all the code associated with this example under `/example/toy`.

The first step is to create a module for your pipeline to use.

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

In this toy example, we define a class `Sample` that is a subclass of `Module`. The `__init__()` method in this case simply passes all the parameters up to the parent class, but a more complicated module may also have additionally initialization requirements that would be met here.

The only other requirement of our module is that it implement the process function which `return`s data for the next module to use. The pipeline for this module will consist of several `Sample` modules chained together, so this module will output data in the same format it reads it in.

The data are made available to the module as an argument to the `process()` method. The parameters are available as a dictionary attribute of the job argument. The key is user-defined in the configuration file. This example will process each line in the dataset and append the phrase: "processed by [module name], params [parameter]".

In order to make use of this module, a pipeline needs to be defined in a configuration file. The configuration file for this example is shown here. The modules section declares a list of three `Sample` modules, that we have already written. The first module gets its data from the `data.json` file and the rest get their input from the preceding modules. The first `Sample` module has two parameters, one a collection and one an integer. The second module has one floating point parameter, and the third module has no parameters at all. The final module is a standard CSVWriter module that will write the final output in CSV format, it does not take parameters.

```
pipeline:
    name: toy_pipeline
    rabbitmq_host: 127.0.0.1
    clean_up: false
    use_mongodb: false
    mongodb_host: 127.0.0.1

modules:
    -   name: module_1
        type: Sample
        input_file: data.json
        output_module: module_2
        instances: 1
        params:
            -   name: p1
                type: collection
                values:
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
```

To run this example start in the top level directory and run `./start_services`.
Then navigate to `example/toy` and run `boom`.
When you are finished, navigate back to the top level directory and run `./stop_services`.
