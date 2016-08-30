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
from utils.tool import get_uuid
from utils.wechat_pay import UnifiedOrder_pub
from model.models import db, Order, User, Purchase, Kind
from handler.base.base_handler import BaseHandler


class SignupHandler(BaseHandler):
    @oauth
    def post(self):
        args = self.get_need_args('kind_ids', 'purchase_id', 'phone', 'name')
        kind_ids = args['kind_ids']
        purchase_id = args['purchase_id']
        phone = args['phone']
        name = args['name']
        wechat_no = args['wechat_no']
        if not (kind_ids and phone and name and purchase_id):
            self.write_res(ARGUMENT_MISSING)
        else:
            union_id = self.session['union_id']
            user = db.query(User).filter_by(union_id=union_id).first()
            if user:
                user.phone = phone
                user.name = name
                user.wechat_no = wechat_no
                db.commit()
                out_trade_no = get_uuid()
                kind = None
                total_fee = 0
                for kind_id in kind_ids:
                    kind = db.query(Kind).filter_by(id=kind_id).first()
                    if kind and kind.purchase_id == purchase_id:
                        order = db.query(Order).filter_by(user_id=user.id, kind_id=kind_id).first()
                        if not order:
                            new_order = Order(status=0, user_id=user.id, kind_id=kind_id, purchase_id=kind.purchase_id,
                                              create_time=datetime.now(), out_trade_no=out_trade_no)
                            new_order.save()
                        else:
                            out_trade_no = order.out_trade_no
                        total_fee += kind.price
                    else:
                        self.write_res(ORDER_DANCE_KIND_NULL)
                purchase = db.query(Purchase).filter_by(id=kind.purchase_id).first()
                res = {
                    'body': purchase.body,
                    'out_trade_no': out_trade_no,
                    'price': price
                }
                unified = UnifiedOrder_pub()
                unified.setParameter('body', purchase.body)
                unified.setParameter('out_trade_no', out_trade_no)
                unified.setParameter('total_fee', total_fee)

            else:
                self.write_res(WECHAT_NO_LOGIN)
