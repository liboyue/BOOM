# Toy Example
## Configuring a pipeline for simple data processing in BOOM

This toy example will show you all that is necessary to get started in BOOM. You can explore all the code associated with this example under `/example/toy`.

The first step is to create a module for your pipeline to use.

![Toy extra_modules.py](/images/toy_extra_modules.png)

In this toy example, we define a class `Sample` that is a subclass of `Module`. The `__init__()` method in this case simply passes all the parameters up to the parent class, but a more complicated module may also have additionally initialization requirements that would be met here.

The only other requirement of our module is that it implement the process function which `return`s data for the next module to use. The pipeline for this module will consist of several `Sample` modules chained together, so this module will output data in the same format it reads it in.

The data are made available to the module as an argument to the `process()` method. The parameters are available as a dictionary attribute of the job argument. The key is user-defined in the configuration file. This example will process each line in the dataset and append the phrase: "processed by [module name], params [parameter]".

In order to make use of this module, a pipeline needs to be defined in a configuration file. The configuration file for this example is shown here. The modules section declares a list of three `Sample` modules, that we have already written. The first module gets its data from the `data.json` file and the rest get their input from the preceding modules. The first `Sample` module has two parameters, one a collection and one an integer. The second module has one floating point parameter, and the third module has no parameters at all. The final module is a standard CSVWriter module that will write the final output in CSV format, it does not take parameters.

![Toy conf.yaml](/images/toy_conf.png)

To run this example start in the top level directory and run `./start_services`. Then navigate to `/example/toy/` and run `boom`. When you are finished, navigate back to the top level directory and run `./stop_services`.
