# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from app.model.event import Event
from flask import request, render_template
from app.controller import auth_required

@app.route("/events")
def events():
    evs = Event.query_all(orderby='open_at asc')
    if evs:
        return [Event(**ev).to_dict() for ev in evs]
    else:
        return []

@app.route("/event/<event_id>")
def event_info(event_id=None):
    ev = Event.find(event_id)
    if ev:
        return ev.to_dict()
    else:
        return {}

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
    return render_template('event.html', event=ev)
