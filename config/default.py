# -*- coding: utf-8 -*-

import logging


CONFIG = 'DEFAULT'
DEBUG = False
MAIL_DEBUG = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
# DEBUG tool bar
DEBUG_TB_ENABLED = False
DEBUG_TB_INTERCEPT_REDIRECTS = False

# Logging
# LOG_TIMEZONE_GMT
#   Valid values:
#       True  - Use GMT time zone
#       False - Use local time zome
LOG_TIMEZONE_GMT = True
# LOG_TYPE
#   Valid values:
#       'single'   : one single log file only
#       'rotating' : ten file rotation with 100k max bytes each
LOG_TYPE = 'rotating'
LOG_FILE = '/tmp/server'
LOG_LEVEL = logging.INFO

# Flask-Cache
CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.

# Flask-Security
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True
SECURITY_CONFIRMABLE = False
SECURITY_TRACKABLE = True
SECURITY_POST_LOGIN_VIEW = '/inside'
SECURITY_POST_LOGOUT_VIEW = '/'
SECURITY_POST_REGISTER_VIEW = '/inside'
SECURITY_POST_CONFIRM_VIEW = '/inside'
