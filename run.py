#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from tornado.web import FallbackHandler, RequestHandler, Application
from application import create_app


class MainHandler(RequestHandler):
    def get(self):
        self.write("This message comes from Tornado ^_^")


tr = WSGIContainer(create_app())


tornado = Application([
    (r"/tornado", MainHandler),
    (r".*", FallbackHandler, dict(fallback=tr)),
])


if __name__ == "__main__":
    ''' Run the application'''
    tornado.listen(5000, address='0.0.0.0')
    IOLoop.instance().start()
