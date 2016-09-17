# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app, conf
from flask import request
from app.model.cart import Cart
from app.model.ledger import Ledger
from app.model.user import auth_required
from app.model.product import Product
from app.model.order import Order
from app.core.response import Response, ResponseCode
from app.util.weixin import WXClient

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

    money = sum([each['price'] for each in carts])
    if user.balance >= money:
        for each in carts:
            pd = Product.find(each['product_id'])
            ct = Cart(**each)
            ct.state = Cart.State.FINISHED
            ct.save()

            Ledger(uid=user.id, name=pd.name,
                money=-pd.price, type=Ledger.Type.BUY_USE_COUPON).save()

        user.balance -= money
        user.save()
    elif user.openid:
        token = WXClient.get_wx_token(conf.wechat_fwh_appid, conf.wechat_fwh_mchkey, user.openid)
        if not token or token.get('errcode'):
            return Response(code=ResponseCode.OPERATE_ERROR, msg='获取微信token失败').out()

        order = Order(user.uid, user.openid)
        order.set_money(money-user.balance, balance=user.balance, from_cart=1)
        tokens = order.get_token()
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
    user = request.user
    carts = Cart.query(fetchone=False, uid=user.id, state=Cart.State.INIT)

    if user.is_founder():
        discount = 0.4
    elif user.is_cofounder():
        discount = 0.3
    else:
        discount = 0.2

    money = sum([each['price'] for each in carts])
    discount_money = min(user.coupon, int(money*discount))
    need_money = money - discount_money

    if user.openid:
        token = WXClient.get_wx_token(conf.wechat_fwh_appid, conf.wechat_fwh_mchkey, user.openid)
        if not token or token.get('errcode'):
            return str(Response(code=ResponseCode.OPERATE_ERROR, msg='获取微信token失败'))

        order = Order(user.uid, user.openid)
        order.set_money(money - discount_money, coupon=discount_money, from_cart=1)
        tokens = order.get_token()
        if not tokens:
            return str(Response(code=ResponseCode.OPERATE_ERROR, msg='订单生成失败'))

        return str(Response(code=ResponseCode.LOW_BALANCE,
                                msg='余额不足',
                                data={'need_money': need_money,
                                      'order': tokens}))
    else:
        return str(Response(code=ResponseCode.AUTH_REQUIRED, msg='请微信关注服务号'))
