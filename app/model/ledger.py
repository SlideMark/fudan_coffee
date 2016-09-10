# -*- coding: utf-8 -*-

__author__ = 'wills'

from app.core.dao import DAO

class Ledger(DAO):

    TABLE = 'fc_ledger'
    COLUMNS = ['uid', 'name', 'money', 'type', 'item_id']

    class Type:
        BUY_USE_BALANCE = 0
        BUY_USE_CHARGE = 1
        BUY_USE_MONEY = 2
        BUY_USE_COUPON = 3
        TRANSFER_COUPON = 4
        PAYMENT_MONEY = 5
        PAYMENT_CHARGE = 6
