# -*- coding: utf-8 -*-
''' Flask Admin

    Role administration view'''

from flask import current_app
from flask_security import current_user
from flask_admin.contrib.sqla import ModelView


# Customized Role model for SQL-Admin
class RoleAdminView(ModelView):

    # Only display relevant details on the list of Users
    column_list = ('active', 'name', 'description',)
    column_editable_list = ('active', 'name', 'description',)

    # Don't include the users related field when creating or editing a
    # Role (but see below)
    form_excluded_columns = ('created_at', 'updated_at', 'users',)

    # Automatically display human-readable names for the current and available
    # Users when creating or editing a User
    column_auto_select_related = True

    # Prevent administration of Roles unless the currently logged-in user has
    # the "admin" role
    def is_accessible(self):
        return current_user.has_role(current_app.config['ADMIN_ROLE'])
