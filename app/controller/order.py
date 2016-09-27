# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from flask import request
from app.model.user import auth_required
from app.model.order import Order, WXOrder
from app.core.response import Response, ResponseCode

@app.route("/orders")
@auth_required
def orders():
    orders = Order.query(fetchone=False, uid=request.user.id, orderby='id desc')
    return Response(data=[Order(**each).to_dict() for each in orders]).out()


@app.route("/order/<order_id>", methods=['GET'])
@auth_required
def order(order_id=0):
    order = Order.find(order_id)

    return Response(data=order.to_dict()).out()


@app.route("/order/<order_id>", methods=['POST'])
@auth_required
def pay_order(order_id=0):
    order = Order.find(order_id)

    user = request.user
    if order.state != Order.State.NORMAL or user.balance + order.balance <0 or user.coupon + order.coupon <0:
        return str(Response(code=ResponseCode.DATA_NOT_EXIST, msg='订单已失效'))

    if order.money < 0:
        if user.openid:
            wxorder = WXOrder(user, order)
            tokens = wxorder.get_token()
            if not tokens:
                return str(Response(code=ResponseCode.OPERATE_ERROR, msg='订单生成失败'))

            return str(Response(data=tokens))
        elif not user.openid:
            return str(Response(code=ResponseCode.AUTH_REQUIRED, msg='请微信关注服务号'))
        else:
            return str(Response(code=ResponseCode.PARAMETER_ERROR, msg='参数错误'))
    else:
        user.balance += order.balance
        user.coupon += order.coupon
        user.save()
        order.close()
        return Response().out()

