"""
Core code of the pipeline framework.
"""

__all__ = ['modules', 'Pipeline', 'Parameter', 'Job']

from .pipeline import Pipeline
from .parameter import Parameter
from .job import Job
