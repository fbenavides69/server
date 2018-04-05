# -*- coding: utf-8 -*-

import time
from logging import getLogger
from logging import Formatter
from logging import FileHandler
from logging.handlers import RotatingFileHandler
from collections import OrderedDict
from json import dumps

LOG_DATE_FMT = '%Y-%m-%dT%H:%M:%SZ%z'
LOG_RECORD_FIELDS = [
    'asctime',
    'name',
    'process',
    'processName',
    'thread',
    'threadName',
    'pathname',
    'module',
    'filename',
    'funcName',
    'levelname',
    'lineno',
    'msg',
    'args',
    'stack_info',
    'exc_info']


class JSONFormatter(Formatter):
    """
        The JSONFormatter class outputs Python log records in JSON format.

        JSONFormatter assumes that log record metadata fields are specified
        at the formatter level as opposed to the record level. The
        specification of metadata fields at the formatter level allows for
        multiple handles to display differing levels of detail. For example,
        console log output might specify less detail to allow for quick
        problem triage while file log output generated from the same data may
        contain more detail for in-depth investigations.

        Attributes:
            record_fields : A list of strings containing the names of metadata
                            fields (see Python log record documentation for
                            details) to add to the JSON output. Metadata fields
                            will be added to the JSON record in the order
                            specified in the recordfields list.
            custom_json   : A JSONEncoder subclass to enable writing of custom
                            JSON objects."""

    def __init__(self, record_fields=[], date_fmt=None, custom_json=None):
        """
            Overrides the default constructor to accept a formatter specific
            list of metadata fields.

            Args:
                record_fields : A list of strings referring to metadata fields
                                on the record object. It can be empty.
                                The list of fields will be added to the JSON
                                record created by the formatter."""

        super(JSONFormatter, self).__init__(None, date_fmt)
        self.record_fields = record_fields
        self.date_fmt = date_fmt
        self.custom_json = custom_json
        #self.converter = time.gmtime

    def uses_time(self):
        """
            Override to look for the asctime attribute in the record's field
            attributes.

            This changes the design assumptions. Alos, the implementation
            in this object could be brittle if a new release changes the name
            or adds another time attribute.

            Returns:
                boolean : True if asctime is in self.record_fields,
                          False otherwise."""

        return 'asctime' in self.record_fields

    def _format_time(self, record):
        ''' Set time format '''

        if self.uses_time():
            record.asctime = self.formatTime(record, self.date_fmt)

    def _getjsondata(self, record):
        """
            Combines any supplied record fields with the log record.msg field
            into an object to convert to JSON.

            Args:
                record : log record to output to JSON log.

            Returns:
                An object to convert to JSON - either an ordered dict if
                record.fields is supplied or the record.msg attribute."""

        if (len(self.record_fields) > 0):
            fields = [(x, getattr(record, x)) for x in self.record_fields]
            fields.append(('msg', record.msg))

            # An OrderedDict is used to ensure that the converted data appears
            # in the same order for every record
            return OrderedDict(fields)

        else:
            return record.msg

    def format(self, record):
        """
            Override to take a log record and output a JSON formatted string.

            Args:
                   record : log record to output to JSON log.

            Returns:
                   A JSON formatted string."""

        self._format_time(record)
        json_data = self._getjsondata(record)
        return dumps(json_data, cls=self.custom_json)


class JSONLogger(object):

    def __init__(self, app=None):
        '''Initialize the object '''

        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        ''' Initialize logging

            Returns:
                A JSON stream logger.'''

        handler = None

        if app.config['LOG_TYPE'] == 'single':
            handler = FileHandler(
                ''.join([app.config['LOG_FILE'], '_json.log']))

        if app.config['LOG_TYPE'] == 'rotating':
            handler = RotatingFileHandler(
                ''.join([app.config['LOG_FILE'], '_json.log']),
                maxBytes=100000,
                backupCount=10)

        handler.setLevel(app.config['LOG_LEVEL'])
        json_formatter = JSONFormatter(LOG_RECORD_FIELDS, LOG_DATE_FMT)
        if app.config['LOG_TIMEZONE_GMT']:
            json_formatter.converter = time.gmtime
        handler.setFormatter(json_formatter)

        self.logger = getLogger(__name__)
        self.logger.setLevel(app.config['LOG_LEVEL'])
        self.logger.addHandler(handler)

        self.logger.info('Logging Initialize')


log = JSONLogger()
