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
    def post(self):
        self.loger.info('in purchase_share')
        args = self.get_need_args('purchase_id')
        purchase_id = args['purchase_id']
        try:
            if not purchase_id:
                self.write_res(ARGUMENT_MISSING)
                return
            share_url = os.path.join('%s%s' % (self.wechat.share_domain, purchase_id))
            res = self.wechat.get_menu_share_conf(share_url)
            self.loger.info(res)
            self.write_res(SUCCESS, res=res)
        except Exception, e:
            self.loger.error(traceback.traceback.format_exc())
            self.write_res(500, msg=e)

