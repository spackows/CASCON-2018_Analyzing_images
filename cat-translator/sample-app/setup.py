from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath( path.dirname( __file__ ) )

setup(
    name='cascon-demo-cat-translator-2',
    version='1.0.0',
    description='Python Flask app for classifying cat vocalization using a trained Visual Recognition model on IBM Cloud',
    license='Apache-2.0'
)
