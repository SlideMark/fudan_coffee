# -*- coding: utf-8 -*-

__author__ = 'wills'

from flask import render_template,request
from app import app
from app.model.user import User
#from app import auth_required

@app.route("/user")
#@auth_required
def me():
    return render_template('user.html', user=request.user)

@app.route("/user/<uid>")
def user(uid=None):
    user = User.find(uid)
    return render_template('user.html', user=user)
