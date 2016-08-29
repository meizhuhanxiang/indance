# coding: utf-8
from utils.code import *
from utils.wechat import oauth
from handler.base.base_handler import BaseHandler

__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'


class MenushareHandler(BaseHandler):
    @oauth
    def get(self):
        urls = '%s/?union_id=%s' % (self.wechat.domain, self.wechat.union_id)
        res = self.wechat.get_menu_share_conf(urls)
        self.write_res(SUCCESS, res=res)
