# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from app.model.user import User

@app.route("/user/<uid>")
def user(uid=None):
    user = User.find(uid)
    if user:
        return 'uid=%s' % user.openid
    else:
        return 'cannot find user'
