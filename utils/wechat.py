# coding: utf-8
import time
import hashlib
import requests
import functools
import urllib2
from model.indance_handler import InDanceDB
import utils.config
from utils.code import *
from utils.logger import runtime_logger

__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'

BASE_TOKEN = 1
WX_TICKET = 2
NONCESTR = 'Wm3WZYTPz0wzccnW'


def oauth(method):
    @functools.wraps(method)
    def warpper(self, *args, **kwargs):
        if not self.session.has_key('open_id'):
            self.write_res(WECHAT_NO_LOGIN)
        else:
            method(self, *args, **kwargs)

    return warpper


class WeChat(object):
    def __init__(self):
        self.appid = utils.config.get('wechat', 'appid')
        self.token = utils.config.get('wechat', 'token')
        self.appsecret = utils.config.get('wechat', 'appsecret')
        self.domain = utils.config.get('global', 'domain')

    def url_get(self, urls):
        req = urllib2.Request(urls)
        response = urllib2.urlopen(req)
        return json.loads(response.read())

    def get_oauth_url(self, callback_url):
        urls = 'http://www.gsteps.cn/Home/Oauth/get_wx_code?appid=%s&scope=snsapi_userinfo&state=callback&redirect_uri=%s' % (
            self.appid, callback_url)
        return urls

    def get_access_token(self, code):
        code_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?' \
                   'appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (self.appid, self.appsecret, code)
        res = self.url_get(code_url)
        access_token = res['access_token']
        open_id = res['openid']
        self.access_token = access_token
        self.open_id = open_id
        return access_token

    def get_user_info(self):
        urls = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (
            self.access_token, self.open_id)
        # urls = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (
        #     self.get_base_access_token(InDanceDB()), self.open_id)
        res = self.url_get(urls)
        runtime_logger().info(res)
        user_info = {
            'open_id': res['openid'],
            'nickname': res['nickname'],
            'sex': res['sex'],
            'province': res['province'],
            'city': res['city'],
            'country': res['country'],
            'head_img_url': res['headimgurl'],
            'privilege': res['privilege'],
        }
        self.user_info = user_info
        return user_info

    def get_base_access_token(self, db):
        cache_info = db.get_cache(BASE_TOKEN)
        code = cache_info['code']
        access_token = cache_info['cache']
        if code != SUCCESS:
            urls = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
                self.appid, self.appsecret)
            res = self.url_get(urls)
            access_token = res.get('access_token', '')
            if access_token:
                db.save_cache(access_token, BASE_TOKEN)
        return access_token

    def get_wx_ticket(self, db):
        cache_info = db.get_cache(WX_TICKET)
        code = cache_info['code']
        wx_ticket = cache_info['cache']
        if code != SUCCESS:
            urls = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi" % self.get_base_access_token()
            res = self.url_get(urls)
            wx_ticket = res.get('ticket', '')
            if wx_ticket:
                db.save_cache(wx_ticket, WX_TICKET)
        return wx_ticket

    def get_menu_share_conf(self, url):
        jsapi_ticket = self.get_wx_ticket()
        timestamps = int(time.time())
        s = 'jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s' % (jsapi_ticket, NONCESTR, timestamps, url)
        signature = hashlib.sha1(s).hexdigest()
        return json.dumps({'appid': self.appid,
                           'timestamp': timestamps,
                           'noncestr': NONCESTR,
                           'signature': signature,
                           'link': url,
                           'js_api_list': ['onMenuShareTimeline', 'onMenuShareAppMessage'],
                           'signature_decode': s
                           })
        #
        # @app.route('/conf_menu_share', methods=['get'])
        # def conf_menu_share():
        #     url = '%s/?union_id=%s' % (DOMAIN, session.get('union_id', ''))
        #     return get_menu_share_conf(url)
