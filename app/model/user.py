# -*- coding: utf-8 -*-

__author__ = 'wills'

from app.core.dao import DAO
from app.core.response import ResponseCode, Response
import hashlib
import time
import random
from flask import request

class User(DAO):

    TABLE = 'fc_user'
    COLUMNS = ['id', 'name', 'gender', 'province', 'city', 'avatar',
               'balance', 'coupon', 'role', 'session_data', 'password',
               'openid', 'unionid', 'phone', 'access_token', 'create_at', 'update_at']
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

    def update_session(self):
        md5 = hashlib.md5()
        md5.update('%s-%s-%s' % ('fudan_coffee', time.time(), random.randint(0,1000)))
        self.session_data = md5.hexdigest().lower()

    def json(self):
        c = ['id', 'name', 'gender', 'province', 'city', 'avatar',
               'balance', 'coupon', 'role', 'phone']
        result = {}
        for each in c:
            result[each] = getattr(self, each)

        return result

def auth_required(func):
    def wraper(*args, **argv):
        uid = request.cookies.get('uid')
        session = request.cookies.get('session')
        if uid:
            usr = User.query_instance(id=uid, session_data=session)
            if usr:
                request.user = usr
                return func(*args, **argv)
        return str(Response(code=ResponseCode.AUTH_REQUIRED, msg='请先登录'))

    wraper.__name__ = func.__name__
    return wraper

def logedin(request):
    uid = request.cookies.get('uid')
    session = request.cookies.get('session')
    if uid and session:
        user = User.query_instance(id=uid, session_data=session)
        if user:
            request.user = user
            return True
    return False
