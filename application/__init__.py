# -*- coding: utf-8 -*-

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

    boot.init_app(app)
    nav.init_app(app)
    custom_renderer.init_app(app)

    debug_toolbar.init_app(app)

    global user_datastore
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    global security
    security = Security(app, user_datastore)

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
    ''' Flask factory pattern'''

    # Initialize app
    app = Flask(
        __name__,
        template_folder='./templates',
        static_folder='./templates/static',
        instance_relative_config=True)
    app.url_map.strict_slashes = False

    register_navbar()
    register_extensions(app)
    register_error_handlers(app)
    register_shell_context(app)
    register_commands(app)

    # Executes before the first request is processed
    @app.before_first_request
    def before_first_request():

        # Create any database tables that don't exist yet.
        db.create_all()

        # Create the Roles "admin" and "super-user"
        # -- unless they already exist

        user_datastore.find_or_create_role(
            name=app.config['SUPER_ROLE'],
            description=app.config['SUPER_ROLE_DESCRIPTION'])
        log.logger.info('Role [{}|{}] created'.format(
            app.config['SUPER_ROLE'], app.config['SUPER_ROLE_DESCRIPTION']))

        user_datastore.find_or_create_role(
            name=app.config['ADMIN_ROLE'],
            description=app.config['ADMIN_ROLE_DESCRIPTION'])
        log.logger.info('Role [{}|{}] created'.format(
            app.config['ADMIN_ROLE'], app.config['ADMIN_ROLE_DESCRIPTION']))

        # Create two Users for testing purposes -- unless they already exists.
        # In each case, use Flask-Security utility function to encrypt the
        # password.

        encrypted_password = utils.encrypt_password(
            app.config['SUPER_PASSWORD'])
        if not user_datastore.get_user(app.config['SUPER_EMAIL']):
            user_datastore.create_user(
                email=app.config['SUPER_EMAIL'], password=encrypted_password)
            log.logger.info('User created: {}/{} {}'.format(
                app.config['SUPER_EMAIL'],
                app.config['SUPER_PASSWORD'],
                encrypted_password))

        encrypted_password = utils.encrypt_password(
            app.config['ADMIN_PASSWORD'])
        if not user_datastore.get_user(app.config['ADMIN_EMAIL']):
            user_datastore.create_user(
                email=app.config['ADMIN_EMAIL'], password=encrypted_password)
            log.logger.info('User created: {}/{} {}'.format(
                app.config['ADMIN_EMAIL'],
                app.config['ADMIN_PASSWORD'],
                encrypted_password))

        # Commit any database changes; the User and Roles must exist before
        # we can add a Role to the User
        db.session.commit()

        # "admin" role. (This will have no effect if the Users already have
        # these Roles.) Again, commit any database changes.

        user_datastore.add_role_to_user(
            app.config['SUPER_EMAIL'], app.config['SUPER_ROLE'])
        log.logger.info('User {} has role {}'.format(
            app.config['SUPER_EMAIL'], app.config['SUPER_ROLE']))

        user_datastore.add_role_to_user(
            app.config['ADMIN_EMAIL'], app.config['ADMIN_ROLE'])
        log.logger.info('User {} has role {}'.format(
            app.config['ADMIN_EMAIL'], app.config['ADMIN_ROLE']))

        # Commit the Admin User and Role
        db.session.commit()

    log.logger.info('{} application started'.format(__name__))

    return app
