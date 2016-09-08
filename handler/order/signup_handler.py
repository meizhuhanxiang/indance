#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2016/8/23 18:54
"""

import tornado
import os
import json
from datetime import datetime
from utils.code import *
from utils.tool import excetion
from utils.wechat import oauth
from utils.tool import get_uuid
from utils.wechat_pay import OrderQuery_pub
from model.models import db, Order, User, Purchase, Kind
from handler.base.base_handler import BaseHandler


class SignupHandler(BaseHandler):
    @oauth
    @excetion
    def post(self):
        args = self.get_need_args('kind_ids', 'purchase_id', 'phone', 'name', 'wechat_no')
        self.loger.info(args)
        kind_ids = json.loads(args['kind_ids'])
        purchase_id = int(args['purchase_id'])
        phone = int(args['phone'])
        name = args['name']
        wechat_no = args['wechat_no']
        if not (kind_ids and phone and name and purchase_id):
            self.write_res(ARGUMENT_MISSING)
            return
        else:
            union_id = self.session['union_id']
            user = db.query(User).filter_by(union_id=union_id).first()
            if user:
                res = {}
                user.phone = phone
                user.name = name
                user.wechat_no = wechat_no
                db.commit()
                out_trade_no = get_uuid()
                kind = None
                total_fee = 0
                payed_kinds = []
                for kind_id in kind_ids:
                    kind = db.query(Kind).filter_by(id=kind_id).first()
                    if kind and kind.purchase_id == purchase_id:
                        order = db.query(Order).filter_by(user_id=user.id, kind_id=kind_id).first()
                        if not order:
                            order = Order(status=0, user_id=user.id, kind_id=kind_id, purchase_id=kind.purchase_id,
                                          create_time=datetime.now(), out_trade_no=out_trade_no)
                        else:
                            if order.status != 1:
                                order.out_trade_no = out_trade_no
                        order.save()
                        # else:
                        #     order.out_trade_no = out_trade_no
                        if order.status == 1:
                            payed_kinds.append(kind.kind)

                        out_trade_no = order.out_trade_no
                        total_fee += kind.price
                    else:
                        self.write_res(ORDER_DANCE_KIND_NULL)
                if payed_kinds:
                    self.loger.info('%s已经购买过' % ','.join(payed_kinds))
                    self.write_res(KIND_ALEADY_PAYED, msg='%s 已经购买过' % ','.join(payed_kinds))
                    return
                res['out_trade_no'] = out_trade_no
                self.write_res(SUCCESS, res=res)
                return
            else:
                self.write_res(WECHAT_NO_LOGIN)
                return
