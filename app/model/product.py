# -*- coding: utf-8 -*-

__author__ = 'wills'

from app.core.dao import DAO

class Product(DAO):

    TABLE = 'fc_product'
    COLUMNS = ['id', 'name', 'description', 'icon', 'shop_id', 'price', 'create_at', 'update_at']
