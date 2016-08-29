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


class SignupHandler(BaseHandler):
    @oauth
    def post(self):
        res = []
        code = SUCCESS
        arguments = tornado.escape.json_decode(self.request.body)
        kind_id = arguments.get('kind_id', [])
        phone = arguments.get('phone', '')
        name = arguments.get('name', '')
        union_id = self.session.get('union_id', '')
        # 参数验证 身份验证


        # 新建订单
        if kind_id and union_id:
            user = db.query(User).filter_by(union_id=union_id).first()
            if user:
                user.phone = phone
                user.name = name
                db.commit()
                for i in kind_id:
                    kind = db.query(Kind).filter_by(id=i).first()
                    if kind:
                        order = db.query(Order).filter_by(user_id=user.id, kind_id=i).first()
                        if not order:
                            new_order = Order(status=0, user_id=user.id, kind_id=i, purchase_id=kind.purchase_id,
                                              create_time=datetime.now())
                            new_order.save()
                    else:
                        code = ORDER_DANCE_KIND_NULL
            else:
                code = USER_NO_EXIST

        else:
            code = ARGUMENT_ILLEGAL

        self.write_res(code)
