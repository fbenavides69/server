#! /usr/bin/env python
# -*- coding: utf-8 -*-

from application import create_app

if __name__ == '__main__':
    ''' Run the application'''
    app = create_app()
    app.run('0.0.0.0')
