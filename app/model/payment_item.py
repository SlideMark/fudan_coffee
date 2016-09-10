# -*- coding: utf-8 -*-

__author__ = 'wills'

from app.core.dao import DAO

class PaymentItem(DAO):

    TABLE = 'fc_payment_item'
    COLUMNS = ['name', 'description', 'money', 'charge']
