# -*- coding: utf-8 -*-
''' URL's

    Define the different routes'''

from flask import Blueprint

from .views import sitemap
from .views import static_from_root
from .views import favicon
from .views import index
from .views import inside


mod = Blueprint('main', __name__)

mod.add_url_rule('/sitemap.xml', view_func=sitemap)
mod.add_url_rule('/robots.txt', view_func=static_from_root)
mod.add_url_rule('/favicon.ico', view_func=favicon)
mod.add_url_rule('/', view_func=index)
mod.add_url_rule('/inside', view_func=inside)
