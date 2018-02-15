from src.modules import Module
from src import Pipeline

conf_pipeline = {
        'name': 'test_pipeline',
        'modules': [
            {
                'name': 'module 1',
                'type': 'SampleModule',
                'input_files': ['data.json'],
                'params': [
                    {
                        'name': 'p',
                        'start': 0,
                        'end': 50,
                        'step size': 10
                    }
                ],
                'output_modules': ['module 2']
            },
            {
                'name': 'module 2',
                'type': 'SampleModule',
                'input_modules': ['module 1'],
                'params': [
                    {
                        'name': 'p',
                        'start': 1,
                        'end': 51,
                        'step size': 10
                    }
                ],
                'output_files': ['test.txt']
            }
        ]
    }

conf_module = {
            'name': 'module 1',
            'type': 'SampleModule',
            'input_files': ['data.json'],
            'params': [
                {
                    'name': 'p',
                    'start': 0,
                    'end': 50,
                    'step size': 10
                }
            ],
            'output_modules': ['module 2']
        }
 
def test_init():
    m = Module(conf_module)
