# -*- coding: utf-8 -*-

__author__ = 'wills'

from flask import request
from app import app
from app.model.user import auth_required
from app.model.ledger import Ledger
from app.core.response import Response

@app.route("/ledgers")
@auth_required
def ledgers():
    user = request.user
    type = request.args.get('type', 0)
    type = int(type)
    if type == 0:
        ledgers = Ledger.query(fetchone=False, uid=user.id,
                               extra={'type in': (Ledger.Type.BUY_USE_BALANCE, Ledger.Type.PAYMENT_MONEY)})
    elif type == 1:
        ledgers = Ledger.query(fetchone=False, uid=user.id,
                               extra={'type in': (Ledger.Type.BUY_USE_COUPON, Ledger.Type.TRANSFER_COUPON)})
    else:
        ledgers = []

    return str(Response(data=[Ledger(**each).to_dict() for each in ledgers]))
