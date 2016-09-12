# -*- coding: utf-8 -*-

__author__ = 'wills'

from flask import render_template,request
from app import app
from app.model.ledger import Ledger

@app.route("/user/<uid>/ledgers")
def ledgers(uid=0):
    type = request.args.get('type', 0)
    type = int(type)
    if type == 0:
        ledgers = Ledger.query(fetchone=False, uid=uid,
                               extra={'type in': (Ledger.Type.BUY_USE_BALANCE, Ledger.Type.PAYMENT_MONEY)})
    elif type == 1:
        ledgers = Ledger.query(fetchone=False, uid=uid,
                               extra={'type in': (Ledger.Type.BUY_USE_COUPON, Ledger.Type.TRANSFER_COUPON)})
    else:
        ledgers = []
    print ledgers
    return render_template('ledgers.html', ledgers=ledgers)
