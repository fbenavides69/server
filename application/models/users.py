# -*- coding: utf-8 -*-

from flask_security import utils
from flask_security import UserMixin
from flask_security import SQLAlchemyUserDatastore

from .primary import db
from .primary import PrimaryKeyMixin
from .roles_users import roles_users
from .roles import Role


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

    roles = db.relationship(
        'Role', secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'))

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

    def verify_password(self, password):
        ''' Check/Verify the supplied password against the stored password'''
        return self.password == utils.encrypt_password(password)

    meta = {
        'allow_inheritance': True,
        'indexes': ['created_at', 'email', 'username'],
        'ordering': ['-created_at']
    }


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
