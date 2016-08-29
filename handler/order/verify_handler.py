#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2016/8/23 18:54
"""
from utils.code import *
from utils.wechat import oauth
from datetime import datetime

from model.models import db, Order, User, Purchase
from handler.base.base_handler import BaseHandler


class VerifyHandler(BaseHandler):
    @oauth
    def get(self):
        union_id = self.get_argument('union_id', None)
        kind_id = self.get_argument('kind_id', None)
        # 参数验证 身份验证
        code = SUCCESS
        if kind_id and union_id:
            user = db.query(User).filter_by(union_id=union_id).first()
            if user:
                order = db.query(Order).filter_by(user_id=user.id, kind_id=kind_id).first()
                if order:
                    order.verify_count += 1
                    order.verify_time = datetime.now()
                    if order.status != 1:
                        code = ORDER_NO_PAY
                else:
                    code = ORDER_DANCE_KIND_NULL
            else:
                code = USER_NO_EXIST
        else:
            code = ARGUMENT_ILLEGAL

        self.write_res(code)
