# -*- coding: utf-8 -*-
''' Flask Application Factory

    Blueprint Flask application using the factory pattern,
    with configuration setup and blueprint module registration'''

from flask import Flask
from flask import render_template
from flask_nav.elements import *
from flask_security import Security

from .extensions import cfg
from .extensions import cache
from .extensions import log
from .extensions import mail
from .extensions import admin
from .extensions import boot
from .extensions import nav
from .extensions import custom_renderer
from .extensions import debug_toolbar
from .navbar import ExtendedNavbar

from .models import db
from .models import User
from .models import Role
from .models import user_datastore
from .admin import UserAdmin
from .admin import RoleAdmin

from .commands import *
from .urls import mod as urls
from .graphql import mod as graphql_urls


def init_navbar():
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

    # registers the "inside" (private) menubar
    nav.register_element(
        'admin',
        ExtendedNavbar(
            title=View('Admin', 'admin.index'),
            root_class='navbar navbar-inverse',
            items=(
                View('Role', 'role.index_view'),
                View('User', 'user.index_view'),
            ),
            right_items=(
                View('Logout', 'security.logout'),
            ),))


def register_extensions(app):
    ''' Initialize given extensions'''

    # Core services
    cfg.init_app(app)
    cache.init_app(app)
    log.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    admin.init_app(app)

    # Look and feel
    boot.init_app(app)
    nav.init_app(app)
    custom_renderer.init_app(app)

    # Debugging
    debug_toolbar.init_app(app)


def register_blueprints(app):
    ''' Register Blueprint extensions'''

    app.register_blueprint(urls)
    app.register_blueprint(graphql_urls)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()


def register_error_handlers(app):
    ''' Register Error handler'''

    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code

    for errcode in [401, 403, 404, 500]:
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


def register_users(app):
    ''' Register Admin and Super User roles and corresponding users'''

    # Set-up user registration
    global security
    security = Security(app, user_datastore)

    # Executes before the first request is processed
    @app.before_first_request
    def create_users():

        # Create any database tables that don't exist yet.
        db.create_all()

        # Create the Roles for "Administration" and "Super User"
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

        # Create Users "admin" and "super"
        # -- unless they already exists.

        if not user_datastore.get_user(app.config['SUPER_EMAIL']):
            if user_datastore.create_user(
                    email=app.config['SUPER_EMAIL'],
                    password=app.config['SUPER_PASSWORD']):
                app.logger.info('User [{}|{}] created'.format(
                    app.config['SUPER_EMAIL'],
                    app.config['SUPER_PASSWORD']))

        if not user_datastore.get_user(app.config['ADMIN_EMAIL']):
            if user_datastore.create_user(
                    email=app.config['ADMIN_EMAIL'],
                    password=app.config['ADMIN_PASSWORD']):
                app.logger.info('User [{}|{}] created'.format(
                    app.config['ADMIN_EMAIL'],
                    app.config['ADMIN_PASSWORD']))

        # Commit any database changes;
        # the User and Roles must exist before we can add a Role to the User
        db.session.commit()

        # "admin" role. (This will have no effect if the Users that already
        # have these Roles.) Again, commit any database changes.

        if user_datastore.add_role_to_user(
                app.config['SUPER_EMAIL'], app.config['SUPER_ROLE']):
            app.logger.info('User [{}] has Role [{}]'.format(
                app.config['SUPER_EMAIL'], app.config['SUPER_ROLE']))

        if user_datastore.add_role_to_user(
                app.config['ADMIN_EMAIL'], app.config['ADMIN_ROLE']):
            app.logger.info('User [{}] has Role [{}]'.format(
                app.config['ADMIN_EMAIL'], app.config['ADMIN_ROLE']))

        # Commit the Admin and Super users and the corresponding roles
        db.session.commit()


def init_admin():
    ''' Initialize Admin elements'''

    # Add the Admin views
    admin.add_view(RoleAdmin(Role, db.session))
    admin.add_view(UserAdmin(User, db.session))


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

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_shell_context(app)
    register_commands(app)
    register_users(app)

    init_navbar()
    init_admin()

    app.logger.info('{} started'.format(__name__))

    return app
