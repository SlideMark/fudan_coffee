# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from flask import request
from app.model.shop import Shop
from app.core.response import Response, ResponseCode
from app.model.product import Product
from app.model.user import auth_required
from app.model.order import Order, WXOrder

@app.route("/products")
def products():
    shop_id = request.args.get('shop_id', Shop.GEHUA)
    products = Product.query(fetchone=False, shop_id=shop_id) or []
    return Response(data=[Product(**each).to_dict() for each in products]).out()

@app.route("/product/<product_id>", methods=['GET'])
@auth_required
def product(product_id=0):
    product = Product.find(product_id)
    return Response(data=product.to_dict()).out()

@app.route("/product/<product_id>", methods=['POST'])
@auth_required
def buy(product_id=0):
    if request.user.balance <=0 and request.user.coupon >0:
        return _buy_product_with_balance(product_id)
    elif request.user.balance > 0 and request.user.coupon <= 0:
        return _buy_product_with_coupon(product_id)
    else:
        return Response(code=ResponseCode.UNKNOWN).out()

@app.route("/product/<product_id>/with_balance", methods=['POST'])
@auth_required
def buy_product_with_balance(product_id=0):
    return _buy_product_with_balance(product_id)

def _buy_product_with_balance(product_id):
    pd = Product.find(product_id)
    user = request.user

    if user.balance >= pd.price:
        order = Order(uid=user.id, name=pd.name, money=user.balance-pd.price,
              balance=-user.balance, type=Order.Type.PAY)
        order.set_order_id()
        order.save()

        user.balance -= pd.price
        user.save()

        return Response(data=pd.to_dict()).out()
    elif user.openid:
        order = Order(uid=user.id, name=pd.name, money=user.balance-pd.price,
              balance=-user.balance, type=Order.Type.PAY)
        order.set_order_id()
        order.save()

        order = WXOrder(user, order)

        tokens = order.get_token()
        if not tokens:
            return Response(code=ResponseCode.OPERATE_ERROR, msg='订单生成失败').out()

        return Response(code=ResponseCode.LOW_BALANCE,
                            msg='余额不足',
                            data={'need_money': pd.price-user.balance,
                                    'order': tokens}).out()
    else:
        return str(Response(code=ResponseCode.AUTH_REQUIRED, msg='请微信关注服务号'))


@app.route("/product/<product_id>/with_coupon", methods=['POST'])
@auth_required
def buy_product_with_coupon(product_id=0):
    return _buy_product_with_coupon(product_id)

def _buy_product_with_coupon(product_id):
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

    if user.openid:
        order = Order(uid=user.id, name=pd.name, money=-need_money,
              coupon=-discount_money, type=Order.Type.PAY)
        order.set_order_id()
        order.save()

        wxorder = WXOrder(user, order)
        tokens = wxorder.get_token()
        if not tokens:
            return str(Response(code=ResponseCode.OPERATE_ERROR, msg='订单生成失败'))

        return str(Response(code=ResponseCode.LOW_BALANCE,
                                msg='余额不足',
                                data={'need_money': need_money,
                                      'order': tokens}))
    else:
        return str(Response(code=ResponseCode.AUTH_REQUIRED, msg='请微信关注服务号'))
