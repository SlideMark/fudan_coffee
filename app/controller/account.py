# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app, conf
from app.model.user import User
from flask import request, render_template, abort
from app.util.weixin import WXClient
from app.core.response import ResponseCode

@app.route("/account/signin")
def signin():

    code = request.args.get('code')
    token = WXClient.get_wx_token(conf.wechat_app_id, conf.wechat_secret, code)
    print token
    if token and token.get('errcode') is None:
        openid = token.get('openid')
        access_token = token.get('access_token')
    else:
        resp = {'code': ResponseCode.OPERATE_ERROR,
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
            user = User.query_instance(openid=openid, master=True)
        else:
            abort(403)

    return render_template('user.html', user=user)


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
