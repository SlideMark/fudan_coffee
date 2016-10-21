# -*- coding: utf-8 -*-
import logging
import traceback
from app import conf
from qiniu import Auth, put_data

__author__ = 'wills'


class QiniuCloud(object):

    INSTANCE = None

    @classmethod
    def  get_token(cls, key, bucket):
        if not cls.INSTANCE:
            cls.INSTANCE = Auth(conf.qiniu_key, conf.qiniu_secret)

        return cls.INSTANCE.upload_token(bucket, key, 3600)

    @classmethod
    def upload_file(cls, data, key, bucket, timeout=5):
        token = cls.get_token(key, bucket)
        if not cls.INSTANCE:
            cls.INSTANCE = Auth(conf.qiniu_key, conf.qiniu_secret)
        try:
            ret, info = put_data(token, key, data)
        except:
            logging.error('UPLOAD failed.\n%s' % ( traceback.format_exc()))
