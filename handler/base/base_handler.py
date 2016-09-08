#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib2
import tornado.web
import tornado.ioloop
import tornado.options
import utils.config
import tornado.httpserver
from utils.code import *
from utils import session
from utils.wechat import WeChat
from model.indance_handler import InDanceDB
from utils.logger import runtime_logger
import xml.etree.ElementTree as ET


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        # self.set_header('Access-Control-Allow-Origin', '*')
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        # self.set_header('Access-Control-Max-Age', 1000)
        # self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'text/html;charset=utf-8')
        pass

    def initialize(self):
        self.code = SUCCESS
        self.reason = ''
        self.session = session.Session(self.application.session_manager, self)
        self.wechat = WeChat()
        self.domain = utils.config.get('global', 'domain')
        self.loger = runtime_logger()
        self.db = InDanceDB('preseller_mysql')

    def on_finish(self):
        self.logger.info('session finished')
        self.session.close()
        self.logger.info('session closed')

    def get_need_args(self, *args):
        res = {}
        for arg in args:
            res[arg] = self.get_argument(arg, '')
        return res

    def write_res(self, code, msg='', res=None):
        res = self.get_res(code, msg, res)
        #self.write(json.dumps(res).decode('unicode-escape'))
        self.write(json.dumps(res))
        #self.write(res)

    def get_res(self, code, msg='', res=None):
        if not res:
            res={}
        if not msg:
            msg = ERROR_MAP.get(code, '')
        return {'code': code, 'msg': msg, 'res': res}

    def url_get(self, urls):
        req = urllib2.Request(urls)
        response = urllib2.urlopen(req)
        return json.loads(response.read())

    def xmlToArray(self, xml):
        """将xml转为array"""
        array_data = {}
        root = ET.fromstring(xml)
        for child in root:
            value = child.text
            array_data[child.tag] = value
        return array_data
