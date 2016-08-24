#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2016/8/23 18:54
"""

import json
import tornado
from datetime import datetime

from model.models import db, Order, User, Purchase
from handler.base.base_handler import BaseHandler


class SignupHandler(BaseHandler):
    def post(self):
        res = []
        arguments = tornado.escape.json_decode(self.request.body)
        kind_id = arguments.get('kind_id', [])
        open_id = arguments.get('open_id', None)
        phone = arguments.get('phone', "")
        nickname = arguments.get('nickname', "")
        # 参数验证 身份验证


        # 新建订单
        if kind_id and open_id:
            user = db.query(User).filter_by(open_id=open_id).first()
            if user:
                user.phone = phone
                user.nickname = nickname
                db.commit()
                for i in kind_id:
                    order = db.query(Order).filter_by(ser_id=user.id, kind_id=i).first()
                    if not order:
                        new_order = Order(status=0, user_id=user.id, kind_id=i, create_time=datetime.now())
                        new_order.save()
                self.write({'reason': '', 'res': res})
            else:
                self.write({'reason': u'无此用户', 'res': res})
        else:
            # 返回数据，如果reason为空则表示成功，否则表示出错
            self.write({'reason': u'参数错误', 'res': res})