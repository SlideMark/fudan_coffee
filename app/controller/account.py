# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app, conf
from app.model.user import User
from flask import request, render_template, make_response
from app.util.weixin import WXClient
from app.core.response import ResponseCode, Response
from app.model.user import auth_required, logedin
import hashlib

@app.route("/account/signin")
def wechat_signin():
    if logedin(request):
        return str(Response(user=request.user.json()))

    code = request.args.get('code')
    token = WXClient.get_wx_token(conf.wechat_app_id, conf.wechat_secret, code)
    print token
    if token and token.get('errcode') is None:
        openid = token.get('openid')
        access_token = token.get('access_token')
    else:
        return str(Response(code=ResponseCode.OPERATE_ERROR, msg='获取微信token失败'))

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
            return str(Response(code=ResponseCode.OPERATE_ERROR))

    resp = make_response(str(Response(data=user.json())))
    resp.set_cookie('uid', user.id)
    resp.set_cookie('session', user.session_data)
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


@app.route("/account/login", methods=['POST'])
def password_signin():
    if logedin(request):
        # return render_template('user.html', user=request.user)
        return str(Response(code=ResponseCode.OPERATE_ERROR, msg='用户已经登录'))
    phone = request.form.get('phone')
    password = request.form.get('password')
    password = hashlib.md5('%s-%s' % (conf.salt, password)).hexdigest().lower()
    user = User.query_instance(phone=phone, password=password)
    if user:
        user.update_session()
        user.save()
        resp = make_response(str(Response(data=user.json())))
        resp.set_cookie('uid', '%s' % user.id)
        resp.set_cookie('session', user.session_data)
        return resp
    else:
        return str(Response(code=ResponseCode.DATA_NOT_EXIST, msg='用户或密码错误'))

@app.route("/account/signout")
@auth_required
def signout():
    resp = make_response(str(Response()))
    resp.set_cookie('uid', '')
    resp.set_cookie('session', '')
    return resp

@app.route("/account/signup", methods=['POST'])
def signup():
    if logedin(request):
        return str(Response(code=ResponseCode.OPERATE_ERROR, msg='用户已经登录'))

    phone = request.form.get('phone')
    password = request.form.get('password')
    if password is not None:
        password = hashlib.md5('%s-%s' % (conf.salt, password)).hexdigest().lower()
        user = User.query_instance(phone=phone, password=password)
        if user:
            return str(Response(code=ResponseCode.DUPLICATE_DATA, msg='用户已存在'))
        else:
            user = User()
            user.name = phone
            user.password = password
            user.phone = phone
            user.openid = 'dummy'
            user.update_session()
            user.save()

            user = User.query_instance(phone=phone, password=password)
            resp = make_response(str(Response(data=user.json())))
            resp.set_cookie('uid', '%s' % user.id)
            resp.set_cookie('session', user.session_data)
            return resp
    else:
        return str(Response(code=ResponseCode.PARAMETER_ERROR, msg='参数错误'))
