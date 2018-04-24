# -*- coding: utf-8 -*-

from flask_security import RoleMixin

from .primary import db
from .primary import PrimaryKeyMixin


class Role(PrimaryKeyMixin, RoleMixin):
    ''' Role based authentication - Flask-Security'''
    __tablename__ = 'role'

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role> {} [{}|{}]'.format(self.id, self.name, self.description)

    def __str__(self):
        return self.name

    meta = {
        'indexes': ['created_at', 'name'],
        'ordering': ['-created_at']
    }
