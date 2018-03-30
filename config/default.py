# -*- coding: utf-8 -*-

import logging


CONFIG = 'DEFAULT'
DEBUG = False

# Logging
LOG_TIMEZONE_GMT = True
# LOG_TYPE
#   Valid values:
#       'single'   : one single log file only
#       'rotating' : ten file rotation with 100k max bytes each
LOG_TYPE = 'single'
LOG_FILE = '/tmp/server'
LOG_LEVEL = logging.INFO

# Flask-Security
SQLALCHEMY_ECHO = False
BCRYPT_LOG_ROUNDS = 12
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = True
SECURITY_LOGIN_WITHOUT_CONFIRMATION = False
SECURITY_POST_LOGIN_VIEW = '/inside'
SECURITY_POST_LOGOUT_VIEW = '/'
SECURITY_POST_REGISTER_VIEW = '/inside'

# Tool bar
DEBUG_TB_INTERCEPT_REDIRECTS = False
