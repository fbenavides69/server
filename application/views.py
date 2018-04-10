# -*- coding: utf-8 -*-
''' Views

    Define the routing views'''
from datetime import datetime
from datetime import timedelta
from flask import url_for
from flask import request
from flask import redirect
from flask import make_response
from flask import render_template
from flask import send_from_directory
from flask import current_app
from flask_security import login_required

from .models import User


def sitemap():
    ''' Generate sitemap.xml, makes a list of urls and modified date'''

    pages = []
    ten_days_ago = datetime.now() - timedelta(days=10)

    # static pages
    for rule in current_app.url_map.iter_rules():
        if 'GET' in rule.methods and len(rule.arguments) == 0:
            pages.append([rule.rule, ten_days_ago.isoformat()])

    # user model pages
    users = User.query.order_by(User.updated_at).all()
    for user in users:
        url = url_for('main.index', name=user.username)
        modified_time = user.updated_at.date().isoformat()
        pages.append([url, modified_time])

    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"

    return response


def static_from_root():
    return send_from_directory(current_app.static_folder, request.path[1:])


def favicon():
    return redirect('http://cdn.sstatic.net/superuser/img/favicon.ico')


def index():
    return render_template('index.html')


@login_required
def inside():
    return render_template('inside.html')
