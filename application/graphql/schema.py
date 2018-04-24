# -*- coding: utf-8 -*-
''' Graphene Schema

    Join Graphene with the model'''

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy import SQLAlchemyConnectionField
from application.models import User as ModelUser
from application.models import Role as ModelRole

from flask import g


class User(SQLAlchemyObjectType):
    class Meta:
        model = ModelUser
        interfaces = (relay.Node, )
        exclude_fields = ['password']


class Role(SQLAlchemyObjectType):
    class Meta:
        model = ModelRole
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    viewer = graphene.Field(User, )
    all_users = SQLAlchemyConnectionField(User)
    all_roles = SQLAlchemyConnectionField(Role)

    def resolve_viewer(self, args, context, info):
        try:
            logged_in_user = g.user
        except AttributeError:
            return None
        return logged_in_user


schema = graphene.Schema(query=Query)
