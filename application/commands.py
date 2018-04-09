# -*- coding: utf-8 -*-
''' Click Commands

    install - Create a default admin user with corresponding admin role
    user    - Creates a given user, by email address
    role    - Adds a role to a given user
    passwd  - Reset a given users password
    clean   - Removes generated files'''

import os
import click

from flask import current_app
from flask.cli import with_appcontext
from flask_security import utils

from .models import User
from .models import Role


@click.command()
@with_appcontext
def install():
    ''' Install a default admin user and add an admin role to it'''

    # Check if role exists; otherwise, add role
    role = current_app.config['ADMIN_ROLE']
    if Role.objects.filter(name=role).first() is not None:
        click.echo('Role {} already exists!'.format(role))

    else:
        description = current_app.config['ADMIN_ROLE_DESCRIPTION']
        Role(name=role, description=description).save()
        click.echo('Role {} added successfully'.format(role))

    # Check if user exits; otherwise, add
    email = current_app.config['ADMIN_EMAIL']
    if User.objects(email=email).first() is not None:
        click.echo('User {} already exists!'.format(email))

    else:
        username = current_app.config['ADMIN_USER']
        password = current_app.config['ADMIN_PASSWORD']
        User(
            username=username,
            email=email,
            active=1,
            password=utils.encrypt_password(password)).save()


@click.command()
@click.option('-e', '--email', prompt=True, default=None)
@click.option('-p', '--password', prompt=True, default=None)
@with_appcontext
def user(email, password):
    ''' Creates a user using an email'''

    # Check if user exists
    if User.objects(email=email).first() is not None:
        click.echo('User {} already exists!'.format(email))

    else:
        User.run(email=email, password=password, active=1).save()
        click.echo('User {} created successfully'.format(email))


@click.command()
@click.option('-r', '--role', prompt=True, default=None)
@click.option('-d', '--description', prompt=True, default=None)
@with_appcontext
def role(role, description):
    ''' Adds a role to the given user'''

    # Check if role exists
    if Role.objects(name=role).first() is not None:
        click.echo('Role {} already exists!'.format(role))

    else:
        Role(role=role, description=description).save()
        click.echo('Role {} created successfully'.format(role))


@click.command()
@click.option('-e', '--email', prompt=True, default=None)
@click.option('-p', '--password', prompt=True, default=None)
@with_appcontext
def passwd(email, password):
    ''' Reset a given user's password'''

    # Check if user exists
    u = User.objects(email=email).first()
    if u is None:
        click.echo('User {} does not exits'.format(email))

    else:
        u.password = utils.encrypt_password(password)
        u.save()
        click.echo(
            'User {} password has been reset successfully'.format(email))


@click.command()
def clean():
    ''' Remove *.pyc and *.pyo files recursively starting at current directory.
        Borrowed from Flask-Script, converted for use with Click'''

    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                click.echo('Removing {}'.format(full_pathname))
                os.remove(full_pathname)
