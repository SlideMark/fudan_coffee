# -*- coding: utf-8 -*-

__author__ = 'wills'

from app.core.dao import DAO

class Event(DAO):

    TABLE = 'fc_event'
    COLUMNS = ['creator', 'state', 'fee', 'user_limit', 'poster_url',
               'description', 'open_at', 'close_at', 'memo', 'update_at']

    class State:
        DRAFT = 0
        IN_REVIRE = 1
        PASSED = 2
        REJECTED = 3
        DELETED = 4
