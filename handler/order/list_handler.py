#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2016/8/22 16:29
"""
import json
from utils.code import *
from utils.wechat import oauth
from utils.wechat_pay import UnifiedOrder_pub
from model.models import db, Order, User, Purchase, Kind
from handler.base.base_handler import BaseHandler


class ListHandler(BaseHandler):
    @oauth
    def get(self):
        args = self.get_need_args('out_trade_no')
        out_trade_no = args['out_trade_no']
        if not out_trade_no:
            self.write_res(ARGUMENT_MISSING)
            return
        orders = db.query(Order).filter_by(out_trade_no=out_trade_no).all()
        if not orders:
            self.write_res(ORDER_NOT_EXIST)
            return
        purchase_id = ''
        total_fee = 0
        kinds = []
        user = None
        purchase = None
        for order in orders:
            purchase_id = order.purchase_id
            kind = db.query(Kind).filter_by(id=order.kind_id).first()
            kinds.append(kind.kind)
            total_fee += kind.price
            user = db.query(User).filter_by(id=order.user_id).first()
            purchase = db.query(Purchase).filter_by(id=order.purchase_id).first()
        if not user or user.union_id != self.session['union_id']:
            self.write_res(USER_NO_EXIST)
        if not purchase:
            self.write_res(PURCHASE_NOT_EXIST)
        unified = UnifiedOrder_pub()
        unified.setParameter('body', str(purchase.body))
        unified.setParameter('out_trade_no', str(out_trade_no))
        unified.setParameter('total_fee', str(total_fee))
        unified.setParameter('notify_url', self.wechat.notify_url)
        unified.setParameter('trade_type', 'JSAPI')
        unified.setParameter('openid', self.session['open_id'])
        jsapi_res = unified.getJSApiParameters()
        if jsapi_res['code'] != SUCCESS:
            self.write(jsapi_res)
            return
        res = {
            'phone': user.phone,
            'kinds': ','.join(kinds),
            'name': user.name,
            'wechat_no': user.wechat_no,
            'total_fee': total_fee * 0.01,
            'purchase_id': purchase_id,
            'out_trade_no': out_trade_no,
            'jsapi_res': json.dumps(jsapi_res['res']),
        }
        self.loger.info(jsapi_res)
        self.loger.info(res)
        self.render('purchase/orderlist.html', **res)
