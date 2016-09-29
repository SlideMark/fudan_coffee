# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from app.model.event import Event
from flask import request
from app.core.response import Response
from app.model.user import auth_required
from app.model.user_event import UserEvent
from app.util.timeutil import dt_to_str

@app.route("/user_events")
@auth_required
def user_events():
    evs = UserEvent.query(fetchone=False, uid=request.user.id,
                          state=UserEvent.State.INIT, orderby='id desc')
    resp = []
    for each in evs:
        ev = Event.find(each['event_id'])
        r = ev.to_dict()
        r['join_at'] = dt_to_str(each['create_at'])
        resp.append(r)
    return Response(data=resp).out()
