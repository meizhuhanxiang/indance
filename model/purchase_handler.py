# coding: utf-8
import json
from model.base_handler import BaseDB

__author__ = 'guoguangchuan'
__email__ = 'ggc0402@qq.com'


class Purchase(BaseDB):

    def recommend(self, purchase_id):
        sql = 'select u.profile, u.name, u.job, u.is_v, r.content from `recommend` r ' \
              'left join `user` u on r.user_id=u.id where r.purchase_id=%s'
        res = self.fetch_all(sql, [purchase_id], 'dict')
        return res

    def publisher(self, purchase_id):
        sql = 'select p.brief_introduction, p.tag_title, p.tag_content'


if __name__ == '__main__':
    p = Purchase()
    p.recommend(1)
