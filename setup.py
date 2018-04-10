''' A setuptools based setup module.

    See:
        https://packaging.python.org/en/latest/distributing.html
        https://github.com/pypa/sampleproject'''

# Always prefer setuptools over distutils
from setuptools import setup
from setuptools import find_packages
# To use a consistent encoding
from codecs import open
from os import path

from application. __meta__ import *


here = path.abspath(path.dirname(__file__))

# Get long description from README.md file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    __long_description__ = f.read()

# Get requirements.txt
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    __requirements__ = f.read()

setup(
    name=__name__,
    version=__version__,
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    author=__author__,
    author_email=__email__,
    description=__description__,
    long_description=__long_description__,
    url=__url__,
    license=__license__,
    keywords='Flask, React, Flask-Security, Yarn, Webpack',
    classifiers=[
        'Development Status :: 1 - Pre-Alpha',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU License',
        'Operating System :: POSIX',
        'Operating System :: Linux :: Ubuntu',
        'Operating System :: Windows 10 Linux Subsystem :: Ubuntu',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
    zip_safe=False,
    include_package_data=False,
    install_requires=__requirements__,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite="tests",
    entry_points='''
        [flask.commands]
            'install=application.commands:install''',
)
