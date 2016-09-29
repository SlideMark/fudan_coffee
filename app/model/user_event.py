# -*- coding: utf-8 -*-

__author__ = 'wills'

from app.core.dao import DAO

class UserEvent(DAO):

    TABLE = 'fc_user_event'
    COLUMNS = ['id', 'uid', 'event_id', 'state', 'create_at', 'update_at']

    class State:
        INIT = 0
        CANCELED = 1
