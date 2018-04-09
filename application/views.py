# -*- coding: utf-8 -*-
''' Views

    Define the routing views'''

from flask import redirect
from flask import render_template
from flask_security import login_required


def favicon():
    return redirect('http://cdn.sstatic.net/superuser/img/favicon.ico')


def index():
    return render_template('index.html')


@login_required
def inside():
    return render_template('inside.html')
