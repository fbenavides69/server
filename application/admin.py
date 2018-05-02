# -*- coding: utf-8 -*-
''' Flask Admin

    Define the administration views'''

from flask import abort
from flask import request
from flask import url_for
from flask import redirect
from flask import current_app
from flask_security import utils
from flask_security import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from wtforms.fields.simple import PasswordField


# Customized Role model for SQL-Admin
class RoleAdmin(ModelView):

    # Only display relevant details on the list of Users
    column_list = ('name', 'description',)
    column_editable_list = ('name', 'description',)

    # Don't include the users related field when creating or editing a
    # Role (but see below)
    form_excluded_columns = ('created_at', 'updated_at', 'users',)

    # Prevent administration of Roles unless the currently logged-in user has
    # the "admin" role
    def is_accessible(self):
        return current_user.has_role('admin')


# Customized User model for SQL-Admin
class UserAdmin(ModelView):

    # Only display relevant details on the list of Users
    # column_exclude_list = ('password',)
    column_list = ('active', 'email', 'username', 'roles',)
    column_editable_list = ('active', 'email', 'username', 'roles',)

    # Don't include the standard password field when creating or editing a
    # User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available
    # Roles when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Users unless the currently logged-in user has
    # the "admin" role
    def is_accessible(self):
        return current_user.has_role(current_app.config['ADMIN_ROLE'])

    # On the form for creating or editing a User, don't display a field
    # corresponding to the model's password field. There are two reasons for
    # this. First, we want to encrypt the password before storing in the
    # database. Second, we want to use a password field (with the input
    # masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. We've
        # already told Flask-Admin to exclude the
        # password field from this form.
        form_class = super(UserAdmin, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New
        # Password".
        form_class.password2 = PasswordField('New Password')
        return form_class

    # This callback executes when the user saves changes to a newly-created or
    # edited User -- before the changes are committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password2):

            # ... then encrypt the new password prior to storing it in the
            # database. If the password field is blank, the existing password
            # in the database will be retained.
            model.password = utils.encrypt_password(model.password2)


# Customized Flask-admin Admin area
class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role(current_app.config['ADMIN_ROLE']):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view
        is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))
