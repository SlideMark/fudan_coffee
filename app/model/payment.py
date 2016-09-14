# -*- coding: utf-8 -*-

__author__ = 'wills'

from app.core.dao import DAO

class Payment(DAO):

    TABLE = 'fc_payment'
    COLUMNS = ['id', 'uid', 'item_id', 'num', 'money', 'description', 'create_at', 'update_at']
