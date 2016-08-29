# coding: utf-8
import urllib2
from utils.tool import get_qrcode
from handler.base.base_handler import BaseHandler

__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'


class QrcodeHandler(BaseHandler):
    def get(self):
        args = self.get_need_args('data')
        data = urllib2.unquote(args['data'])
        img_io = get_qrcode(data)
        self.set_header("Content-Type", "image/*; charset=UTF-8")
        self.write(img_io)
