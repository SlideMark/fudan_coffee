# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from flask import request, render_template, abort
from app.model.shop import Shop
from app.model.user import User
from app.model.product import Product
from app.model.ledger import Ledger

@app.route("/products")
def products():
    shop_id = request.args.get('shop_id', Shop.GEHUA)
    products = Product.query(fetchone=False, shop_id=shop_id) or []
    return render_template('products.html', products=products)

@app.route("/product/<product_id>", methods=['GET'])
def product(product_id=0):
    product = Product.find(product_id)
    return render_template('product.html', product=product)

@app.route("/product/<product_id>", methods=['POST'])
def buy_product(product_id=0):
    pd = Product.find(product_id)
    user = User.find(1)
    if not pd or not user:
        abort(404)
        return

    if user.is_founder():
        discount = 0.4
    elif user.is_cofounder():
        discount = 0.3
    else:
        discount = 0

    discount_money = min(user.coupon, int(pd.price*discount))
    need_money = pd.price - discount_money

    print discount_money, need_money, user.balance
    if user.balance >= need_money:
        user.coupon -= discount_money
        user.balance -= need_money
        user.save()

        ledger = Ledger()
        ledger.product_id = pd.id
        ledger.money = -discount_money
        ledger.type = 2
        ledger.uid = 1
        ledger.save()

        ledger2 = Ledger()
        ledger2.money = -need_money
        ledger2.uid = 1
        ledger2.product_id = pd.id
        ledger2.save()

        return render_template('buy_success.html', product=pd, money=need_money, discount=discount_money)
    else:

        return render_template('buy_fail.html', product=pd, msg='余额不足')
