# -*- coding: utf-8 -*-

__author__ = 'guoguangchuan'

# nomal
SUCCESS = 0
ARGUMENT_MISSING = 1
ARGUMENT_ILLEGAL = 2
DB_ERROR = 3
USER_NO_EXIST = 4
INTERNAL_ERROR = 5

# wechat
WECHAT_NO_LOGIN = 200
WECHAT_OAUTH_CALLBACK_URL_MISSING = 201
WECHAT_NO_CACHE = 202  # 服务端内部使用, 不返回给前端
WECHAT_CACHE_TIME_OUT = 203  # 服务端内部使用, 不返回给前端
WECHAT_UNIFIED_ERROR = 204
WECHAT_SIGN_FAILED = 205


# order
ORDER_NO_PAY = 300
ORDER_DANCE_KIND_NULL = 301
USER_NULL = 302
KIND_ALEADY_PAYED = 303
ORDER_NOT_EXIST = 304
PURCHASE_NOT_EXIST = 305

ERROR_MAP_BAK = {
    SUCCESS: 'success',  # 成功
    ARGUMENT_MISSING: 'argument is missing',  # 参数不存在或值为空
    ARGUMENT_ILLEGAL: 'argument is illegal',  # 参数不合法
    DB_ERROR: 'database error',  # 数据库错误
    USER_NO_EXIST: 'user does not exist',  # 用户不存在
    INTERNAL_ERROR: 'internal error',  # 服务器内部错误

    WECHAT_NO_LOGIN: 'wechat is not login',  # 微信未认证登陆
    WECHAT_OAUTH_CALLBACK_URL_MISSING: 'wechat oauth callback url is missing',  # 微信认证回调URL参数(callback_url)不存在或值为空
    WECHAT_NO_CACHE: 'wechat is not cache',  # 参数未缓存
    WECHAT_CACHE_TIME_OUT: 'wechat cache is time out',  # 参数缓存已超时
    WECHAT_UNIFIED_ERROR: 'wechat unified error',  # 微信预支付错误
    WECHAT_SIGN_FAILED:'wechat sign is failed',

    ORDER_NO_PAY: 'no pay',  # 支付未完成
    ORDER_DANCE_KIND_NULL: 'dance kind is null',  # 此比赛舞种
    KIND_ALEADY_PAYED: 'this kind is aleady payed',  # 已经购买过
    ORDER_NOT_EXIST: 'order is not exist',
    PURCHASE_NOT_EXIST: 'purchase is not exist'

}
ERROR_MAP = {
    SUCCESS: '成功',  # 成功
    ARGUMENT_MISSING: '参数不存在或值为空',  # 参数不存在或值为空
    ARGUMENT_ILLEGAL: '参数不合法',  #
    DB_ERROR: '数据库错误',  #
    USER_NO_EXIST: '用户不存在',  #
    INTERNAL_ERROR: '服务器内部错误',  #

    WECHAT_NO_LOGIN: '微信未认证登陆',  #
    WECHAT_OAUTH_CALLBACK_URL_MISSING: '微信认证回调URL参数(callback_url)不存在或值为空',  #
    WECHAT_NO_CACHE: '参数未缓存',  #
    WECHAT_CACHE_TIME_OUT: '参数缓存已超时',  #
    WECHAT_UNIFIED_ERROR: '微信预支付错误',  #
    WECHAT_SIGN_FAILED:'wechat sign is failed',

    ORDER_NO_PAY: 'no pay',  # 支付未完成
    ORDER_DANCE_KIND_NULL: '无比赛舞种',  #
    KIND_ALEADY_PAYED: '已经购买过',  #
    ORDER_NOT_EXIST: 'order is not exist',
    PURCHASE_NOT_EXIST: 'purchase is not exist'

}