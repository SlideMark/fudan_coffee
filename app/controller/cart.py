# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from flask import render_template, abort, request, redirect, url_for
from app.model.cart import Cart
from app.model.ledger import Ledger
from app.model.user import auth_required
from app.model.product import Product

@app.route("/cart", methods=['GET'])
@auth_required
def cart():
    user = request.user
    carts = Cart.query(fetchone=False, uid=user.id, state=Cart.State.INIT)
    for each in carts:
        pd = Product.find(each['product_id'])
        each['product_name'] = pd.name
        each['price'] = pd.price
    return render_template('cart.html', user=user,
                           carts=carts)


@app.route("/cart", methods=['POST'])
@auth_required
def add_cart():
    product_id = request.form['product_id']
    pd = Product.find(product_id)

    if not pd:
        abort(404)
        return

    cart = Cart()
    cart.uid = request.user.id
    cart.product_id = product_id
    cart.save()
    return redirect(url_for('cart', uid=request.user.id))


@app.route("/cart/pay_with_balance", methods=['POST'])
@auth_required
def pay_cart_with_balance():
    user = request.user
    carts = Cart.query(fetchone=False, uid=user.id, state=Cart.State.INIT)
    if not carts:
        abort(404)
        return
    success = []
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

            success.append(each)

    if success:
        return render_template('pay_cart_success.html', carts=success)
    else:
        return render_template('pay_cart_fail.html', carts=carts)



@app.route("/cart/pay_with_coupon", methods=['POST'])
@auth_required
def pay_cart_with_coupon():
    user = request.user
    carts = Cart.query(fetchone=False, uid=user.id, state=Cart.State.INIT)
    if not carts:
        abort(404)
        return
    success = []
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

            success.append(each)

    if success:
        return render_template('pay_cart_success.html', carts=success)
    else:
        return render_template('pay_cart_fail.html', carts=carts)