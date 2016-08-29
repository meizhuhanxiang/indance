# coding: utf-8
import utils.config
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from handler.base.base_handler import BaseHandler

__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'


class CheckserverHandler(BaseHandler):
    def post(self):
        args = self.get_need_args('signature', 'timestamp', 'nonce', 'echostr')
        signature = args('signature', '')
        timestamp = args('timestamp', '')
        nonce = args('nonce', '')
        echostr = args('echostr', '')
        token = utils.config.get("global", "port")
        try:
            check_signature(token, signature, timestamp, nonce)
            return echostr
        except InvalidSignatureException:
            return False
