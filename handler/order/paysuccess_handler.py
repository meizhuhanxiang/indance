#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2016/8/23 18:54
"""

import tornado
from datetime import datetime
import time
from utils.code import *
import traceback
from utils.wechat import oauth
import utils.config
from model.models import db, Order, User, Purchase, Kind
from handler.base.base_handler import BaseHandler


class PaysuccessHandler(BaseHandler):
    @oauth
    def get(self):
        try:
            self.loger.info('in paysuccess')
            args = self.get_need_args('out_trade_no')
            out_trade_no = args['out_trade_no']
            if not out_trade_no:
                self.write_res(ARGUMENT_MISSING)
                return
            orders = db.query(Order).filter_by(out_trade_no=out_trade_no).all()
            time.sleep(2)
            for aaa in orders:
                self.loger.info(aaa.status)
                self.loger.info(aaa.notified)
            if orders and orders[0].status == 1 and not orders[0].notified:
                user_id = ''
                kind_ids = []
                purchase_id = ''
                for order in orders:
                    user_id = order.user_id
                    purchase_id = order.purchase_id
                    kind_ids.append(order.kind_id)
                try:
                    template_res = {
                        'db': self.db,
                    }
                    if user_id and kind_ids and purchase_id:
                        user = db.query(User).filter_by(id=user_id).first()
                        template_res['keyword1'] = '%s(%s)' % (user.name, user.nickname)
                        template_res['open_id'] = user.open_id
                        purchase = db.query(Purchase).filter_by(id=purchase_id).first()
                        template_res['keyword3'] = purchase.begin_time.strftime('%Y-%m-%d %H:%M')
                        template_res['keyword4'] = purchase.place
                        kinds = []
                        price = 0
                        for kind_id in kind_ids:
                            kind = db.query(Kind).filter_by(id=kind_id).first()
                            kinds.append(kind.kind)
                            price += kind.price
                        template_res['urls'] = '%s%s' % (
                            utils.config.get('global', 'notify_detail_domain'), order.out_trade_no)
                        template_res['keyword2'] = '%s(%s)' % (purchase.body, ','.join(kinds))
                        template_res['first'] = '您已报名成功, 报名费共%s元' % (price * 0.01)
                        template_res['remark'] = '届时，我们期待您的参加！'
                        self.wechat.send_template(**template_res)
                        for order in orders:
                            order.notified = 1
                            order.save()
                        self.write_res(SUCCESS)
                except Exception, e:
                    self.loger.error(traceback.format_exc())
        except:
            self.loger.error(traceback.format_exc())