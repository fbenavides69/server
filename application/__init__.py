# -*- coding: utf-8 -*-

from flask import Flask
from flask import redirect
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_security import utils
from flask_security import Security
from flask_security import login_required
from flask_security import SQLAlchemyUserDatastore
from flask_mail import Mail

from flask_debugtoolbar import DebugToolbarExtension

from .config import cfg
from .logging import log
from .navbar import nav
from .navbar import custom_renderer
from .models import db
from .models import User
from .models import Role


def create_app():

    # Initialize app
    app = Flask(
        __name__,
        template_folder='./templates',
        static_folder='./templates/static',
        instance_relative_config=True)
    app.url_map.strict_slashes = False

    # Set-up the application core

    cfg.init_app(app)   # Configuration
    log.init_app(app)   # Logging
    db.init_app(app)    # Flask-Security ORM
    Mail(app)           # Flask-Security Email sending

    # Create needed connection
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    global security
    security = Security(app, user_datastore)

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

    # Setup User Interface
    Bootstrap(app)
    nav.init_app(app)
    custom_renderer.init_app(app)

    # Debug Toolbar
    global toolbar
    toolbar = DebugToolbarExtension(app)

    @app.route('/favicon.ico')
    def favicon():
        return redirect('http://cdn.sstatic.net/superuser/img/favicon.ico')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/inside')
    @login_required
    def inside():
        return render_template('inside.html')

    log.logger.info('{} application started'.format(__name__))

    return app
