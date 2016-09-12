# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from flask import render_template, abort, request, redirect, url_for
from app.model.user import User
from app.model.cart import Cart
from app.model.ledger import Ledger

from app.model.product import Product

@app.route("/user/<uid>/cart", methods=['GET'])
def cart(uid=0):
    user = User.find(uid)
    carts = Cart.query(fetchone=False, uid=uid, state=Cart.State.INIT)
    for each in carts:
        pd = Product.find(each['product_id'])
        each['product_name'] = pd.name
        each['price'] = pd.price
    return render_template('cart.html', user=user,
                           carts=carts)


@app.route("/user/<uid>/cart", methods=['POST'])
def add_cart(uid=0):
    product_id = request.form['product_id']
    user = User.find(uid)
    pd = Product.find(product_id)

    if not user or not pd:
        abort(404)
        return

    cart = Cart()
    cart.uid = uid
    cart.product_id = product_id
    cart.save()
    return redirect(url_for('cart', uid=uid))

@app.route("/user/<uid>/cart/pay", methods=['POST'])
def pay_cart(uid=0):
    carts = Cart.query(fetchone=False, uid=uid, state=Cart.State.INIT)
    user = User.find(uid)
    if not carts or not user:
        abort(404)
        return

    success = []
    for each in carts:
        pd = Product.find(each['product_id'])
        if user.balance > pd.price:
            ct = Cart.find(each['id'])
            ct.state = Cart.State.FINISHED
            ct.save()

            user.balance -= pd.price
            user.save()

            ledger = Ledger()
            ledger.uid = uid
            ledger.name = pd.name
            ledger.money = -pd.price
            ledger.type = Ledger.Type.BUY_USE_BALANCE
            ledger.save()

            success.append(each)
    return render_template('pay_cart_success.html', carts=success)


@app.route("/user/<uid>/cart/pay_with_coupon", methods=['POST'])
def pay_cart_with_coupon(uid=0):
    carts = Cart.query(fetchone=False, uid=uid, state=Cart.State.INIT)
    user = User.find(uid)
    if not carts or not user:
        abort(404)
        return

    success = []
    for each in carts:
        pd = Product.find(each['product_id'])
        if user.coupon > pd.price:
            each.state = Cart.State.FINISHED
            each.save()

            user.coupon -= pd.price
            user.save()

            ledger = Ledger()
            ledger.uid = uid
            ledger.name = pd.name
            ledger.money = -pd.price
            ledger.type = Ledger.Type.BUY_USE_COUPON
            ledger.save()

            success.append(each)
    return render_template('pay_cart_success.html', carts=success)
