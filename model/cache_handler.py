# coding: utf-8
import datetime
from model.base_handler import BaseDB

__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'


class WechatCacheDB(BaseDB):
    def get_cache(self, cache_type, tb_name):
        conn, cursor = self.get_cursor()
        sql = "select `cache` from `%s` t where `cache_type`=%%s" % tb_name
        cursor.execute(sql, (cache_type,))
        cache_info = cursor.fetchall()
        if cache_info:
            return cache_info[0][0]
        else:
            return ''

    def save_cache(self, cache, cache_type, tb_name):
        conn, cursor = self.get_cursor()
        print cache, cache_type, tb_name
        if not self.get_cache(cache_type, tb_name):
            sql = u'insert into `%s` (`cache_type`, `cache`) values (%%s,  %%s)' % tb_name
            cursor.execute(sql, (cache_type, cache))
        else:
            sql = u'update `%s` set `cache`=%%s where `cache_type`=%%s' % tb_name
            cursor.execute(sql, (cache, cache_type))
        return True
