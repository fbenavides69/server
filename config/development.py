# -*- coding: utf-8 -*-

import logging


CONFIG = 'DEVELOPMENT'
DEBUG = True

# Logging
LOG_FILE = '/tmp/server_development.log'
LOG_LEVEL = logging.DEBUG

# Flask-Security
SQLALCHEMY_ECHO = True
SECURITY_SEND_REGISTER_EMAIL = False
