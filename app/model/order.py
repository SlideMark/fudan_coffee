# -*- coding: utf-8 -*-

__author__ = 'wills'

import hashlib
import logging
import time
import traceback
from app import conf
import urllib2
from xml.etree import ElementTree
import random
from app.model.payment_item import PaymentItem
from app.model.payment_transaction import PaymentTransaction
from app.model.payment import Payment
from app.model.ledger import Ledger
from app.model.user import User
from app.util.weixin import WXClient
from app.model.cart import Cart

class Order(object):

    def __init__(self, uid, openid):
        self.uid = uid
        self.tid = 0
        self.nonce_str = ''
        self.body = ''
        self.out_trade_no = ''
        self.total_fee = ''
        self.spbill_create_ip = conf.ip
        self.notify_url = '%s/payment_notify' % conf.domain
        self.trade_type = ''
        self.attach = ''
        self.openid = openid
        self.trade_type = 'JSAPI'
        self.appid = conf.wechat_fwh_appid
        self.mch_id = conf.wechat_fwh_mchid

    def set_item(self, item_id):
        item = PaymentItem.find(item_id)
        if not item:
            return False
        else:
            self.out_trade_no = '%s-%s-%s-%s' % (
                self.uid, item.id, int(1000 * time.time()), random.randint(0, 1000))
            result = PaymentTransaction(uid=self.uid, out_trade_no=self.out_trade_no).save(return_keys=['id'])
            self.tid = result['id']
            self.body = self.detail = '自由而无用账号充值%s元,赠送%s元' % (item.money / 100.0, item.charge/100.0)
            self.attach = '%s-%s' % (self.uid, self.tid)
            if conf.debug:
                self.total_fee = 1
            else:
                self.total_fee = item.money

            return True

    def set_money(self, money, balance=0, coupon=0, from_cart=0):
        self.out_trade_no = '%s-%s-%s-%s' % (
            self.uid, money, int(1000 * time.time()), random.randint(0, 1000))
        result = PaymentTransaction(uid=self.uid, out_trade_no=self.out_trade_no,
                                    balance=balance, coupon=coupon,
                                    type=PaymentTransaction.Type.BY_DIRECTLY,
                                    from_cart=from_cart).save(return_keys=['id'])
        self.tid = result['id']
        self.body = self.detail = '自由而无用消费%s元' % (money / 100.0)
        self.attach = '%s-%s' % (self.uid, self.tid)
        if conf.debug:
            self.total_fee = 1
        else:
            self.total_fee = money

        return True

    @classmethod
    def sign(self, data):
        weixin_params = []
        for key, value in data.iteritems():
            if key not in ['uid','tid', 'sign']:
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
             Order.sign(self.__dict__)
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
                resp['id'] = self.tid
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

        # check transaction
        attachs = data.get('attach').split('-')
        tid = int(attachs[1])
        t = PaymentTransaction.find(tid)
        if not t or t.state != PaymentTransaction.State.NORMAL:
            return False

        try:
            out_trade_no = data['out_trade_no']
            parts = out_trade_no.split('-')
            uid, flag = int(parts[0]), parts[1]
            user = User.find(uid)
            if not user:
                return False

            if t.type == PaymentTransaction.Type.BY_PAYMENT_ITEM:
                item_id = int(flag)
                item = PaymentItem.find(item_id)
                payment_info = {
                    'openid': data.get('openid'),
                    'uid': uid,
                    'item_id': item_id,
                    'trade_no': data['transaction_id'],
                    'price': int(data['total_fee']),
                    'money': item.money + item.charge,
                    'item_name': '账户充值%s元, 返现%s元' % (item.money/100.0, item.charge/100.0)
                }
                user.balance += payment_info['money']
                user.save()
                Ledger(uid=user.id, name='账户充值', money=payment_info['money'],
                       type=Ledger.Type.PAYMENT_CHARGE, item_id=item_id).save()
            else:
                money = int(flag)
                payment_info = {
                    'openid': data.get('openid'),
                    'uid': uid,
                    'item_id': 'recharge_%s' % money,
                    'trade_no': data['transaction_id'],
                    'price': money,
                    'money': money,
                    'item_name': '购买咖啡消费%s元' % (money/100.0)
                }
                if t.balance:
                    pay = max(t.balance, user.banalce)
                    Ledger(uid=user.id, name='购买咖啡消费', money=pay,
                       type=Ledger.Type.BUY_USE_BALANCE).save()
                    user.balance -= pay
                if t.coupon:
                    pay = max(t.coupon, user.coupon)
                    Ledger(uid=user.id, name='购买咖啡消费', money=pay,
                       type=Ledger.Type.BUY_USE_COUPON).save()
                    user.balance -= pay

                if t.from_cart:
                    carts = Cart.query(fetchone=False, uid=user.id, state=Cart.State.INIT)
                    for each in carts:
                        cart = Cart(**each)
                        cart.state = Cart.State.FINISHED
                        cart.save()

                user.save()

            Payment(uid=user.id, item_id=payment_info['item_id'],
                    num=1, money=payment_info['price']).save()
        except:
            traceback.print_exc()
            return False

        t.close()

        WXClient.send_buy_success_msg(user, payment_info)
        return True
