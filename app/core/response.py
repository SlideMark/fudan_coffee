# -*- coding: utf-8 -*-

__author__ = 'wills'

import json

class ResponseCode(object):

    SUCCESS = 0
    OPERATE_ERROR = 10001
    DATA_NOT_EXIST = 10002
    AUTH_REQUIRED = 10003
    DUPLICATE_DATA = 10004
    PARAMETER_ERROR = 10005
    LOW_BALANCE = 10006
    UNKNOWN = 10007

class Response(object):

    def __init__(self, **kwargs):
        self.data = kwargs
        if not self.data:
            self.data = {'code':ResponseCode.SUCCESS}
        elif not self.data.get('code'):
            self.data['code'] = ResponseCode.SUCCESS

    def __str__(self):
        return json.dumps(self.data)

    def out(self):
        return json.dumps(self.data)
