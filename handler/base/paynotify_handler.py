#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2016/8/23 18:54
"""

import tornado
from datetime import datetime
from utils.code import *
from utils.wechat import oauth
from model.models import db, Order, User, Purchase, Kind
from handler.base.base_handler import BaseHandler


class PaynotifyHandler(tornado.web.RequestHandler):
    def get(self):
        self.loger.info('adfsfsafasfsafadfafsa')
