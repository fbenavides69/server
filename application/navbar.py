# -*- coding: utf-8 -*-

from flask_nav import Nav
from flask_nav.elements import *

nav = Nav()

# registers the "index" (public) menubar
nav.register_element(
    'index',
    Navbar(
        View('Welcome', 'index'),
        View('Register', 'security.register'),
        View('Login', 'security.login')
    )
)

# registers the "inside" (private) menubar
nav.register_element(
    'inside',
    Navbar(
        View('Welcome', 'index'),
        View('Logout', 'security.logout')
    )
)
