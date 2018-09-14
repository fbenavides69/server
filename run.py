#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
from application import create_app

TORNADO = '''<!DOCTYPE html>
<html>
    <head><title>Tornado WSGI</title></head>
    <body><h1>Tornado Web Server</h1></body>
</html>'''


class MainHandler(RequestHandler):
    def get(self):
        self.write(TORNADO)


tr = WSGIContainer(create_app())


tornado = Application([
    (r"/tornado", MainHandler),
    (r".*", FallbackHandler, dict(fallback=tr)),
])


if __name__ == "__main__":
    ''' Run the application'''
    tornado.listen(5000, address='0.0.0.0')
    IOLoop.instance().start()
