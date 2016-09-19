# -*- coding: utf-8 -*-

__author__ = 'wills'

from flask import render_template, request
from app import app, conf
from app.model.cart import Cart
from app.model.product import Product
from app.core.response import Response, ResponseCode
from app.model.user import auth_required


if True:
    @app.route("/test/give_balance")
    @auth_required
    def give_balance():
        request.user.balance += 5000
        request.user.save()

        return render_template('error.html', msg='Success!')

    @app.route("/test/give_coupon")
    @auth_required
    def give_coupon():
        request.user.coupon += 5000
        request.user.save()

        return render_template('error.html', msg='Success!')

