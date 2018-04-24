# -*- coding: utf-8 -*-
''' JSON Web Tokens'''

from flask_jwt import JWT
from application.models import user_datastore


def authenticate(username, password):
    user = user_datastore.find_user(email=username)
    if user and username == user.email and user.verify_password(password):
        return user
    return None


def identity(payload):
    return user_datastore.find_user(id=payload['identity'])


jwt = JWT(authenticate, identity)
