#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2016/8/22 16:29
"""

from utils.code import *
from utils.wechat import oauth
from model.models import db, Order, User, Purchase
from handler.base.base_handler import BaseHandler


class ListHandler(BaseHandler):
    @oauth
    def get(self):
        res = []
        union_id = self.session.get('union_id', None)
        purchase_id = self.get_argument('purchase_id', None)

        if union_id:
            user = db.query(User).filter_by(union_id=union_id).first()
            if user:
                if purchase_id:
                    all_orders = db.query(Order).filter_by(user_id=user.id, purchase_id=purchase_id).all()
                else:
                    all_orders = db.query(Order).filter_by(user_id=user.id).all()

                for i in all_orders:
                    res.append(i.items)

        res = self.get_res(SUCCESS, res=res)
        self.render('order/list.html', **res)
