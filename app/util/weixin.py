# -*- coding: utf-8 -*-

__author__ = 'wills'

import logging
from app import conf
from app.util.httputil import request_with_params
from app.core.cache import LocalCache

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

    @staticmethod
    def get_service_user(next_openid):
        access_token = WXClient.get_service_token()
        profile_url = 'https://api.weixin.qq.com/cgi-bin/user/get'
        kwargs = {
            'access_token': access_token,
        }
        if next_openid:kwargs['next_openid'] = next_openid

        profile = request_with_params(profile_url, **kwargs)

        return profile

    @staticmethod
    def get_service_user_info(openid):
        fwh_token = WXClient.get_service_token()
        if not fwh_token:return None

        wx_user = WXClient.get_wx_info(openid, fwh_token)
        if wx_user and wx_user.get('errcode') == 40001:
            fwh_token = WXClient.get_service_token()
            if not fwh_token:return None
            wx_user = WXClient.get_wx_info(openid, fwh_token)

        if not wx_user or wx_user.get('errcode'):
            return None

        return wx_user

