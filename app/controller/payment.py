# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from flask import render_template, abort
from app.model.payment_item import PaymentItem
from app.model.user import User
from app.model.ledger import Ledger

@app.route("/payment_items")
def items():
    items = PaymentItem.query_all()
    return render_template('payment_items.html', payment_items=items)

@app.route("/payment_item/<item_id>")
def buy_item(item_id=0):
    it = PaymentItem.find(item_id)
    user = User.find(1)
    if not it or not user:
        abort(404)
        return

    user.balance += it.money
    user.charge += it.charge
    user.save()

    ledger = Ledger()
    ledger.item_id = it.id
    ledger.name = it.name
    ledger.money = it.money
    ledger.type = Ledger.Type.PAYMENT_MONEY
    ledger.uid = 1
    ledger.save()

    ledger2 = Ledger()
    ledger2.name = it.name
    ledger2.money = it.charge
    ledger2.uid = 1
    ledger2.item_id = it.id
    ledger2.type = Ledger.Type.PAYMENT_CHARGE
    ledger2.save()

    return render_template('payment_buy_success.html', payment_item=it)
