# -*- coding: utf-8 -*-

__author__ = 'wills'

from app import app, conf
from app.model.cart import Cart
from app.model.product import Product
from app.core.response import Response, ResponseCode


if conf.debug:
    @app.route("/test")
    def test():
        product_id = 2
        if not product_id or not Product.find(product_id):
            return str(Response(code=ResponseCode.DATA_NOT_EXIST, msg='商品不存在'))

        cart = Cart()
        cart.uid = 1
        cart.product_id = product_id
        rt = cart.save(return_keys=[Cart.PKEY])
        print rt

        return str(Response())
