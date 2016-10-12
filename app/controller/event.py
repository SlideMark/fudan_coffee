# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from app.model.event import Event
from app.model.order import Order, WXOrder
from flask import request
from app.core.response import Response, ResponseCode
from app.model.user import auth_required
from app.model.user_event import UserEvent

@app.route("/events")
def events():
    evs = Event.query_all(orderby='open_at asc')
    resp = []
    for each in evs:
        ev = Event(**each)
        r = ev.to_dict()
        r['creator'] = ev.get_creator().to_dict()
        r['num'] = UserEvent.count(event_id=ev.id, state=UserEvent.State.INIT)
        resp.append(r)
    return str(Response(data=resp))

@app.route("/event/<event_id>", methods=['GET'])
@auth_required
def event(event_id=0):
    ev = Event.find(event_id)
    resp = ev.to_dict()
    resp['creator'] = ev.get_creator().to_dict()
    resp['num'] = UserEvent.count(event_id=ev.id, state=UserEvent.State.INIT)

    if UserEvent.query(event_id=ev.id, uid=request.user.id, state=UserEvent.State.INIT):
        resp['member'] = 1
    else:
        resp['member'] = 0
    return str(Response(data=resp))

@app.route("/event/<event_id>", methods=['POST'])
@auth_required
def join_event(event_id=0):
    ev = Event.find(event_id)
    user = request.user
    user_ev = UserEvent.query(uid=user.id, event_id=ev.id)
    if user_ev and user_ev['state'] == UserEvent.State.INIT:
        return Response(code=ResponseCode.DUPLICATE_DATA, msg='已经报名成功').out()

    if ev.fee <= 0:
        if user_ev:
            user_ev = UserEvent(**user_ev)
            user_ev.state = UserEvent.State.INIT
            user_ev.save()
        else:
            UserEvent(uid=user.id, event_id=ev.id).save()

        return Response().out()
    elif user.openid:
        order = Order(uid=user.id, name=ev.title, money=-ev.fee,
                      item_id=ev.id, type=Order.Type.JOIN_EVENT)
        order.set_order_id()
        resp = order.save(return_keys=[Order.PKEY])
        order = Order.find(resp[Order.PKEY])

        wxorder = WXOrder(user, order)
        tokens = wxorder.get_token()
        if not tokens:
            return Response(code=ResponseCode.OPERATE_ERROR, msg='订单生成失败').out()

        return Response(code=ResponseCode.LOW_BALANCE,
                            msg='余额不足',
                            data={'need_money': ev.fee,
                                  'order_id': order.id,
                                    'order': tokens}).out()
    else:
        return str(Response(code=ResponseCode.AUTH_REQUIRED, msg='请微信关注服务号'))

@app.route("/event/<event_id>/cancel", methods=['POST'])
@auth_required
def cancel_event(event_id=0):
    ev = Event.find(event_id)
    user = request.user
    user_ev = UserEvent.query(uid=user.id, event_id=ev.id)
    if not user_ev or user_ev['state'] != UserEvent.State.INIT:
        return Response(code=ResponseCode.DATA_NOT_EXIST, msg='暂无报名').out()

    user_ev = UserEvent(**user_ev)
    user_ev.state = UserEvent.State.CANCELED
    user_ev.save()
    return Response().out()

@app.route("/event", methods=['POST'])
@auth_required
def create_event():
    ev = Event()
    ev.fee = request.form['fee'] or 0
    ev.user_limit = request.form['user_limit'] or 0
    ev.poster_url = request.form['poster_url']
    ev.description = request.form['description']
    ev.creator = request.user.id
    ev.open_at = request.form['open_at']
    ev.close_at = request.form['close_at']
    ev.save()
    return str(Response())
