# -*- coding: utf-8 -*-

from flask import jsonify

from application.models import Role
from application.models import User
from .schema import role_schema
from .schema import user_schema


def roles():
    return(jsonify(role_schema.dump(Role.query.all()).data))


def users():
    return(jsonify(user_schema.dump(User.query.all()).data))
