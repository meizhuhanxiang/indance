# -*- coding: utf-8 -*-
import urllib2
from utils.code import *
from utils.wechat import oauth
from handler.base.base_handler import BaseHandler

__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'


class IndexHandler(BaseHandler):
    @oauth
    def get(self):
        args = self.get_need_args('purchase_id')
        self.session['index_url'] = self.request.uri
        self.session.save()
        purchase_id = urllib2.unquote(args['purchase_id'])
        res = self.get_res(SUCCESS, res={"purchase_id": purchase_id, "finished": False})
        self.render('purchase/index.html', **res)
