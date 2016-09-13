# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from flask import request
from app.model.shop import Shop
from app.core.response import Response, ResponseCode
from app.model.product import Product
from app.model.ledger import Ledger
from app.model.user import auth_required

@app.route("/products")
def products():
    shop_id = request.args.get('shop_id', Shop.GEHUA)
    products = Product.query(fetchone=False, shop_id=shop_id) or []
    return str(Response(data=[Product(**each).to_dict() for each in products]))

@app.route("/product/<product_id>", methods=['GET'])
@auth_required
def product(product_id=0):
    product = Product.find(product_id)
    return str(Response(data=product.to_dict()))

@app.route("/product/<product_id>/with_balance", methods=['POST'])
@auth_required
def buy_product(product_id=0):
    pd = Product.find(product_id)
    user = request.user

    if user.balance >= pd.price:
        user.balance -= pd.price
        user.save()

        ledger = Ledger()
        ledger.name = pd.name
        ledger.item_id = pd.id
        ledger.money = -pd.price
        ledger.type = Ledger.Type.BUY_USE_COUPON
        ledger.uid = user.id
        ledger.save()

        return str(Response(data=pd.to_dict()))
    else:

        return str(Response(code=ResponseCode.LOW_BALANCE, msg='余额不足'))


@app.route("/product/<product_id>/with_coupon", methods=['POST'])
@auth_required
def buy_product_with_coupon(product_id=0):
    pd = Product.find(product_id)
    user = request.user
    if user.is_founder():
        discount = 0.4
    elif user.is_cofounder():
        discount = 0.3
    else:
        discount = 0.2

    discount_money = min(user.coupon, int(pd.price*discount))
    need_money = pd.price - discount_money

    if user.balance >= need_money:
        user.coupon -= discount_money
        user.balance -= need_money
        user.save()

        ledger = Ledger()
        ledger.name = pd.name
        ledger.item_id = pd.id
        ledger.money = -discount_money
        ledger.type = Ledger.Type.BUY_USE_COUPON
        ledger.uid = user.id
        ledger.save()

        ledger2 = Ledger()
        ledger2.name = pd.name
        ledger2.money = -need_money
        ledger2.uid = user.id
        ledger2.item_id = pd.id
        ledger2.save()

        return str(Response(data=pd.to_dict()))
    else:

        return str(Response(code=ResponseCode.LOW_BALANCE, msg='余额不足'))