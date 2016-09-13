# -*- coding: utf-8 -*-

__author__ = 'wills'

from app.core.dao import DAO

class PaymentItem(DAO):

    TABLE = 'fc_payment_item'
    COLUMNS = ['id', 'name', 'description', 'money', 'charge', 'create_at', 'update_at']
