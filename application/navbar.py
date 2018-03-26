#! /usr/bin/env python
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from flask_nav import Nav
from flask_nav.elements import *

nav = Nav()

# registers the "top" menubar
nav.register_element(
    'top',
    Navbar(
        View('Welcome', 'index')
    )
)
