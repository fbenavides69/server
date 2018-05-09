# -*- coding: utf-8 -*-
''' Marshmallow API'''

from flask import Blueprint

from .views import roles
from .views import users


mod = Blueprint('marshmallow', __name__)


mod.add_url_rule('/api/roles/', view_func=roles)
mod.add_url_rule('/api/users/', view_func=users)
