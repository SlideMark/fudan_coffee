# -*- coding: utf-8 -*-

__author__ = 'wills'

from flask import request
from app.core.response import Response
from app import app
from app.model.user import auth_required

@app.route("/user")
@auth_required
def me():
    return str(Response(user=request.user.json()))
