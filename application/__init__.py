# -*- coding: utf-8 -*-
''' Flask Application Factory

    Blueprint Flask application using the factory pattern,
    with configuration setup and blueprint module registration'''

from flask import Flask
from flask import render_template
from flask_nav.elements import *
from flask_security import utils
from flask_security import Security
from flask_security import SQLAlchemyUserDatastore

from .extensions import cfg
from .extensions import cache
from .extensions import log
from .extensions import mail
from .extensions import db
from .extensions import boot
from .extensions import nav
from .extensions import custom_renderer
from .extensions import debug_toolbar
from .navbar import ExtendedNavbar

from .models import User
from .models import Role
from .admin import admin

from .commands import *
from .urls import mod as urls


def register_navbar():
    ''' Initialize navbar elements'''

    # registers the "index" (public) menubar
    nav.register_element(
        'index',
        ExtendedNavbar(
            title=View('Welcome', 'main.index'),
            root_class='navbar navbar-inverse',
            right_items=(
                View('Admin', 'admin.index'),
                View('Register', 'security.register'),
                View('Login', 'security.login'),)))

    # registers the "inside" (private) menubar
    nav.register_element(
        'inside',
        ExtendedNavbar(
            title=View('Welcome', 'main.index'),
            root_class='navbar navbar-inverse',
            right_items=(
                View('Logout', 'security.logout'),
            ),))


def register_extensions(app):
    ''' Initialize given extensions'''

    cfg.init_app(app)
    cache.init_app(app)
    log.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    admin.init_app(app)

    boot.init_app(app)
    nav.init_app(app)
    custom_renderer.init_app(app)

    debug_toolbar.init_app(app)

    global user_datastore
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    global security
    security = Security(app, user_datastore)


def register_blueprints(app):
    ''' Register Blueprint extensions'''

    app.register_blueprint(urls)


def register_error_handlers(app):
    ''' Handle errors'''

    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)

    return None


def register_shell_context(app):
    ''' Register shell context objects'''

    def shell_context():
        '''Shell context objects'''
        return {
            'db': db,
            'User': User,
            'Role': Role}

    app.shell_context_processor(shell_context)


def register_commands(app):
    ''' Register Click Commands'''

    app.cli.add_command(install)
    app.cli.add_command(user)
    app.cli.add_command(role)
    app.cli.add_command(passwd)
    app.cli.add_command(clean)


def create_app():
    ''' create_app

        input:
            None

        output:
            app -- flask web application instance

        Read configuration values in the following order:
            1) default, values which can be overwritten later
            2) intance, for your eyes only not stored in repo values
            3) environment, selectable values from:
                - development
                - stagging
                - production

        Setup web interface with Bootstrap framework'''

    # Initialize app
    app = Flask(
        __name__,
        template_folder='./templates',
        static_folder='./templates/static',
        instance_relative_config=True)
    app.url_map.strict_slashes = False

    register_navbar()
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_shell_context(app)
    register_commands(app)

    # Executes before the first request is processed
    @app.before_first_request
    def create_users():

        # Create any database tables that don't exist yet.
        db.create_all()

        # Create the Roles "admin" and "super-user"
        # -- unless they already exist

        if not user_datastore.find_role(app.config['SUPER_ROLE']):
            if user_datastore.create_role(
                    name=app.config['SUPER_ROLE'],
                    description=app.config['SUPER_ROLE_DESCRIPTION']):
                app.logger.info('Role [{}|{}] created'.format(
                    app.config['SUPER_ROLE'],
                    app.config['SUPER_ROLE_DESCRIPTION']))

        if not user_datastore.find_role(app.config['ADMIN_ROLE']):
            if user_datastore.create_role(
                    name=app.config['ADMIN_ROLE'],
                    description=app.config['ADMIN_ROLE_DESCRIPTION']):
                app.logger.info('Role [{}|{}] created'.format(
                    app.config['ADMIN_ROLE'],
                    app.config['ADMIN_ROLE_DESCRIPTION']))

        # Create two Users for testing purposes -- unless they already exists.
        # In each case, use Flask-Security utility function to encrypt the
        # password.

        if not user_datastore.get_user(app.config['SUPER_EMAIL']):
            encrypted_password = utils.encrypt_password(
                app.config['SUPER_PASSWORD'])
            if user_datastore.create_user(
                    email=app.config['SUPER_EMAIL'],
                    password=encrypted_password):
                app.logger.info('User created: {}/{} {}'.format(
                    app.config['SUPER_EMAIL'],
                    app.config['SUPER_PASSWORD'],
                    encrypted_password))

        if not user_datastore.get_user(app.config['ADMIN_EMAIL']):
            encrypted_password = utils.encrypt_password(
                app.config['ADMIN_PASSWORD'])
            if user_datastore.create_user(
                    email=app.config['ADMIN_EMAIL'],
                    password=encrypted_password):
                app.logger.info('User created: {}/{} {}'.format(
                    app.config['ADMIN_EMAIL'],
                    app.config['ADMIN_PASSWORD'],
                    encrypted_password))

        # Commit any database changes;
        # the User and Roles must exist before we can add a Role to the User
        db.session.commit()

        # "admin" role. (This will have no effect if the Users already have
        # these Roles.) Again, commit any database changes.

        if user_datastore.add_role_to_user(
                app.config['SUPER_EMAIL'], app.config['SUPER_ROLE']):
            app.logger.info('User {} has role {}'.format(
                app.config['SUPER_EMAIL'], app.config['SUPER_ROLE']))

        if user_datastore.add_role_to_user(
                app.config['ADMIN_EMAIL'], app.config['ADMIN_ROLE']):
            app.logger.info('User {} has role {}'.format(
                app.config['ADMIN_EMAIL'], app.config['ADMIN_ROLE']))

        # Commit the Admin and Super users and the corresponding roles
        db.session.commit()

    app.logger.info('{} started'.format(__name__))

    return app
