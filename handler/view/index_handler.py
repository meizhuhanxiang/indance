# coding: utf-8
import urllib2
from utils.tool import get_qrcode
from handler.base.base_handler import BaseHandler

__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'


class IndexHandler(BaseHandler):
    def get(self):
        args = self.get_need_args('purchase_id')
        purchase_id = urllib2.unquote(args['purchase_id'])
        self.render('index.html', purchase_id=purchase_id)
