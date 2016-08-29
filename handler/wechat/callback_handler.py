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
        current_url = self.session['current_url']
        self.wechat.get_access_token(code)
        wechat_user_info = self.wechat.get_user_info()
        self.db.save_wechat_user_info(wechat_user_info)
        self.session['union_id'] = self.wechat.union_id
        self.session['current_url'] = None
        self.session.save()
        self.redirect(current_url)
