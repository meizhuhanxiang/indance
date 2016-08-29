#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2016/8/22 21:30
"""

from utils.wechat import oauth
from utils.code import *
from model.models import db, Order, User, Purchase, Kind
from handler.base.base_handler import BaseHandler


class KindsHandler(BaseHandler):
    @oauth
    def get(self):
        res = []
        purchase_id = self.get_argument('purchase_id', None)
        if purchase_id:
            all_kinds = db.query(Kind).join(Purchase.kinds).filter(Purchase.id == purchase_id).all()
            for i in all_kinds:
                res.append(i.items)
        res = self.get_res(SUCCESS, res=res)
        self.render('purchase/kinds.html', res=res)
