# -*- coding: utf-8 -*-

import sys
import time
import pytz
import inspect
import datetime
import structlog
import threading
import collections
import logging.config


LOGGED_TZ = pytz.timezone('Zulu')


class StructLogger(object):

    def __init__(self, app=None):
        self.log = None
        if app is not None:
            self.init_app(app)

    def _add_caller_info(self, logger, method_name, event_dict):
        # pylint: disable=unused-argument
        # Typically skipped funcs: _add_caller_info, _process_event,
        # _proxy_to_logger, _proxy_to_logger
        frame = inspect.currentframe()
        while frame:
            frame = frame.f_back
            module = frame.f_globals['__name__']
            if module.startswith('structlog.'):
                continue
            event_dict['_module'] = module
            event_dict['_lineno'] = frame.f_lineno
            event_dict['_func'] = frame.f_code.co_name
            return event_dict

    def _add_log_level(self, logger, method_name, event_dict):
        # pylint: disable=unused-argument
        event_dict['_level'] = method_name
        event_dict['_levelno'] = getattr(logging, method_name.upper())
        return event_dict

    def _add_thread_info(self, logger, method_name, event_dict):
        # pylint: disable=unused-argument
        thread = threading.current_thread()
        event_dict['_thread_id'] = thread.ident
        event_dict['_thread_name'] = thread.name
        return event_dict

    def _event_uppercase(self, logger, method_name, event_dict):
        # pylint: disable=unused-argument
        event_dict['event'] = event_dict['event'].upper()
        return event_dict

    def _add_timestamp(self, logger, method_name, event_dict):
        # pylint: disable=unused-argument
        event_dict['_time_unix'] = time.time()
        dt_utc = datetime.datetime.fromtimestamp(
            event_dict['_time_unix'], datetime.timezone.utc)
        event_dict['_time_human_utc'] = dt_utc.isoformat()
        event_dict['_time_human_localized'] = {
            LOGGED_TZ.zone: dt_utc.astimezone(LOGGED_TZ).isoformat()}
        return event_dict

    def _order_keys(self, logger, method_name, event_dict):
        # pylint: disable=unused-argument
        return collections.OrderedDict(
            sorted(
                event_dict.items(),
                key=lambda item: (item[0] != 'event', item)))

    def _censor_password(self, _, __, event_dict):
        pw = event_dict.get('password')
        if pw:
            event_dict['password'] = '*CENSORED*'
        return event_dict

    def init_app(self, app):
        self.app = app

        structlog.configure_once(
            processors=[
                structlog.stdlib.filter_by_level,
                self._add_caller_info,
                self._add_log_level,
                self._add_thread_info,
                self._event_uppercase,
                structlog.stdlib.PositionalArgumentsFormatter(True),
                self._add_timestamp,
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeEncoder()
                if sys.version_info.major == 2
                else structlog.processors.UnicodeDecoder(),
                self._order_keys,
                self._censor_password,
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.stdlib.BoundLogger,
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'json': {
                    'format': '%(message)s %(lineno)d %(pathname)s',
                    'class': 'pythonjsonlogger.jsonlogger.JsonFormatter'
                }
            },
            'handlers': {
                'file': {
                    '()': logging.handlers.TimedRotatingFileHandler,
                    'filename': app.config['LOG_FILE'],
                    'when': 'midnight',
                    'backupCount': 14,
                    'utc': True,
                },
                'json': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'json'
                }
            },
            'loggers': {
                '': {
                    'handlers': ['file'],
                    'level': app.config['LOG_LEVEL']}}})

        self.log = structlog.wrap_logger(logging.getLogger(__name__))
        self.log.info('Logging Initialized ')


log = StructLogger()
