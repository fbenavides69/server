# -*- coding: utf-8 -*-

from flask_security import RoleMixin
from flask_security import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

# Initialize the SQL Alchemy object
db = SQLAlchemy()


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
        return '<Role> {}'.format(self.name)


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
    username = db.Column(db.String(255), nullable=True)

    roles = relationship(
        'Role',
        secondary=roles_users,
        backref=backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User> {} {}'.format(
            self.username, 'Active' if self.active else 'Non Active')


class RolesUsers():

    def __repr__(self):
        return '<RolesUsers> {} {}'.format(self.role_id, self.user_id)


db.mapper(RolesUsers, roles_users)
