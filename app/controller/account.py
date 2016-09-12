# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app, conf
from app.model.user import User
from flask import request, render_template, abort, make_response
from app.util.weixin import WXClient
from app.core.response import ResponseCode
from app.model.user import auth_required
import hashlib

@app.route("/account/signin")
def wechat_signin():

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

    resp = make_response(render_template('user.html', user=user))
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
    phone = request.form.get('phone')
    password = request.form.get('password')
    password = hashlib.md5('fudan_coffee-%s' % password).hexdigest().lower()
    user = User.query_instance(phone=phone, password=password)
    if user:
        user.update_session()
        user.save()
        resp = make_response(render_template('user.html', user=user))
        resp.set_cookie('uid', '%s' % user.id)
        resp.set_cookie('session', user.session_data)
        return resp
    else:
        return render_template('error.html', msg='User Not Found!')

@app.route("/account/signout")
@auth_required
def signout():
    resp = make_response(render_template('signin.html'))
    resp.set_cookie('uid', '')
    resp.set_cookie('session', '')
    return resp

@app.route("/account/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    phone = request.form.get('phone')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    if password == password_confirm and password is not None:
        password = hashlib.md5('fudan_coffee-%s' % password).hexdigest().lower()
        user = User.query_instance(phone=phone, password=password)
        if user:
            return render_template('error.html', msg='Phone already existed!')
        else:
            user = User()
            user.name = phone
            user.password = password
            user.phone = phone
            user.openid = 'dummy'
            user.update_session()
            user.save()

            user = User.query_instance(phone=phone, password=password)
            resp = make_response(render_template('user.html', user=user))
            resp.set_cookie('uid', '%s' % user.id)
            resp.set_cookie('session', user.session_data)
            return resp

    elif password == password_confirm:
        return render_template('error.html', msg='Same password!')
    else:
        return render_template('error.html', msg='Signup msg error!')