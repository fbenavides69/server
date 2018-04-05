# -*- coding: utf-8 -*-


class Configuration(object):

    def __init__(self, app=None):
        '''Initialize the object '''

        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        ''' Initialize configuration

            Returns:
                A configuration object.'''

        # Configure app
        app.config.from_object('config.default')
        app.config.from_pyfile('config.py')
        app.config.from_envvar('APP_CONFIG_FILE')


cfg = Configuration()
