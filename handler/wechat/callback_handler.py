# coding: utf-8
import requests
from handler.base.base_handler import BaseHandler

requests.packages.urllib3.disable_warnings()
__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'


class CallbackHandler(BaseHandler):
    def get(self):
        args = self.get_need_args('code', 'state')
        code = args['code']
        state = args['state']
        callback_url = self.session['callback_url']
        self.wechat.get_access_token(code)
        wechat_user_info = self.wechat.get_user_info()
        self.loger.info(wechat_user_info)
        self.db.save_wechat_user_info(wechat_user_info)
        self.session['open_id'] = self.wechat.open_id
        self.session['callback_url'] = None
        self.session.save()
        self.redirect(callback_url)
