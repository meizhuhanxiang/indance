#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver


from utils.code import *


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

    def initialize(self):
        self.code = SUCCESS
        self.reason = ''


    def on_finish(self):
        self.session.close()

    def get_need_args(self, args):
        res = {}
        for arg in args:
            try:
                param = self.get_argument(arg)
                res[arg] = param
            except:
                self.code = ARGUMENT_MISSING
                self.reason = '%s is missing' % arg
                return {}
        return res

    def write_res(self, res):
        self.write(json.dumps({'code': self.code, 'reason': self.reason, 'res': res}))
