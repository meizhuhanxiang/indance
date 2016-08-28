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


class SetinfoHandler(BaseHandler):
    @oauth
    def post(self):
        args = self.get_need_args('name', 'job', 'company', 'phone', 'email')
        name = args['name']
        job = args['job']
        company = args['company']
        phone = args['phone']
        email = args['email']
        if not (name and job and company and phone and email):
            self.write_res(ARGUMENT_MISSING)
            return
        self.db.set_user_info(args)
        self.write_res(SUCCESS)
