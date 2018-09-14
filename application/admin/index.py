# -*- coding: utf-8 -*-
''' Flask Admin

    Define the administration views'''

from flask import abort
from flask import request
from flask import url_for
from flask import redirect
from flask import current_app
from flask_security import current_user
from flask_admin import AdminIndexView
from flask_admin import Admin


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


admin = Admin(
    name='Admin',
    index_view=MyAdminIndexView(),
    template_mode='bootstrap3',
    base_template='admin/new_base.html')
