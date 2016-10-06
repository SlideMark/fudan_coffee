# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from app.model.event import Event
from flask import request
from app.core.response import Response, ResponseCode
from app.model.user import auth_required, User
from app.model.user_event import UserEvent
from app.util.timeutil import dt_to_str

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
    evs = Event.query(fetchone=False, creator=request.user.id, orderby='id desc')
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