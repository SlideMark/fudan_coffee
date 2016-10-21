# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app, conf
from app.model.user import User
from flask import request, make_response
from app.core.response import ResponseCode, Response
from app.model.user import auth_required, logedin
import hashlib

@app.route("/account/signin")
@auth_required
def wechat_signin():
    return Response(data=request.user.json()).out()

@app.route("/account/login", methods=['POST'])
def password_signin():
    if logedin(request):
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


@app.route("/account/bindphone", methods=['POST'])
@auth_required
def bindphone():
    phone = request.form.get('phone')
    password = request.form.get('password')

    user = request.user
    user.phone = phone
    user.password = hashlib.md5('%s-%s' % (conf.salt, password)).hexdigest().lower()
    user.save()

    return Response(data=user.to_dict()).out()


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
            user.openid = ''
            user.update_session()
            user.save()

            user = User.query_instance(phone=phone, password=password)
            resp = make_response(Response(data=user.json()).out())
            resp.set_cookie('uid', '%s' % user.id)
            resp.set_cookie('session', user.session_data)
            return resp
    else:
        return str(Response(code=ResponseCode.PARAMETER_ERROR, msg='参数错误'))
