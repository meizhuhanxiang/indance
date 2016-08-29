#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from utils.code import *
from utils import session
from utils.wechat import WeChat
from model.indance_handler import InDanceDB
from utils.logger import runtime_logger


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        # self.set_header('Access-Control-Allow-Origin', '*')
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        # self.set_header('Access-Control-Max-Age', 1000)
        # self.set_header('Access-Control-Allow-Headers', '*')
        # self.set_header('Content-type', 'application/json')
        pass

    def initialize(self):
        self.code = SUCCESS
        self.reason = ''
        self.session = session.Session(self.application.session_manager, self)
        self.wechat = WeChat()
        self.loger = runtime_logger()
        self.db = InDanceDB()

    def on_finish(self):
        pass

    def get_need_args(self, *args):
        res = {}
        for arg in args:
            res[arg] = self.get_argument(arg, '')
        return res

    def write_res(self, code, msg='', res={}):
        if not msg:
            msg = ERROR_MAP.get(code, '')
        self.write(json.dumps({'code': code, 'msg': msg, 'res': res}).decode('unicode-escape'))

    def url_get(self, urls):
        req = urllib2.Request(urls)
        response = urllib2.urlopen(req)
        return json.loads(response.read())
