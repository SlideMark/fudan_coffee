# -*- coding: utf-8 -*-

__author__ = 'wills'

import yaml
import os

class Config(object):

    def __init__(self):
        conf = yaml.load(open(os.getenv("HOME") + '/.fudan_coffee.yaml'))
        self.domain = conf.get('domain')
        self.port = conf.get('port') or 5000
        self.ip = conf.get('ip')
        self.db_uri = conf.get('db')
        self.wechat_app_id = conf.get('wechat_app_id')
        self.wechat_secret = conf.get('wechat_secret')
        self.debug = True if conf.get('env') == 'debug' else False
        self.wechat_fwh_appid = conf.get('wechat_fwh_appid')
        self.wechat_fwh_mchid = conf.get('wechat_fwh_mchid')
        self.wechat_fwh_mchkey = conf.get('wechat_fwh_mchkey')
        self.salt = conf.get('salt')
        self.wechat_template_id = conf.get('wechat_template_id')
