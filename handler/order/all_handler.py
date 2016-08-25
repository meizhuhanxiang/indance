#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2016/8/22 16:29
"""

import json
from model.models import db, Order, User, Purchase
from handler.base.base_handler import BaseHandler


class AllHandler(BaseHandler):
    def get(self):
        res = []
        open_id = self.get_argument('open_id', None)
        purchase_id = self.get_argument('purchase_id', None)

        if open_id:
            user = db.query(User).filter_by(open_id=open_id).first()
            if user:
                if purchase_id:
                    all_orders = db.query(Order).filter_by(user_id=user.id, purchase_id=purchase_id).all()
                else:
                    all_orders = db.query(Order).filter_by(user_id=user.id).all()

                for i in all_orders:
                    res.append(i.items)

        # 返回数据，如果reason为空则表示成功，否则表示出错
        self.write({'reason': '', 'res': res})