# coding: utf-8
import json
import os
from utils.code import *
import urllib
import utils.config
from handler.base.base_handler import BaseHandler

__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'


class OauthHandler(BaseHandler):
    def get(self):
        args = self.get_need_args('callback_url')
        current_url = urllib.unquote_plus(args['callback_url'])
        if not current_url:
            self.write_res(WECHAT_OAUTH_CALLBACK_URL_MISSING)
            return
        self.session['callback_url'] = current_url
        self.session.save()
        callback_url = urllib.quote_plus(os.path.join(self.wechat.domain, 'api/wechat/callback'))
        urls = self.wechat.get_oauth_url(callback_url)
        self.redirect(urls)
