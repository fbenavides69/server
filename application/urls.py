# -*- coding: utf-8 -*-
''' URL's

    Define the different routes'''

from flask import Blueprint

from .views import favicon
from .views import index
from .views import inside


mod = Blueprint('main', __name__)

mod.add_url_rule('/favicon.ico', view_func=favicon)
mod.add_url_rule('/', view_func=index)
mod.add_url_rule('/inside', view_func=inside)
