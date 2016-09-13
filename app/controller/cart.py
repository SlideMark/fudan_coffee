# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from flask import render_template, abort, request, redirect, url_for
from app.model.cart import Cart
from app.model.ledger import Ledger
from app.model.user import auth_required
from app.model.product import Product
from app.core.response import Response, ResponseCode

@app.route("/cart", methods=['GET'])
@auth_required
def cart():
    carts = Cart.query(fetchone=False, uid=request.user.id, state=Cart.State.INIT)
    resp = []
    for each in carts:
        pd = Product.find(each['product_id'])
        cart = Cart(**each).to_dict()
        cart['product_name'] = pd.name
        cart['product_price'] = pd.price
        resp.append(cart)
    return str(Response(data=resp))


@app.route("/cart", methods=['POST'])
@auth_required
def add_cart():
    product_id = request.form['product_id']
    pd = Product.find(product_id)

    if not pd:
        return str(Response(code=ResponseCode.DATA_NOT_EXIST, msg='商品不存在'))

    cart = Cart()
    cart.uid = request.user.id
    cart.product_id = product_id
    cart.save()
    return str(Response())


@app.route("/cart/pay_with_balance", methods=['POST'])
@auth_required
def pay_cart_with_balance():
    user = request.user
    carts = Cart.query(fetchone=False, uid=user.id, state=Cart.State.INIT)

    success = []
    fail = []
    for each in carts:
        pd = Product.find(each['product_id'])
        each['product'] = pd
        if user.balance > pd.price:
            ct = Cart(**each)
            ct.state = Cart.State.FINISHED
            ct.save()

            user.balance -= pd.price
            user.save()

            ledger = Ledger()
            ledger.uid = user.id
            ledger.name = pd.name
            ledger.money = -pd.price
            ledger.type = Ledger.Type.BUY_USE_COUPON
            ledger.save()

            success.append(pd.to_dict())
        else:
            fail.append(pd.to_dict())

    return str(Response(data={'success': success, 'fail': fail}))


@app.route("/cart/pay_with_coupon", methods=['POST'])
@auth_required
def pay_cart_with_coupon():
    user = request.user
    carts = Cart.query(fetchone=False, uid=user.id, state=Cart.State.INIT)

    success = []
    fail = []

    for each in carts:
        pd = Product.find(each['product_id'])
        each['product'] = pd
        if user.coupon > pd.price:
            ct = Cart(**each)
            ct.state = Cart.State.FINISHED
            ct.save()


            user.coupon -= pd.price
            user.save()

            ledger = Ledger()
            ledger.uid = user.id
            ledger.name = pd.name
            ledger.money = -pd.price
            ledger.type = Ledger.Type.BUY_USE_COUPON
            ledger.save()

            success.append(pd.to_dict())
        else:
            fail.append(pd.to_dict())

    return str(Response(data={'success': success, 'fail': fail}))
