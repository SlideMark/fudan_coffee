# -*- coding: utf-8 -*-

__author__ = 'wills'

from app.core.dao import DAO

class PaymentTransaction(DAO):

    TABLE = 'fc_payment_transaction'
    COLUMNS = ['id', 'uid', 'type', 'out_trade_no', 'balance', 'coupon', 'state', 'create_at', 'update_at']

    class State:
        NORMAL = 0
        FINISHED = 1
        CANCELED = 2

    class Type:
        BY_PAYMENT_ITEM = 0
        BY_DIRECTLY = 1