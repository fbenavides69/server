# -*- coding: utf-8 -*-
''' Marshmallow Serializer'''

from flask_marshmallow import Marshmallow

from application.models import Role
from application.models import User


ma = Marshmallow()


class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'active')


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'roles', 'active')


role_schema = RoleSchema(many=True)
user_schema = UserSchema(many=True)
