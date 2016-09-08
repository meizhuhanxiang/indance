# -*- coding: utf-8 -*-
import urllib2
import traceback
from utils.code import *
from utils.wechat import oauth
from handler.base.base_handler import BaseHandler

__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'


class IndexHandler(BaseHandler):
    @oauth
    def get(self):
        try:
            args = self.get_need_args('purchase_id', 'new')
            self.session['index_url'] = self.request.uri
            self.session.save()
            new = args['new']
            if not new:
                new = False
            else:
                new = True
            purchase_id = args['purchase_id']
            res = self.get_res(SUCCESS, res={"purchase_id": purchase_id, "finished": False, "new": new})
            self.loger.info(res)
            self.render('purchase/index.html', **res)
        except:
            self.loger.info(traceback.format_exc())