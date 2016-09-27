# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from flask import request
from app.model.payment_item import PaymentItem
from app.model.user import auth_required
from app.model.order import Order, WXOrder
from app.core.response import Response, ResponseCode

@app.route("/payment_items")
@auth_required
def items():
    items = PaymentItem.query_all()
    return Response(data=[PaymentItem(**each).to_dict() for each in items]).out()


@app.route("/payment_item/<item_id>", methods=['POST'])
@auth_required
def buy_item(item_id=0):
    it = PaymentItem.find(item_id)
    user = request.user

    user.balance += user.balance + it.money + it.charge
    user.save()

    return Response(data=it.to_dict()).out()


@app.route("/payment_order", methods=['GET'])
@auth_required
def payment_order():
    user = request.user
    item_id = request.args.get('item_id')
    item = PaymentItem.find(item_id)

    if user.openid or not item_id:
        order = Order(uid=user.id, name=item.name, money=-item.money,
              balance=item.money+item.charge, type=Order.Type.CHARGE)
        order.set_order_id()
        order.save()

        wxorder = WXOrder(user, order)
        tokens = wxorder.get_token()
        if not tokens:
            return str(Response(code=ResponseCode.OPERATE_ERROR, msg='订单生成失败'))

        return str(Response(data=tokens))
    elif not user.openid:
        return str(Response(code=ResponseCode.AUTH_REQUIRED, msg='请微信关注服务号'))
    else:
        return str(Response(code=ResponseCode.PARAMETER_ERROR, msg='参数错误'))


@app.route("/payment_notify", methods=['POST'])
def notify():
        result = WXOrder.notify(request.stream.read())
        if result:
            return '''<xml>
    <return_code><![CDATA[SUCCESS]]></return_code>
    <return_msg><![CDATA[OK]]></return_msg>
</xml>'''
