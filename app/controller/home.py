# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from flask import render_template
from app.model.user import auth_required

@app.route("/")
@auth_required
def root():
    return render_template('index.html')
