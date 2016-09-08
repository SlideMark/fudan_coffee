# -*- coding: utf-8 -*-

__author__ = 'wills'

from datetime import date
from datetime import datetime
import time

format_str = '%Y-%m-%d %H:%M:%S'

# dt is short for datetime

def dt_to_str(dt):
    if not isinstance(dt, (datetime, date)):
        return
    try:
        return dt.strftime(format_str)
    except:
        pass

def str_to_dt(dt_str):
    if not dt_str:
        return
    if isinstance(dt_str, datetime):
        return dt_str
    elif isinstance(dt_str, date):
        return datetime(dt_str.year, dt_str.month, dt_str.day)
    try:
        return datetime.strptime(dt_str, format_str)
    except:
        pass

def dt_str_to_dt(dt_str):
    if not dt_str:
        return
    try:
        return datetime.strptime(dt_str, '%Y-%m-%d')
    except:
        pass

def timestamp_to_dt(timestamp):
    return datetime.fromtimestamp(timestamp)


def timestamp_to_str(timstamp):
    return time.strftime(format_str, time.localtime(timstamp))


def str_to_timestamp(dt_str):
    return time.mktime(datetime.strptime(dt_str, format_str).timetuple())
