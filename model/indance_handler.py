# coding: utf-8
import datetime
from utils.code import *
from model.base_handler import BaseDB

__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'


class InDanceDB(BaseDB):
    def save_wechat_user_info(self, user_info):
        conn, cursor = self.get_cursor()
        sql = "select count(1) from `user` where `open_id`='%s'" % user_info['open_id']
        cursor.execute(sql)
        res = cursor.fetchall()
        if res[0][0] == 1:
            pass
        else:
            user_info_keys = user_info.keys()
            pre_compile = []
            infos = []
            for x in user_info_keys:
                pre_compile.append('%s')
                infos.append(str(user_info[x]))
            pre_compile = ','.join(pre_compile)
            keys = ','.join(user_info_keys)
            sql = u'insert into `user` (%s) values (%s)' % (keys, pre_compile)
            cursor.execute(sql, tuple(infos))

    def set_user_info(self, user_info):
        conn, cursor = self.get_cursor()
        user_info_keys = user_info.keys()
        pre_compile = []
        infos = []
        for x in user_info_keys:
            pre_compile.append('%s')
            infos.append(str(user_info[x]))
        pre_compile = ','.join(pre_compile)
        keys = ','.join(user_info_keys)
        sql = u'insert into `user` (%s) values (%s)' % (keys, pre_compile)
        cursor.execute(sql, tuple(infos))

    def get_user_info(self, open_id):
        sql = 'select * from `user` where open_id = "%s" '
        res = self.fetch_all(sql, [open_id])
        if res:
            return res[0]
        else:
            return {}

    def get_cache(self, cache_type):
        try:
            conn, cursor = self.get_cursor()
            sql = "select `cache`, `update_time` from `cache` t where `cache_type`=%s"
            cursor.execute(sql, (cache_type,))
            cache_info = cursor.fetchall()[0]
            if not cache_info:
                return {'code': WECHAT_NO_CACHE, 'cache': ''}
            else:
                cache, update_time = cache_info
                import datetime
                a = datetime.datetime.now()
                if (a - update_time).seconds > 5400:
                    return {'code': WECHAT_CACHE_TIME_OUT, 'cache': ''}
                else:
                    return {'code': SUCCESS, 'cache': cache}
        except Exception, e:
            return {'code': WECHAT_NO_CACHE, 'cache': ''}

    def save_cache(self, cache, cache_type):
        try:
            conn, cursor = self.get_cursor()
            sql = u'delete from `cache` where `cache_type`=%s'
            cursor.execute(sql, (cache_type,))

            a = datetime.datetime.now()
            sql = u'insert into `cache` (`cache_type`, `cache`, `update_time`) values (%s,  %s, %s)'
            cursor.execute(sql, (cache_type, cache, a))
            return True
        except Exception, e:
            return False
