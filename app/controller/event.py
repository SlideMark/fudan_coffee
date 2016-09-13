# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from app.model.event import Event
from flask import request
from app.core.response import Response
from app.model.user import auth_required

@app.route("/events")
def events():
    evs = Event.query_all(orderby='open_at asc')
    return str(Response(data=[Event(**ev).to_dict() for ev in evs]))

@app.route("/event/<event_id>", methods=['GET'])
def event(event_id=0):
    ev = Event.find(event_id)
    return str(Response(data=ev.to_dict()))

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
