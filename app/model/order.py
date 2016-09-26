# -*- coding: utf-8 -*-

__author__ = 'wills'

import hashlib
import logging
import time
import traceback
from app import conf
import urllib2
from xml.etree import ElementTree
from app.model.user import User
from app.util.weixin import WXClient
from app.model.cart import Cart
from datetime import datetime
import random
from app.core.dao import DAO

class Order(DAO):

    TABLE = 'fc_payment'
    COLUMNS = ['id', 'order_id', 'uid', 'name', 'money',
               'balance', 'coupon', 'item_id', 'type',
               'state', 'extra', 'create_at', 'update_at']

    class State:
        NORMAL = 0
        FINISHED = 1
        CANCELED = 2

    class Type:
        CHARGE = 0
        PAY = 1

    def set_order_id(self):
        self.order_id = '%s%s' % (datetime.now().strftime('%Y%m%d%H%M%S'), random.randint(1000,9999))

    def close(self):
        self.state = Order.State.FINISHED
        self.save()

class WXOrder(object):

    def __init__(self, user, order):
        self.uid = user.id
        self.nonce_str = ''
        self.out_trade_no = order.order_id
        self.spbill_create_ip = conf.ip
        self.notify_url = '%s/payment_notify' % conf.domain
        self.trade_type = ''
        self.attach = '%s' % (user.id)
        self.openid = user.openid
        self.trade_type = 'JSAPI'
        self.appid = conf.wechat_fwh_appid
        self.mch_id = conf.wechat_fwh_mchid
        self.body = self.detail = order.name
        if conf.debug:
            self.total_fee = 1
        else:
            self.total_fee = abs(order.money)

    @classmethod
    def sign(self, data):
        weixin_params = []
        for key, value in data.iteritems():
            if key not in ['uid','sign']:
                weixin_params.append([str(key), str(value)])
        weixin_params.sort(key=lambda x:x[0])
        sign_src = '%s&key=%s' % ('&'.join(['%s=%s'%(x[0], x[1]) for x in weixin_params]), conf.wechat_fwh_mchkey)
        logging.info(sign_src)
        return hashlib.md5(sign_src).hexdigest().upper()

    def order(self):
        self.nonce_str = hashlib.md5('%s-%s' % (self.uid, time.time())).hexdigest()
        return '''<xml>
   <appid>%s</appid>
   <attach>%s</attach>
   <body>%s</body>
   <detail>%s</detail>
   <mch_id>%s</mch_id>
   <nonce_str>%s</nonce_str>
   <notify_url>%s</notify_url>
   <out_trade_no>%s</out_trade_no>
   <spbill_create_ip>%s</spbill_create_ip>
   <total_fee>%s</total_fee>
   <trade_type>%s</trade_type>
   <openid>%s</openid>
   <sign>%s</sign>
</xml>''' % (self.appid, self.attach, self.body, self.detail,
             self.mch_id, self.nonce_str, self.notify_url,
             self.out_trade_no, self.spbill_create_ip, self.total_fee,
             self.trade_type, self.openid.encode('utf8'),
             WXOrder.sign(self.__dict__)
    )

    def get_token(self):
        try:
            order = self.order()
            request = urllib2.Request(
                '%s' % 'https://api.mch.weixin.qq.com/pay/unifiedorder', order)
            data = urllib2.urlopen(request, timeout=5).read()
            root = ElementTree.fromstring(data)
            response = {child.tag: child.text for child in root.getchildren()}
            print response
            if response.get('return_code') == 'SUCCESS' and response.get('result_code') == 'SUCCESS':
                resp = {
                    'appId': self.appid,
                    'package': 'prepay_id=%s' % (response.get('prepay_id'), ),
                    'nonceStr': response.get('nonce_str'),
                    'signType':'MD5',
                    'timeStamp': str(int(time.time()))
                }
                resp['sign'] = self.sign(resp)
                resp['order_id'] = self.out_trade_no
                return resp
            else:
                logging.error(data)

            return
        except:
            traceback.print_exc()
            return

    @classmethod
    def notify(cls, data):
        try:
            logging.debug("notify: data: %s" % data)
            root = ElementTree.fromstring(data)
            response = {child.tag: child.text for child in root.getchildren()}
            logging.error('wx callback sign error %s:%s' % (response.get('sign'), cls.sign(response)))

            if response.get('sign') == cls.sign(response):
                return cls.finish(response)
        except:
            traceback.print_exc()

    @classmethod
    def finish(cls, data):
        logging.debug("finish: %s" % data)
        if data.get('return_code') != 'SUCCESS' or not data.get('attach'):
            return False

        order_id = data['out_trade_no']
        order = Order.query_instance(order_id=order_id)
        if not order or order.state != Order.State.NORMAL:
            return False

        payment_info = {
            'openid': data.get('openid'),
            'money': int(data['total_fee']),
        }
        user = User.find(order.uid)
        if order.type == Order.Type.CHARGE:
            user.balance += order.balance
        else:
            if order.balance:
                pay = min(order.balance, user.banalce)
                user.balance -= pay
            if order.coupon:
                pay = min(order.coupon, user.coupon)
                user.coupon -= pay

            carts = Cart.query(fetchone=False, uid=user.id, state=Cart.State.INIT)
            for each in carts:
                cart = Cart(**each)
                cart.state = Cart.State.FINISHED
                cart.save()

        user.save()
        order.close()
        WXClient.send_buy_success_msg(payment_info)
        return True
