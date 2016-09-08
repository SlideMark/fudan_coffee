# -*- coding: utf-8 -*-

__author__ = 'wills'

import yaml
import os

class Config(object):

    def __init__(self):
        conf = yaml.load(open(os.getenv("HOME") + '/.fudan_coffee.yaml'))
        self.db_uri = conf.get('db')
        self.wechat_app_id = conf.get('wechat_app_id')
        self.wechat_secret = conf.get('wechat_secret')
