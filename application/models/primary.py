# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


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
