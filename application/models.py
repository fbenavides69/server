# -*- coding: utf-8 -*-

from flask_security import utils
from flask_security import RoleMixin
from flask_security import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from .extensions import db


roles_users = db.Table(
    ''' Joint table'''
    'roles_users',
    db.Column(
        'role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column(
        'user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))


class PrimaryKeyMixin(db.Model):
    ''' Base clase for common properties'''
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
        nullable=False)


class Role(PrimaryKeyMixin, RoleMixin):
    ''' Role based authentication - Flask-Security'''
    __tablename__ = 'role'

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role> {} [{}|{}]'.format(self.id, self.name, self.description)

    def __str__(self):
        return self.name


class User(PrimaryKeyMixin, UserMixin):
    ''' User based authentication - Flask-Security'''
    __tablename__ = 'user'

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

    def __init__(self, email, password=None, **kwargs):
        ''' Create instance'''
        super(User, self).__init__(email=email, password=password, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def __repr__(self):
        ''' CLI human undestanable format'''
        return '<User> {} {} [{}|{}]'.format(
            self.id,
            'Active' if self.active else 'Non Active',
            self.username,
            self.email)

    def set_password(self, password):
        ''' Set password with Flask-Security encryption'''
        self.password = utils.encrypt_password(password)

    def check_password(self, password):
        ''' Check/Verify the supplied password against the stored password'''
        return self.password == utils.encrypt_password(password)

    meta = {
        'allow_inheritance': True,
        'indexes': ['created_at', 'email', 'username'],
        'ordering': ['-created_at']
    }


class RolesUsers():

    def __repr__(self):
        ''' CLI human understandable format'''
        return '<RolesUsers> {} {}'.format(self.role_id, self.user_id)


db.mapper(RolesUsers, roles_users)
