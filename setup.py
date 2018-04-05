"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup
from setuptools import find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='server',
    version='1.0.0',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    author='Francisco Benavides',
    author_email='francisco.benavides@gmail.com',
    description='Flask Server Application Foundation',
    long_description=long_description,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite="tests",
)
