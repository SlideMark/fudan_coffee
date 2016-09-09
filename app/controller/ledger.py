# -*- coding: utf-8 -*-

__author__ = 'wills'

from flask import render_template,request
from app import app
from app.model.ledger import Ledger
from app.model.product import Product

@app.route("/ledgers")
def ledgers():
    type = request.args.get('type', 0)
    uid = 1
    ledgers = Ledger.query(fetchone=False, uid=uid, type=type)
    for each in ledgers:
        each['product_name'] = Product.find(each['product_id']).name
    return render_template('ledgers.html', ledgers=ledgers)
