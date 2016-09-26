# -*- coding: utf-8 -*-

__author__ = 'wills'

import logging
import json
from app import conf
from app.util.httputil import request_with_params, request_with_data
from app.core.cache import LocalCache
from app.util.timeutil import dt_to_str
from datetime import datetime


class WXClient(object):

    TOKEN_REDIS = 'wechat_token'
    @staticmethod
    def get_wx_token(appid, app_secret, code):
        api_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        kwargs = {
            'appid': appid,
            'secret': app_secret,
            'code': code,
            'grant_type':'authorization_code'
        }
        token = request_with_params(api_url, **kwargs)
        return token

    @staticmethod
    def get_wx_info(openid, access_token, lang='zh_CN'):
        api_url = 'https://api.weixin.qq.com/cgi-bin/user/info'
        kwargs = {
            'access_token':access_token,
            'openid':openid,
            'lang':lang,
        }

        info = request_with_params(api_url, **kwargs)
        return info

    @staticmethod
    def get_wx_profile(openid, access_token):
        profile_url = 'https://api.weixin.qq.com/sns/userinfo'
        kwargs = {
            'openid': openid,
            'access_token': access_token
        }
        profile = request_with_params(profile_url, **kwargs)
        if profile:
            profile['access_token'] = access_token
        return profile

    @staticmethod
    def get_js_token(appid, app_secret):
        profile_url = 'https://api.weixin.qq.com/cgi-bin/token'
        kwargs = {
            'grant_type': 'client_credential',
            'appid': appid,
            'secret': app_secret
        }
        profile = request_with_params(profile_url, **kwargs)
        logging.debug('get_js_token appid:%s app_secret:%s profile:%s' %
                      (appid, app_secret, profile))
        return profile

    @staticmethod
    def get_js_ticket(access_token):
        profile_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket'
        kwargs = {
            'access_token': access_token,
            'type': 'jsapi'
        }
        profile = request_with_params(profile_url, **kwargs)
        return profile

    @staticmethod
    def get_service_token():
        token = LocalCache.get(WXClient.TOKEN_REDIS)

        if not token:
            token_info = WXClient.get_js_token(conf.wechat_app_id, conf.wechat_secret)
            if not token_info:return None

            token = token_info.get('access_token')
            LocalCache.set(WXClient.TOKEN_REDIS, token, expire_time=3600)

        return token


    '''
    您好，您已消费成功。

    消费金额：{{pay.DATA}}
    消费地址：{{address.DATA}}
    消费时间：{{time.DATA}}
    {{remark.DATA}}

    {{first.DATA}}
    会员姓名：{{name.DATA}}
    消费内容：{{itemName.DATA}}
    消费金额：{{itemMoney.}}
    消费时间：{{time.DATA}}
    {{remark.DATA}}
    '''
    @staticmethod
    def send_buy_success_msg(user, data):
        openid = data.get('openid')
        token = WXClient.get_service_token()

        template = {
            'touser':openid,
            'template_id': conf.wechat_template_id,
            'data':{
                'address':{
                    'value': '自由而无用咖啡店',
                },
                'pay':{
                    'value':'%s元' % str(data['price']/100.0),
                },
                'time': {
                    'value': dt_to_str(datetime.now())
                },
                'remark':{
                    'value':'如有疑问，请联系咖啡店店员。',
                }
            }
        }

        resp = request_with_data('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % (token, ),
                          json.dumps(template))
        if resp and resp.get('msgid'):return True
        return False


    @staticmethod
    def send_signup_msg(user, data):
        openid = data.get('openid')
        token = WXClient.get_service_token()

        template = {
            'touser':openid,
            'template_id': 'iOKEU3_7migQusQ6jU3mDlTkklB5d7VdpfQvY5g5ddw',
            'data':{}
        }

        resp = request_with_data('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % (token, ),
                          json.dumps(template))
        if resp and resp.get('msgid'):return True
        return False
