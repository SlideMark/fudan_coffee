# -*- coding: utf-8 -*-

__author__ = 'wills'

from app.core.dao import DAO

class User(DAO):

    TABLE = 'fc_user'
    COLUMNS = ['name', 'gender', 'province', 'city', 'avatar',
               'balance', 'coupon', 'role',
               'openid', 'unionid', 'phone', 'access_token']
    INCR_FIELDS = ['balance', 'coupon']


    FOUNDER = 0b1
    COFOUNDER = 0b10
    EMPLOYEE = 0b100

    def is_founder(self):
        return self.role & self.FOUNDER

    def is_cofounder(self):
        return self.role & self.COFOUNDER

    def is_employee(self):
        return self.role & self.EMPLOYEE

    def set_founder(self):
        self.role |= self.FOUNDER

    def set_cofounder(self):
        self.role |= self.COFOUNDER

    def set_employee(self):
        self.role |= self.EMPLOYEE
