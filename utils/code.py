# -*- coding: utf-8 -*-

__author__ = 'guoguangchuan'

# nomal
SUCCESS = 0
ARGUMENT_MISSING = 1
ARGUMENT_ILLEGAL = 2
DB_ERROR = 3
USER_NO_EXIST = 4

# wechat
WECHAT_NO_LOGIN = 200
WECHAT_OAUTH_CALLBACK_URL_MISSING = 201
WECHAT_NO_CACHE = 202  # 服务端内部使用, 不返回给前端
WECHAT_CACHE_TIME_OUT = 203  # 服务端内部使用, 不返回给前端

# order
ORDER_NO_PAY = 300
ORDER_DANCE_KIND_NULL = 301
USER_NULL = 302

ERROR_MAP = {
    SUCCESS: 'success',  # 成功
    ARGUMENT_MISSING: 'argument is missing',  # 参数不存在或值为空
    ARGUMENT_ILLEGAL: 'argument is illegal',  # 参数不合法
    DB_ERROR: 'database error',  # 数据库错误
    USER_NO_EXIST: 'user does not exist',  # 用户不存在

    WECHAT_NO_LOGIN: 'wechat is not login',  # 微信未认证登陆
    WECHAT_OAUTH_CALLBACK_URL_MISSING: 'wechat oauth callback url is missing',  # 微信认证回调URL参数(callback_url)不存在或值为空
    WECHAT_NO_CACHE: 'wechat is not cache',  # 参数未缓存
    WECHAT_CACHE_TIME_OUT: 'wechat cache is time out',  # 参数缓存已超时

    ORDER_NO_PAY: 'no pay',  # 支付未完成
    ORDER_DANCE_KIND_NULL: 'dance kind is null',  # 此比赛舞种

}
