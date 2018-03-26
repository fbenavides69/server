#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(
    __name__,
    static_folder='./templates/static',
    template_folder='./templates')

app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = 'secret-key'

Bootstrap(app)
toolbar = DebugToolbarExtension(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
