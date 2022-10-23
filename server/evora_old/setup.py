from setuptools import find_packages
from setuptools import setup

setup(
        name='evora',
        version='1.0.0',
        description='Package contains wrapper code for the Andor SDK.',
        author='Astronomy Undergraduate Engineering Group',
        install_requires=['pybind11', 'numpy']
)
