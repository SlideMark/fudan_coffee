# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app
from app.model.event import Event
from flask import request, render_template
from app.controller import auth_required
from app.model.shop import Shop
from app.model.product import Product

@app.route("/products")
def products():
    shop_id = request.args.get('shop_id', Shop.GEHUA)
    products = Product.query(fetchone=False, shop_id=shop_id) or []
    return render_template('products.html', products=products)

@app.route("/product/<product_id>", methods=['GET'])
def product(product_id=0):
    product = Product.find(product_id)
    return render_template('product.html', product=product)

@app.route("/product/<product_id>", methods=['POST'])
def buy_product(product_id=0):
    product = Product.find(product_id)

    return render_template('product.html', product=product)
