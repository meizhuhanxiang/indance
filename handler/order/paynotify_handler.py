#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@version: 
@author:
@time: 2016/8/23 18:54
"""

import tornado
from utils.logger import runtime_logger
from utils.wechat_pay import Wxpay_server_pub
from datetime import datetime
from utils.code import *
from utils.wechat import oauth
import traceback
import datetime
import utils.config
from model.models import db, Order, User, Purchase, Kind
from handler.base.base_handler import BaseHandler


# <xml><appid><![CDATA[wx1f5f84b210348212]]></appid>
# <bank_type><![CDATA[CFT]]></bank_type>
# <cash_fee><![CDATA[1]]></cash_fee>
# <fee_type><![CDATA[CNY]]></fee_type>
# <is_subscribe><![CDATA[Y]]></is_subscribe>
# <mch_id><![CDATA[1377692402]]></mch_id>
# <nonce_str><![CDATA[crx4xawpy9fdgesqvf0c0kcp50793is6]]></nonce_str>
# <openid><![CDATA[oZDZcxIVPgABuLIbLi_ZEENVRzGM]]></openid>
# <out_trade_no><![CDATA[9866b802718311e6a84ffa163ec98286]]></out_trade_no>
# <result_code><![CDATA[SUCCESS]]></result_code>
# <return_code><![CDATA[SUCCESS]]></return_code>
# <sign><![CDATA[9DE03189B516C58EBF8C23D607C5828F]]></sign>
# <time_end><![CDATA[20160903110818]]></time_end>
# <total_fee>1</total_fee>
# <trade_type><![CDATA[JSAPI]]></trade_type>
# <transaction_id><![CDATA[4007362001201609032969671597]]></transaction_id>
# </xml>

class PaynotifyHandler(BaseHandler):
    def post(self):
        runtime_logger().info('in PaynotifyHandler') 
        wechat_server_notify = Wxpay_server_pub()
        wechat_server_notify.saveData(self.request.body)
        if not wechat_server_notify.checkSign():
            self.write(wechat_server_notify.FAIL)
            return
        wechat_data = wechat_server_notify.getData()
        self.loger.info(wechat_data)
        result_code = wechat_data.get('result_code', '')
        return_code = wechat_data.get('return_code', '')
        out_trade_no = wechat_data.get('out_trade_no', '')
        if result_code != 'SUCCESS' or return_code != 'SUCCESS' or not out_trade_no:
            self.write(wechat_server_notify.FAIL)
            return
        orders = db.query(Order).filter_by(out_trade_no=out_trade_no).all()
        if orders[0].status == 1:
            self.write(wechat_server_notify.SUCCESS)
            return
        user_id = ''
        kind_ids = []
        purchase_id = ''
        for order in orders:
            user_id = order.user_id
            purchase_id = order.purchase_id
            kind_ids.append(order.kind_id)
            order.status = 1
            order.transaction_id = wechat_data.get('transaction_id', '')
            order.save()
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
                template_res['urls'] = '%s%s' % (utils.config.get('global', 'notify_detail_domain'), order.out_trade_no)
                template_res['keyword2'] = '%s(%s)' % (purchase.body, ','.join(kinds))
                template_res['first'] = '您已报名成功, 报名费共%s元' % (price * 0.01)
                template_res['remark'] = '届时，我们期待您的参加！'
                self.wechat.send_template(**template_res)
        except Exception, e:
            self.loger.error(traceback.format_exc())
        self.write(wechat_server_notify.SUCCESS)
