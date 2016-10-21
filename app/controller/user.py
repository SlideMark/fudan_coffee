# -*- coding: utf-8 -*-

__author__ = 'wills'

import time
from datetime import datetime
import hashlib
from app import app,conf
from app.model.event import Event
from flask import request
from app.core.response import Response, ResponseCode
from app.model.user import auth_required, User
from app.model.user_event import UserEvent
from app.util.timeutil import dt_to_str
from app.core.cache import LocalCache
from app.util.weixin import WXClient
from app.util.qn import QiniuCloud

@app.route("/signature")
def signature():
    url = request.args.get('url')
    import logging
    logging.error(url)
    ticket = LocalCache.get('TICKET_CACHE_KEY')
    if not ticket:
        token = WXClient.get_service_token()
        ticket_info = WXClient.get_js_ticket(token)
        if not ticket_info or ticket_info.get('errcode'):
            return Response(code=ResponseCode.OPERATE_ERROR, msg='获取ticket失败').out()

        ticket = ticket_info.get('ticket')
        expire_time = ticket_info.get('expires_in')
        LocalCache.set('TICKET_CACHE_KEY', ticket, expire_time=expire_time - 100)

    time_stamp = int(time.time())
    noncestr = hashlib.md5(str(time.time())).hexdigest().lower()
    msgs = [['jsapi_ticket', ticket],
                ['noncestr', noncestr],
                ['timestamp', time_stamp],
                ['url', url]]

    signature = hashlib.sha1('&'.join(['%s=%s' % (msg[0], msg[1]) for msg in msgs])).hexdigest()
    return Response(data={
        'appId': conf.wechat_app_id,
        'signature': signature,
        'timestamp': time_stamp,
        'nonceStr': noncestr}).out()

@app.route("/user")
@auth_required
def me():
    return Response(user=request.user.json()).out()

@app.route("/user/<uid>")
@auth_required
def user(uid=0):
    user = User.find(uid)
    if user:
        return Response(user=user.json()).out()
    else:
        return Response(code=ResponseCode.DATA_NOT_EXIST, msg='不存在此用户').out()

@app.route("/user/events/join")
@auth_required
def joined_events():
    evs = UserEvent.query(fetchone=False, uid=request.user.id,
                          state=UserEvent.State.INIT, orderby='id desc')
    resp = []
    for each in evs:
        ev = Event.find(each['event_id'])
        r = ev.to_dict()
        r['join_at'] = dt_to_str(each['create_at'])
        resp.append(r)
    return Response(data=resp).out()

@app.route("/user/events/publish")
@auth_required
def published_events():
    evs = Event.query(fetchone=False, creator=request.user.id, extra={"state <": Event.State.DELETED}, orderby='id desc')
    resp = []
    for each in evs:
        ev = Event(**each)
        r = ev.to_dict()
        r['num'] = UserEvent.count(event_id=ev.id, state=UserEvent.State.INIT)
        resp.append(r)
    return str(Response(data=resp))

@app.route("/user/event/<event_id>")
@auth_required
def user_event(event_id=0):
    ev = Event.find(event_id)
    ev_user = UserEvent.query(fetchone=False, event_id=ev.id,
                              state=UserEvent.State.INIT, orderby='id desc')
    resp = ev.to_dict()
    users = []
    for each in ev_user:
        user = User.find(each['uid'])
        r = user.json()
        r['join_at'] = dt_to_str(each['create_at'])
        users.append(r)

    resp['users'] = users
    resp['num'] = len(users)
    return Response(data=resp).out()


@app.route("/user/event/<event_id>", methods=['DELETE'])
@auth_required
def delete_event(event_id=0):
    ev = Event.find(event_id)
    if ev.creator != request.user.id:
        return Response(code=ResponseCode.OPERATE_ERROR, msg='没有权限').out()
    ev.state = Event.State.DELETED
    ev.save()
    return Response().out()


@app.route("/user/event/<event_id>", methods=['PUT'])
@auth_required
def edit_event(event_id=0):
    ev = Event.find(event_id)
    ev.fee = int(request.form.get('fee', 0)) * 100
    ev.shop_id = request.form.get('shop_id', 0)
    ev.show_num = request.form.get('show_num') == 'on'
    ev.title = request.form.get('title')
    ev.user_limit = request.form.get('user_limit', 0)
    ev.description = request.form.get('description')
    ev.open_at = request.form.get('open_at')
    ev.close_at = request.form.get('close_at')

    file = request.files.get('poster')
    if file and file.filename != "" and  allowed_file(file.filename):
        filename = '%s_%s' % (request.user.id, datetime.now().strftime('%Y%m%d%H%M%S'))
        QiniuCloud.upload_file(file, filename, conf.qiniu_img_bucket)
        ev.poster_url = conf.qiniu_img_prefix + filename
    ev.save()

    return str(Response())

@app.route("/event", methods=['POST'])
@auth_required
def create_event():
    ev = Event()
    ev.fee = int(request.form.get('fee', 0)) * 100
    ev.shop_id = request.form.get('shop_id', 0)
    ev.show_num = request.form.get('show_num') == 'on'
    ev.title = request.form.get('title')
    ev.user_limit = request.form.get('user_limit', 0)
    ev.description = request.form.get('description')
    ev.creator = request.user.id
    ev.open_at = request.form.get('open_at')
    ev.close_at = request.form.get('close_at')

    file = request.files.get('poster')
    if not file or file.filename == '':
        return Response(code=ResponseCode.OPERATE_ERROR, msg='请选择上传文件').out()
    elif allowed_file(file.filename):
        filename = '%s_%s' % (request.user.id, datetime.now().strftime('%Y%m%d%H%M%S'))
        QiniuCloud.upload_file(file, filename, conf.qiniu_img_bucket)
        ev.poster_url = conf.qiniu_img_prefix + filename
        ev.save()
    else:
        return Response(code=ResponseCode.OPERATE_ERROR, msg='请选择正确的上传格式文件').out()

    return str(Response())

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['jpg', 'png', 'JPG', 'PNG']