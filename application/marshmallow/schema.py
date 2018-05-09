# -*- coding: utf-8 -*-
''' Marshmallow Serializer'''

from flask_marshmallow import Marshmallow


ma = Marshmallow()


class RoleSchema(ma.Schema):
    class Meta:
        fields = ('name', 'description', 'active')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('email', 'username', 'roles', 'active')


role_schema = RoleSchema(many=True)
user_schema = UserSchema(many=True)
