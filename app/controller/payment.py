# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from flask import request
from app.model.payment_item import PaymentItem
from app.model.ledger import Ledger
from app.model.user import auth_required
from app.model.order import WXOrder
from app.core.response import Response, ResponseCode
from app.util.weixin import WXClient
from app import conf


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

    Ledger(uid=user.id, item_id=it.id, name=it.name,
            money=it.money+it.charge, type=Ledger.Type.PAYMENT_MONEY).save()

    return Response(data=it.to_dict()).out()


@app.route("/payment_order", methods=['GET'])
@auth_required
def order():
    user = request.user
    item_id = request.args.get('item_id')

    if user.openid or not item_id:
        order = WXOrder(user.id, user.openid)
        if not order.set_item(item_id):
            return str(Response(code=ResponseCode.PARAMETER_ERROR, msg='参数错误'))

        tokens = order.get_token()
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
