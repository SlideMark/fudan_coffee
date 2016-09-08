# -*- coding: utf-8 -*-

__author__ = 'wills'

import logging
import json
import traceback
import urllib
import urllib2

def request_with_data(api_url, data, timeout=5):
    try:
        request = urllib2.Request(api_url, data)
        resp_data = urllib2.urlopen(request, timeout=timeout).read()
        return json.loads(resp_data)
    except Exception, e:
        logging.info('%s. POST %s with %s' % (e, api_url, data))


def request_with_params(api_url, method='GET', timeout=5, **kwargs):
    try:
        query = urllib.urlencode(kwargs)
        if method == 'GET':
            request = urllib2.Request('%s?%s' % (api_url, query))
        else:
            request = urllib2.Request(api_url, query)
        data = urllib2.urlopen(request, timeout=timeout).read()
        logging.debug('%s?%s' % (api_url, query))
        return json.loads(data)
    except Exception, e:
        logging.info('%s. %s %s with %s' % (e, method, api_url, kwargs))


def urlopen(url, timeout=5):
    try:
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)')
        response = urllib2.urlopen(request, timeout=timeout)
        data = response.read()
        return data
    except:
        logging.error('ulropen error!url:%s %s' % (url, traceback.format_exc()))
