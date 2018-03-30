# -*- coding: utf-8 -*-

CONFIG = 'DEVELOPMENT'
DEBUG = True

# Logging
LOG_FILE = '/tmp/development'
LOG_LEVEL = 'DEBUG'

# Flask-Security
SQLALCHEMY_ECHO = True
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
