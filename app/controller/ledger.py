# -*- coding: utf-8 -*-

__author__ = 'wills'

from flask import request
from app import app
from app.model.user import auth_required
from app.model.order import Order

@app.route("/ledgers")
@auth_required
def ledgers():
    user = request.user
    type = request.args.get('type', 0)



