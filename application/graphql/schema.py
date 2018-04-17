# -*- coding: utf-8 -*-
''' Graphene Schema

    Join Graphene with the model'''

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy import SQLAlchemyConnectionField
from application.models import User as ModelUser
from application.models import Role as ModelRole


class User(SQLAlchemyObjectType):
    class Meta:
        model = ModelUser
        interfaces = (relay.Node, )


class Role(SQLAlchemyObjectType):
    class Meta:
        model = ModelRole
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_users = SQLAlchemyConnectionField(User)
    all_roles = SQLAlchemyConnectionField(Role)


schema = graphene.Schema(query=Query)
