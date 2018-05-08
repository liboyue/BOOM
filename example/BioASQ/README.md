# BioASQ Example
## Exploring a Configuration Space and Adapting pre-existing modules

This example will show you how to configure your pipeline to explore a parameter space and take advantage of modules you already have on hand. You can explore all the code associated with this example under `example/BioASQ`.

The BioASQ example was adapted from a pre-existing codebase. If your system is already modularized it is extremely easy to implement it as a BOOM pipeline as shown by this example module:

![BioASQ Orderer](/images/orderer.png)

Just make sure the parameters are taken as function arguments to the function called to do the processing and BOOM will handle generating the parameter combinations necessary for exploring the parameter space.

Because most of the processing occurs in the `CoreMMR` module, we have additional code to parallelize the processing. This requires us to override the `cleanup()` function of the `Module` class so the process pool gets closed.

![BioASQ CoreMMR](/images/coremmr.png)

The configuration file for this pipeline is similar to the one in toy module. In this case, each module is an instantiation of a different user-defined module type. Additionally, we create extra instances of the modules to take advantage of parallel processing. Each module has its own parameters associated with it and we can easily define the parameter space we want to execute over.

![BioASQ conf.yaml](/images/bioasq_conf.png)

To run this example start in the top level directory and run `./start_services`. Then navigate to `/example/BioASQ/` and run `boom`. When you are finished, navigate back to the top level directory and run `./stop_services`.
