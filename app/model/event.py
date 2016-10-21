# -*- coding: utf-8 -*-

__author__ = 'wills'

from app.core.dao import DAO
from app.model.user import User

class Event(DAO):

    TABLE = 'fc_event'
    COLUMNS = ['id', 'title', 'creator', 'state', 'fee', 'user_limit', 'poster_url', 'shop_id',
               'description', 'open_at', 'close_at', 'memo', 'create_at', 'update_at', 'show_num']

    class State:
        DRAFT = 0
        IN_REVIEW = 1
        PASSED = 2
        REJECTED = 3
        DELETED = 4

    def get_creator(self):
        return User.find(self.creator)
