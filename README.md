# server
Flask + React

## Description
Simple Flask React web application built with Flask-Bootstrap, Webpack and
Yarn. Based on the work given by Angela Branaes:
[Building a Python ReactJS web application](https://www.youtube.com/watch?v=nfi0hX-F8Zo "Youtube: Angela Branaes")

## Setup
PyEnv was used to select the proper Python version to be used along with
VirtualEnv. The React part was integrated using NodeEnv.

## Prerrequisites
Make sure to install and have a working Git and PyEnv environment and then
with the help of PyEnv install Python versions 2.7.14 and 3.6.3, accordingly.

## Installation
Please follow the next recommended sequence of general instructions to install
this application:

    git clone
    cd server
    pyenv virtualenv 2.7.14 server27 | pyenv virtualenv 3.6.3 server36
    pyenv activate server27 | pyenv activate server36
    pip install -r requirements.txt

### Update .bashrc (Ubuntu)
Nodeenv has been installed via 'pip install -r requirements.txt', now we make
sure the following is present at the end in the bash setup (.bashrc file):

    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"

To continue, refresh/rehash the shell.

### Install yarn
We proceed to install the yarn node package manager, and also make sure the
proper settings have been applied to the end of the bash setup (.bashrc file):

    curl -o- -L https://yarnpkg.com/install.sh | bash

    export PATH="$HOME/.yarn/bin:$HOME/.config/yarn/global/node_modules/.bin:$PATH"

To continue, refresh/rehash the shell.

### Install Node packages via yarn
Proceed to install all needed React dependencies:

    cd application/templates/static
    yarn install
    yarn build
    cd ../../..

## Run server
To run the server, make sure you have the instance folder with the config.py
file settings needed, before you start the sever:

    mkdir instance
    cd instance
    touch config.py

With your favorite editor add the following settings accordingly:

    CONFIG = 'INSTANCE'
    SECRET_KEY = 'some-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/server.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'some-password-salt'

    SUPER_ROLE = 'super'
    SUPER_ROLE_DESCRIPTION = 'Super User'
    SUPER_PASSWORD = 'superuser'
    SUPER_EMAIL = 'super@localhost.com'
    ADMIN_ROLE = 'admin'
    ADMIN_ROLE_DESCRIPTION = 'Administrador'
    ADMIN_PASSWORD = 'adminuser'
    ADMIN_EMAIL = 'admin@localhost.com'

    SECURITY_EMAIL_SENDER = 'no-reply@localhost'
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = some-user
    MAIL_PASSWORD = some-password

Then start the server:

    ./start

## React autobuild
While developing React components, you can use the auto build feature by:

    cd application/templates/static
    yarn watch

## Logging
The built in logging feature using JSON can be monitered as well:

    tail -f /tmp/server_development_json.log

## NOTES
The SQLite file location is setup via the instance configuration settings.
The logging file location is setup via the different config files for:
    - development
    - stagging
    - production
