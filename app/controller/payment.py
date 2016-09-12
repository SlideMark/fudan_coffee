# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from flask import render_template, abort, request
from app.model.payment_item import PaymentItem
from app.model.ledger import Ledger
from app.model.user import auth_required

@app.route("/payment_items")
@auth_required
def items():
    items = PaymentItem.query_all()
    return render_template('payment_items.html', payment_items=items)

@app.route("/payment_item/<item_id>")
@auth_required
def buy_item(item_id=0):
    it = PaymentItem.find(item_id)
    user = request.user
    if not it or not user:
        abort(404)
        return

    user.balance += user.balance + it.money + it.charge
    user.save()

    ledger = Ledger()
    ledger.item_id = it.id
    ledger.name = it.name
    ledger.money = it.money + it.charge
    ledger.type = Ledger.Type.PAYMENT_MONEY
    ledger.uid = user.id
    ledger.save()

    return render_template('payment_buy_success.html', payment_item=it)
