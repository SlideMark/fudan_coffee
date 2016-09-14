# -*- coding: utf-8 -*-

__author__ = 'wills'

import hashlib
import logging
import time
import traceback
from app import conf
import urllib2
import json
from xml.etree import ElementTree
import random
from app.model.payment_item import PaymentItem
from app.model.payment_transaction import PaymentTransaction
from app.model.payment import Payment
from app.model.user import User
from app.util.weixin import WXClient

class Order(object):

    def __init__(self, uid, openid):
        self.uid = uid
        self.tid = 0
        self.nonce_str = ''
        self.body = ''
        self.out_trade_no = ''
        self.total_fee = ''
        self.spbill_create_ip = '115.28.160.193'
        self.notify_url = '%s/v2.0/payment/weixin/notify'
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
                self.uid, item_id, int(1000 * time.time()), random.randint(0, 1000))
            result = PaymentTransaction(uid=self.uid, out_trade_no=self.out_trade_no).save(return_keys=['id'])
            self.tid = result['id']
            self.body = self.detail = '自由而无用账号充值%s元,赠送%s元' % (item.money / 100.0, item.charge/100.0)
            self.attach = '%s-%s' % (self.uid, self.tid)
            if conf.debug:
                self.total_fee = 1
            else:
                self.total_fee = item.money

            return True

    def set_money(self, money):
        self.out_trade_no = '%s-%s-%s-%s' % (
            self.uid, 'money_%s'%money, int(1000 * time.time()), random.randint(0, 1000))
        result = PaymentTransaction(uid=self.uid, out_trade_no=self.out_trade_no).save(return_keys=['id'])
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
        for key, value in data.iteritems():weixin_params.append([str(key), str(value)])
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
             self.trade_type, self.openid.encode('utf8'), Order.sign(self.__dict__),
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
            if response.get('return_code') == 'SUCCESS':
                if response.get('result_code') == 'SUCCESS' and response.get('sign') == self.sign(response):
                    resp = {
                        'appId': self.appid,
                        'package': 'prepay_id=%s' % (response.get('prepay_id'), ),
                        'nonceStr': response.get('nonce_str'),
                        'signType':'MD5',
                        'timeStamp': str(int(time.time()))
                    }
                    resp['sign'] = self.sign(resp)
                    return resp
                else:
                    logging.error(data)
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
            if response.get('sign') == cls.sign(response):
                return cls.finish(response)
            logging.info('wx callback sign error %s:%s' % (response.get('sign'), cls.sign(response)))
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
                    'uid': uid,
                    'item_id': item_id,
                    'trade_no': data['transaction_id'],
                    'price': int(data['total_fee']),
                    'money': item.money + item.charge
                }
            else:
                money = int(flag)
                payment_info = {
                    'uid': uid,
                    'item_id': 'recharge_%s' % money,
                    'trade_no': data['transaction_id'],
                    'price': money,
                    'money': money
                }
        except:
            traceback.print_exc()
            return False

        logging.debug("finish: payment_info: %s" % payment_info)
        error = cls.finish_transaction(user, payment_info)

        t.close()

        if error:
            logging.error(error[1])
            return error[0]

        return Order.finish_web(uid, data)

    @classmethod
    def finish_transaction(cls, user, payment_info):
        user.balance += payment_info['money']
        user.save()

        Payment(uid=user.uid, item_id=payment_info['item_id'],
                num=1, money=payment_info['price']).save()

    @classmethod
    def finish_web(cls, uid, data):
        openid = data.get('openid')
        token = WXClient.get_service_token()

        template = {
            'touser':openid,
            'template_id':'UTac8ANDkVkSQ9CAhiH-BBwxBkikPrqbYavKBXX8bMk',
            'data':{
                'first':{
                    'value':'恭喜你购买成功！',
                },
                'accountType':{
                    'value':'ID',
                },
                'account':{
                    'value':str(uid),
                },
                'amount':{
                    'value': str(int(data['total_fee']) / 100.0)+'元',
                },
                'result':{
                    'value':'充值成功',
                },
                'remark':{
                    'value':'如有疑问，请联系客服人员。',
                }
            }
        }

        try:
            url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % (token, )
            request = urllib2.Request(url, json.dumps(template))
            data = urllib2.urlopen(request, timeout=5).read()
            data2 = json.loads(data)
            if data2.get('msgid'):return True
        except:
            traceback.print_exc()
            return False

        return True
