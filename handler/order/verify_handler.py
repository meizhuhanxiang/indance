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


class VerifyHandler(BaseHandler):
    def get(self):
        open_id = self.get_argument('open_id', None)
        kind_id = self.get_argument('kind_id', None)
        # 参数验证 身份验证

        if kind_id and open_id:
            user = db.query(User).filter_by(open_id=open_id).first()
            if user:
                order = db.query(Order).filter_by(user_id=user.id, kind_id=kind_id).first()
                if order:
                    order.verify_count += 1
                    order.verify_time = datetime.now()
                    (res, reason) = (1, u'验证通过') if order.status == 1 else (0, u"支付未完成")
                else:
                    res, reason = 0, u'无此比赛舞种'

            else:
                res, reason = 0, u'无此用户'
        else:
            # 返回数据，如果reason为空则表示成功，否则表示出错
            res, reason = 0, u'参数错误'

        self.write({'res': res, 'reason': reason})