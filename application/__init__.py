# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension

from .logging import log
from .navbar import nav


def create_app():

    # Initialize app
    app = Flask(
        __name__,
        static_folder='./templates/static',
        template_folder='./templates',
        instance_relative_config=True)
    app.url_map.strict_slashes = False

    # Configure app
    app.config.from_object('config.default')
    app.config.from_pyfile('config.py')
    app.config.from_envvar('APP_CONFIG_FILE')

    Bootstrap(app)
    nav.init_app(app)
    log.init_app(app)

    toolbar = DebugToolbarExtension(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    log.log.info('{} application started'.format(__name__))

    return app
