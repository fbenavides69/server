# -*- coding: utf-8 -*-
''' Extensions

    Instantiate needed extensions, initialization is done in app factory.'''

from flask_caching import Cache
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_debugtoolbar import DebugToolbarExtension

from .config import Configuration
from .logging import JSONLogger
from .navbar import CustomBootstrapRenderer


cfg = Configuration()
cache = Cache()
log = JSONLogger()
mail = Mail()
db = SQLAlchemy()

boot = Bootstrap()
nav = Nav()
custom_renderer = CustomBootstrapRenderer()
debug_toolbar = DebugToolbarExtension()
