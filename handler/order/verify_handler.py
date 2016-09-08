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

from model.models import db, Order, User, Purchase, Kind
from handler.base.base_handler import BaseHandler


class VerifyHandler(BaseHandler):
    @oauth
    def get(self):
        args = self.get_need_args('purchase_id', 'out_trade_no')
        purchase_id = args['purchase_id']
        out_trade_no = args['out_trade_no']
        if not purchase_id and not out_trade_no:
            self.render('/purchase/orderverify.html', **self.get_res(ARGUMENT_MISSING))
            return
        if purchase_id:
            user = db.query(User).filter_by(union_id=self.session['union_id']).first()
            purchase = db.query(Purchase).filter_by(id=purchase_id).first()
            if not purchase:
                self.render('purchase/orderverify.html', **self.get_res(PURCHASE_NOT_EXIST))
                return
            orders = db.query(Order).filter_by(purchase_id=purchase.id, user_id=user.id).all()
            kinds = []
            for order in orders:
                if order.status == 1:
                    kind = db.query(Kind).filter_by(id=order.kind_id).first()
                    kinds.append(kind.kind)
            if not kinds:
                self.redirect('/purchase/index?purchase_id=%s' % purchase_id)
            res = {
                'phone': user.phone,
                'kinds': ','.join(kinds),
                'name': user.name,
                'wechat_no': user.wechat_no,
                'type': 'signup'
            }
            self.render('purchase/orderverify.html', **self.get_res(SUCCESS, res=res))
        else:
            orders = db.query(Order).filter_by(out_trade_no=out_trade_no).all()
            if not orders:
                self.render('purchase/orderverify.html', **self.get_res(ORDER_NOT_EXIST))
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
                self.render('purchase/orderverify.html', **self.get_res(USER_NO_EXIST))
                return
            if not purchase:
                self.render('purchase/orderverify.html', **self.get_res(PURCHASE_NOT_EXIST))
                return
            res = {
                'phone': user.phone,
                'kinds': ','.join(kinds),
                'name': user.name,
                'wechat_no': user.wechat_no,
                'total_fee': total_fee * 0.01,
                'purchase_id': purchase_id,
                'out_trade_no': out_trade_no,
                'type': 'order',
            }
            self.render('purchase/orderverify.html', **self.get_res(SUCCESS, res=res))
