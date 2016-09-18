# -*- coding: utf-8 -*-

__author__ = 'wills'

from app.core.dao import DAO

class Cart(DAO):

    TABLE = 'fc_cart'
    COLUMNS = ['id', 'uid', 'product_id', 'state', 'num', 'create_at', 'update_at']
    INCR_FIELDS = ['num']

    class State:
        INIT = 0
        FINISHED = 1
        CANCELED = 2
