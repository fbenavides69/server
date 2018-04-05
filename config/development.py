# -*- coding: utf-8 -*-

import logging


CONFIG = 'DEVELOPMENT'
DEBUG = True
MAIL_DEBUG = True
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
# DEBUG tool bar
DEBUG_TB_ENABLED = True
DEBUG_TB_INTERCEPT_REDIRECTS = True

# Logging
LOG_TYPE = 'single'
LOG_FILE = '/tmp/server_development'
LOG_LEVEL = logging.DEBUG

# REPL
REPL_FILE = '/tmp/repl_development.txt'
