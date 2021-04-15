from setuptools import find_packages
from setuptools import setup

setup(
    name='wtf_converter',
    version='1.0.0',
    packeges=find_packages(exclude=('tests*',))
)