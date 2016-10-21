# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from app.model.user import auth_required
from app.core.response import Response

@app.route("/")
@auth_required
def root():
    return Response().out()
