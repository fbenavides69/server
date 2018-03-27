# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_security import utils
from flask_security import Security
from flask_security import login_required
from flask_security import SQLAlchemyUserDatastore
from flask_mail import Mail

from flask_debugtoolbar import DebugToolbarExtension

from .logging import log
from .navbar import nav
from .models import db
from .models import User
from .models import Role


def create_app():

    # Initialize app
    app = Flask(
        __name__,
        static_folder='./templates/static',
        template_folder='./templates',
        instance_relative_config=True)
    app.url_map.strict_slashes = False

    # Configure app
    app.config.from_object('config.default')
    app.config.from_pyfile('config.py')
    app.config.from_envvar('APP_CONFIG_FILE')

    # Setup logging
    log.init_app(app)

    # Setup Flask-Security

    # Configure Email sending
    Mail(app)
    # Configure ORM
    db.init_app(app)

    # Create needed connection
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
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
        user_datastore.find_or_create_role(
            name=app.config['ADMIN_ROLE'],
            description=app.config['ADMIN_ROLE_DESCRIPTION'])

        # Create two Users for testing purposes -- unless they already exists.
        # In each case, use Flask-Security utility function to encrypt the
        # password.
        encrypted_password = utils.encrypt_password(
            app.config['SUPER_PASSWORD'])
        if not user_datastore.get_user(app.config['SUPER_EMAIL']):
            user_datastore.create_user(
                email=app.config['SUPER_EMAIL'], password=encrypted_password)
        encrypted_password = utils.encrypt_password(
            app.config['ADMIN_PASSWORD'])
        if not user_datastore.get_user(app.config['ADMIN_EMAIL']):
            user_datastore.create_user(
                email=app.config['ADMIN_EMAIL'], password=encrypted_password)

        # Commit any database changes; the User and Roles must exist before
        # we can add a Role to the User
        db.session.commit()

        # "admin" role. (This will have no effect if the Users already have
        # these Roles.) Again, commit any database changes.
        user_datastore.add_role_to_user(
            app.config['SUPER_EMAIL'], app.config['SUPER_ROLE'])
        user_datastore.add_role_to_user(
            app.config['ADMIN_EMAIL'], app.config['ADMIN_ROLE'])

        # Commit the Admin User and Role
        db.session.commit()

    # Setup User Interface
    Bootstrap(app)
    nav.init_app(app)

    # Debug Toolbar
    toolbar = DebugToolbarExtension(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/inside')
    @login_required
    def inside():
        return render_template('inside.html')

    log.log.info('{} application started'.format(__name__))

    return app
