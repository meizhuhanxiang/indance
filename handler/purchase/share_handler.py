#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import os
from utils.code import *
import traceback
from utils.wechat import oauth
from handler.base.base_handler import BaseHandler

__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'


class ShareHandler(BaseHandler):
    @oauth
    def get(self):
        self.set_header('Content-type', 'application/json;charset=utf-8')
        self.loger.info('in purchase_share')
        try:
            args = self.get_need_args('purchase_id')
            purchase_id = args['purchase_id']
            if not purchase_id:
                self.write_res(ARGUMENT_MISSING)
                return
            share_url = os.path.join('%s%s' % (self.wechat.share_domain, purchase_id))
            res = self.wechat.get_menu_share_conf(share_url, self.db)
            self.loger.info(res)
            self.write_res(SUCCESS, res=res)
            self.loger.info('in purchase_share: success')
        except Exception, e:
            self.loger.error(traceback.format_exc())
            self.loger.info('in purchase_share: failed')
            self.write_res(500, msg=e)

