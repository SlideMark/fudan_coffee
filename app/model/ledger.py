# -*- coding: utf-8 -*-

__author__ = 'wills'

from app.core.dao import DAO

class Ledger(DAO):

    TABLE = 'fc_ledger'
    COLUMNS = ['id', 'uid', 'name', 'money', 'type', 'item_id', 'create_at', 'update_at']

    class Type:
        BUY_USE_BALANCE = 0
        BUY_USE_MONEY = 1
        BUY_USE_COUPON = 2
        TRANSFER_COUPON = 3
        PAYMENT_MONEY = 4
