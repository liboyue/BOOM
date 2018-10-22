# BioASQ Example

## Additional requirements
Please install [NLTK](https://www.nltk.org/), then download its data by running `python -m nltk.downloader all`.

## Data preparation
Please register at the [BioASQ website](http://participants-area.bioasq.org/) and download the dataset for task 6b [here](http://participants-area.bioasq.org/accounts/login/?next=/Tasks/6b/trainingDataset/). You start to download a zip file named `BioASQ-training6b.zip`, after unzipping it, you will have `BioASQ-trainingDataset6b.json`.
We also offer an script `split_data.py` to split data to small chuncks for developing and debugging.

NOTE: The `train_sample.json` only shows the code could work, it is not real BioASQ data.
Please make sure to download a copy of BioASQ using the link above.


## Exploring a Configuration Space and Adapting pre-existing modules

This example will show you how to configure your pipeline to explore a parameter space and take advantage of modules you already have on hand. You can explore all the code associated with this example under `examples/BioASQ`.

The BioASQ example was adapted from a pre-existing codebase.
If your system is already modularized, it is extremely easy to implement it as a BOOM pipeline.
Just make sure the parameters are taken as function arguments to the function called to do the processing and BOOM will handle generating the parameter combinations necessary for exploring the parameter space.

Because most of the processing occurs in the `CoreMMR` module, we have additional code to parallelize the processing. This requires us to override the `cleanup()` function of the `Module` class so the process pool gets closed.

```
from multiprocessing import Pool
from bioasq.coreMMR import CoreMMR as BioASQCoreMMR

def multi_process_helper(args):
    questions, alpha = args
    ranker = BioASQCoreMMR()
    result = []
    for question in questions:
        if 'snippets' in question:
            question['snippets'] = [s['text'] for s in question['snippets']]
            result.append((ranker.getRankedList(question, alpha, 0), question['ideal_answer'][0]))
    #log.debug(result)
    return result

class CoreMMR(Module):

    def __init__(self, module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs):
        super(CoreMMR, self).__init__(module_id, name, rabbitmq_host, pipeline_conf, module_conf, **kwargs)
        self.processes = module_conf['processes'] if 'processes' in module_conf else 1
        self.pool = Pool(processes=self.processes)

    ## Override the cleanup function to make sure close the process pool.
    def cleanup(self):
        self.pool.close()
        self.pool.join()

    def process(self, job, data):

        questions = data['questions']
        N = len(questions)
        step_size = int(N / float(self.processes))
        slices = [(questions[i:i+step_size], job.params['alpha']) for i in range(0, N, step_size)]
        tmp = self.pool.map(multi_process_helper, slices)

        result = []
        for x in tmp:
            result += x

        return result
```

The configuration file for this pipeline is similar to the one in toy module. In this case, each module is an instantiation of a different user-defined module type. Additionally, we create extra instances of the modules to take advantage of parallel processing. Each module has its own parameters associated with it and we can easily define the parameter space we want to execute over.

```
pipeline:
    name: bioasq_pipeline
    rabbitmq_host: 127.0.0.1
    clean_up: false

modules:
    -   name: ranker
        type: CoreMMR
        input_file: BioASQ-trainingDataset6b.json
        output_module: orderer
        instances: 10
        processes: 4
        params:
            -   name: alpha
                type: int
                start: 50
                end: 60
                step_size: 10

    -   name: orderer
        type: Orderer
        output_module: tiler
        instances: 3
        params:
            -   name: k
                type: int
                start: 2
                end: 4
                step_size: 2

    -   name: tiler
        type: Tiler
        output_module: csv
        instances: 1
        params:
            -   name: word_limit
                type: int
                start: 50
                end: 200
                step_size: 25

    -   name: csv
        type: CSVWriter
        output_file: results.csv
        instances: 1
```
To run this example, navigate to `example/BioASQ` and run `boom`.
