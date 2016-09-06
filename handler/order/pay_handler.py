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


class PayHandler(BaseHandler):
    @oauth
    def post(self):
        unified = UnifiedOrder_pub()
        unified.setParameter('body', str(purchase.body))
        unified.setParameter('out_trade_no', str(out_trade_no))
        unified.setParameter('total_fee', str(total_fee))
        unified.setParameter('notify_url', self.wechat.notify_url)
        unified.setParameter('trade_type', 'JSAPI')
        unified.setParameter('openid', self.session['open_id'])
        jsapi_res = unified.getJSApiParameters()

        self.write_res(code)
