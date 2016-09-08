# -*- coding: utf-8 -*-

__author__ = 'wills'

import time

class LocalCache(object):

    CACHES = {}

    @classmethod
    def get(cls, key, without_expire=False):
        info = cls.CACHES.get(key)
        if not info or not info.get('expire_at'):
            return None
        else:
            if without_expire:
                return info.get('value')
            
            expire_at = info.get('expire_at')
            if time.time() < expire_at:
                return info.get('value')
            return None

    @classmethod
    def get_expire_time(cls, key):
        info = cls.CACHES.get(key)
        if not info:
            return None
        return info.get('expire_at')

    @classmethod
    def set(cls, key, value, expire_time=600):
        cls.CACHES[key] = {
            'value': value,
            'expire_at': time.time() + expire_time
        }
