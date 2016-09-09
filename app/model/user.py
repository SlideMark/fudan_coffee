# -*- coding: utf-8 -*-

__author__ = 'wills'

from app.core.dao import DAO

class User(DAO):

    TABLE = 'fc_user'
    COLUMNS = ['name', 'gender', 'province', 'city', 'avatar',
               'balance', 'coupon',
               'openid', 'unionid', 'phone', 'access_token']
