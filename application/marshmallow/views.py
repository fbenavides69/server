# -*- coding: utf-8 -*-

from flask import jsonify

from .models import Role
from .models import User
from .schema import role_schema
from .schema import user_schema


def roles():
    return(jsonify(role_schema.dump(Role.all()).data))


def users():
    return(jsonify(user_schema.dump(User.all()).data))
