# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from flask import request
from app.model.cart import Cart
from app.model.user import auth_required
from app.model.product import Product
from app.model.order import Order, WXOrder
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
        cart['product_icon'] = pd.icon
        resp.append(cart)
    return str(Response(data=resp))


@app.route("/cart", methods=['POST'])
@auth_required
def add_cart():
    product_id = request.form['product_id']
    if not product_id or not Product.find(product_id):
        return str(Response(code=ResponseCode.DATA_NOT_EXIST, msg='商品不存在'))

    cart = Cart.query_instance(uid=request.user.id, product_id=product_id, state=Cart.State.INIT)
    if cart:
        cart.num += 1
    else:
        cart = Cart()
        cart.uid = request.user.id
        cart.product_id = product_id
    ct = cart.save(return_keys=[Cart.PKEY])
    cart = Cart.find(ct[Cart.PKEY])

    return Response(data=cart.to_dict()).out()


@app.route("/cart/update", methods=['POST'])
@auth_required
def update_cart():
    cart_id = request.form['cart_id']
    num = request.form['num']
    cart = Cart.query_instance(id=cart_id, uid=request.user.id)

    if not cart:
        return str(Response(code=ResponseCode.DATA_NOT_EXIST, msg='数据不存在'))

    cart.num = num
    cart.save()
    return Response(data=cart.to_dict()).out()

@app.route("/cart/delete", methods=['POST'])
@auth_required
def delete_cart():
    cart_id = request.form['cart_id']
    cart = Cart.query_instance(id=cart_id, uid=request.user.id)

    if not cart:
        return str(Response(code=ResponseCode.DATA_NOT_EXIST, msg='数据不存在'))

    cart.state = Cart.State.CANCELED
    cart.save()
    return Response(data=cart.to_dict()).out()


@app.route("/cart/pay", methods=['POST'])
@auth_required
def pay_cart():
    if request.user.balance <=0 and request.user.coupon >0:
        return _pay_cart_with_coupon()
    elif request.user.balance >= 0 and request.user.coupon <= 0:
        return _pay_cart_with_balance()
    else:
        return Response(code=ResponseCode.UNKNOWN).out()

@app.route("/cart/pay_with_balance", methods=['POST'])
@auth_required
def pay_cart_with_balance():
    return _pay_cart_with_balance()

def _pay_cart_with_balance():
    user = request.user
    carts = Cart.query(fetchone=False, uid=user.id, state=Cart.State.INIT)

    if not carts:
        return Response(code=ResponseCode.DATA_NOT_EXIST, msg='购物车内没有物品').out()
    money = 0
    name = ''

    for each in carts:
        pd = Product.find(each['product_id'])
        money += pd.price * each['num']
        if name:
            name = '%s,%s' % (name, pd.name)
        else:
            name = pd.name
    if user.balance >= money:
        resp = []
        for each in carts:
            pd = Product.find(each['product_id'])
            ct = Cart(**each)
            ct.state = Cart.State.FINISHED
            ct.save()

            cart = Cart(**each).to_dict()
            cart['product_name'] = pd.name
            cart['product_price'] = pd.price
            cart['product_icon'] = pd.icon
            resp.append(cart)

        order = Order(uid=user.id, name=name, balance=-money, type=Order.Type.PAY)
        order.set_order_id()
        order.save()

        user.balance -= money
        user.save()
        return Response(data=resp).out()
    elif user.openid:
        order = Order(uid=user.id, name=name, money=user.balance-money,
              balance=-user.balance, type=Order.Type.PAY)
        order.set_order_id()
        order.save()

        wxorder = WXOrder(user, order)
        tokens = wxorder.get_token()
        if not tokens:
            return Response(code=ResponseCode.OPERATE_ERROR, msg='订单生成失败').out()

        return Response(code=ResponseCode.LOW_BALANCE,
                            msg='余额不足',
                            data={'need_money': money-user.balance,
                                    'order': tokens}).out()
    else:
        return str(Response(code=ResponseCode.AUTH_REQUIRED, msg='请微信关注服务号'))


@app.route("/cart/pay_with_coupon", methods=['POST'])
@auth_required
def pay_cart_with_coupon():
    return _pay_cart_with_coupon()

def _pay_cart_with_coupon():
    user = request.user
    carts = Cart.query(fetchone=False, uid=user.id, state=Cart.State.INIT)

    if not carts:
        return Response(code=ResponseCode.DATA_NOT_EXIST, msg='购物车内没有物品').out()

    if user.is_founder():
        discount = 0.4
    elif user.is_cofounder():
        discount = 0.3
    else:
        discount = 0.2

    money = 0
    name = ''
    for each in carts:
        pd = Product.find(each['product_id'])
        money += pd.price * each['num']
        if name:
            name = '%s,%s' % (name, pd.name)
        else:
            name = pd.name

    discount_money = min(user.coupon, int(money*discount))
    need_money = money - discount_money

    if user.openid:
        order = Order(uid=user.id, name=name, money=-need_money,
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
