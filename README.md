# server
Flask + React

## Description
Simple Flask React web application built with Flask-Bootstrap, Webpack and
Yarn. Based on the work given by Angela Branaes:
[Building a Python ReactJS web application](https://www.youtube.com/watch?v=nfi0hX-F8Zo "Youtube: Angela Branaes")

## Setup
PyEnv was used to select the proper Python version to be used along with
VirtualEnv. The React part was integrated using Nodeenv.

## Prerrequisites
Make sure to install and have a working PyEnv and then with the help of PyEnv
install Python versions 2.7.14 and 3.6.3, accordingly.

## Installation
Please follow the next recommended sequence of general instructions to install
this application:

Git clone
cd server
pyenv virtualenv 2.7.14 server27 | pyenv virtualenv 3.6.3 server36
pyenv activate server27 | pyenv activate server36
pip install -r requirements.txt
cd templates/static
yarn install
yarn build
cd ../..
./start
