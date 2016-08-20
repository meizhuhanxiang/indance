# coding: utf-8
import MySQLdb
import MySQLdb.cursors as cursors
import utils.config
from utils.error import *
from utils.code import *
from DBUtils.PooledDB import PooledDB

__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


class BaseDB(object):
    def __init__(self):
        self.connect_info = {
            'host': utils.config.get("preseller_mysql", "host"),
            'user': utils.config.get("preseller_mysql", "user"),
            'port': int(utils.config.get("preseller_mysql", "port")),
            'passwd': utils.config.get("preseller_mysql", "passwd"),
            'database': utils.config.get('preseller_mysql', 'database')
        }
        self.list_pool = self.create_pool('list')
        self.dict_pool = self.create_pool('dict')

    def create_pool(self, cursor_type='list'):
        if cursor_type == 'dict':
            mysql_cursor = cursors.DictCursor
        else:
            mysql_cursor = cursors.SSCursor
        pool = PooledDB(MySQLdb,
                        host=self.connect_info['host'],
                        port=self.connect_info['port'],
                        user=self.connect_info['user'],
                        passwd=self.connect_info['passwd'],
                        db=self.connect_info['database'],
                        cursorclass=mysql_cursor,
                        charset='utf8')
        return pool

    def get_cursor(self, cursor_type='list'):
        if cursor_type == 'dict':
            conn = self.dict_pool.connection()
            cursor = conn.cursor()
            return conn, cursor
        else:
            conn = self.list_pool.connection()
            cursor = conn.cursor()
            return conn, cursor

    def fetch_all(self, sql, args=[], cursor_type='list'):
        conn = cursor = None
        try:
            conn, cursor = self.get_cursor(cursor_type)
            cursor.execute(sql, args)
            res = cursor.fetchall()
            return list(res)
        except Exception, e:
            raise DBException(e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
