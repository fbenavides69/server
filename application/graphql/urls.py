# -*- coding: utf-8 -*-
''' GraphQL API'''

from flask import Blueprint
from flask_graphql import GraphQLView

from .schema import schema


mod = Blueprint('graphql', __name__)


mod.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True))
