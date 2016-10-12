# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import conf
from app.util.weixin import WXClient
from app.core.dao import DAO
from app.core.response import ResponseCode, Response
import hashlib
import time
import random
from flask import request, make_response

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
        user = None
        need_cookie = False
        if uid:
            user = User.query_instance(id=uid, session_data=session)
        elif request.args.get('code'):
            code = request.args.get('code')
            token = WXClient.get_wx_token(conf.wechat_app_id, conf.wechat_secret, code)
            if token and token.get('errcode') is None:
                need_cookie = True
                openid = token.get('openid')
                access_token = token.get('access_token')
                user = User.query_instance(openid=openid)
                if user:
                    user.access_token = access_token
                    user.update_session()
                    user.save()
                else:
                    user = User()
                    user.openid = openid
                    user.access_token = access_token
                    user.update_session()
                    if _signup(user):
                        user.save()
                        user = User.query_instance(openid=openid, master=True)

                        WXClient.send_signup_msg(user, {"openid": openid})
                    else:
                        return str(Response(code=ResponseCode.OPERATE_ERROR, msg='获取用户资料失败'))

        if user:
            request.user = user

            resp = make_response(func(*args, **argv))
            if need_cookie:
                resp.set_cookie('uid', '%s'%user.id)
                resp.set_cookie('session', user.session_data)
            return resp

        return str(Response(code=ResponseCode.AUTH_REQUIRED, msg='请先登录'))

    wraper.__name__ = func.__name__
    return wraper

def auth_optional(func):
    def wraper(*args, **argv):
        uid = request.cookies.get('uid')
        session = request.cookies.get('session')
        user = None
        need_cookie = False
        if uid:
            user = User.query_instance(id=uid, session_data=session)
        elif request.args.get('code'):
            code = request.args.get('code')
            token = WXClient.get_wx_token(conf.wechat_app_id, conf.wechat_secret, code)
            if token and token.get('errcode') is None:
                need_cookie = True
                openid = token.get('openid')
                access_token = token.get('access_token')
                user = User.query_instance(openid=openid)
                if user:
                    user.access_token = access_token
                    user.update_session()
                    user.save()
                else:
                    user = User()
                    user.openid = openid
                    user.access_token = access_token
                    user.update_session()
                    if _signup(user):
                        user.save()
                        user = User.query_instance(openid=openid, master=True)

                        WXClient.send_signup_msg(user, {"openid": openid})
                    else:
                        return str(Response(code=ResponseCode.OPERATE_ERROR, msg='获取用户资料失败'))

        request.user = user
        if user:
            resp = make_response(func(*args, **argv))
            if need_cookie:
                resp.set_cookie('uid', '%s'%user.id)
                resp.set_cookie('session', user.session_data)
            return resp
        return func(*args, **argv)

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

def _signup(user):
    wx_user = WXClient.get_wx_profile(user.openid, user.access_token)
    if wx_user and wx_user.get('errcode') is None:
        user.name = wx_user.get('nickname')
        user.gender = wx_user.get('sex')
        user.avatar = wx_user.get('headimgurl')
        user.province = wx_user.get('province')
        user.city = wx_user.get('city')
        user.unionid = wx_user.get('unionid')
        return True
    else:
        return False