"""
BOOM: An easy-to-use question answering pipeline framework.
"""

__all__ = ['modules', 'Pipeline', 'Parameter', 'Job', 'set_logger']

from .pipeline import Pipeline
from .parameter import Parameter
from .job import Job
from .log import set_logger
#from .log import get_logger
