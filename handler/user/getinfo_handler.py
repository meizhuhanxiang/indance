# coding: utf-8
import requests
import utils.config
from utils.code import *
from utils.wechat import oauth
from handler.base.base_handler import BaseHandler

requests.packages.urllib3.disable_warnings()
__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'

APPID = utils.config.get('wechat', 'appid')
APPSECRET = utils.config.get('wechat', 'appsecret')


class GetinfoHandler(BaseHandler):
    @oauth
    def post(self):
        args = self.get_need_args('open_id')
        open_id = args['open_id']
        if not open_id:
            self.write_res(ARGUMENT_MISSING)
            return
        res = self.db.get_user_info(open_id)
        self.write_res(SUCCESS, res=res)
