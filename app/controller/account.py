# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from app.model.user import User
from flask import request
from app.util.weixin import WXClient
from app.core.response import ResponseCode

@app.route("/account/signin")
def signin():

    code = request.args.get('code')
    init = 0
    token = WXClient.get_service_token()
    if token and token.get('errcode') is None:
        openid = token.get('openid')
        access_token = token.get('access_token')
    else:
        resp = {'code': 1,
                'msg': '获取微信token失败'}
        return resp

    user = User.query_instance(openid=openid)
    if user:
        user.access_token = access_token
        user.update_session()
        user.save()
    else:
        user = User()
        user.openid = openid
        user.access_token = access_token
        if _signup(user):
            user.save()
            init = 1
        else:
            resp = {'code': ResponseCode.OPERATE_ERROR,
            'msg': '第三方登录失败'}
            return resp

    resp_data = user.to_dict()
    resp_data['init'] = init
    resp = {'code': ResponseCode.SUCCESS,
            'data': resp_data}
    return resp

def _signup(user):
    wx_user = WXClient.get_wx_profile(user.openid, user.access_token)
    if wx_user and wx_user.get('errcode') is None:
        user.name = wx_user.get('nickname')
        user.gender = wx_user.get('sex')
        user.headimgurl = wx_user.get('headimgurl')
        user.province = wx_user.get('province')
        user.city = wx_user.get('city')
        user.unionid = wx_user.get('unionid')
        return True
    else:
        return False
