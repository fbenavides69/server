# -*- coding: utf-8 -*-

import datetime

from flask_security import RoleMixin
from flask_security import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base

from .extensions import db

Base = declarative_base()

roles_users = db.Table(
    'roles_users',
    db.Column(
        'role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column(
        'user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role> {} {} {}'.format(self.id, self.name, self.description)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    # SECURITY_CONFIRMABLE
    confirmed_at = db.Column(db.DateTime())
    # SECURITY_TRACKABLE
    last_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_at = db.Column(db.DateTime())
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer())
    # Custom
    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False)
    username = db.Column(db.String(255), nullable=True)

    roles = relationship(
        'Role',
        secondary=roles_users,
        backref=backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User> {} {} {} {}'.format(
            self.id,
            self.username,
            self.email,
            'Active' if self.active else 'Non Active')

    meta = {
        'allow_inheritance': True,
        'indexes': ['created_at', 'email', 'username'],
        'ordering': ['-created_at']
    }


class RolesUsers():

    def __repr__(self):
        return '<RolesUsers> {} {}'.format(self.role_id, self.user_id)


db.mapper(RolesUsers, roles_users)
