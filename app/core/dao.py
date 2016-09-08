# -*- coding: utf-8 -*-

__author__ = 'wills'

from datetime import datetime
from datetime import date
from decimal import Decimal
from collections import defaultdict
import psycopg2.extras
import traceback
import logging
import psycopg2
from app import conf
from app.util.timeutil import dt_to_str

class Connection(object):

    def __init__(self, db):
        self.conn = psycopg2.connect(db)
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def run_query_fetch_one(self, query, *args):
        self.cursor.execute(query, *args)
        return self.cursor.fetchone()

    def run_query(self, query, *args):
        self.cursor.execute(query, *args)
        return self.cursor.fetchall()

    def run_operation(self, query, *args):
        self.cursor.execute(query, *args)
        self.conn.commit()

class Postgres(object):

    master = Connection(conf.db_uri)
    slave = Connection(conf.db_uri)

class DAO(object):

    TABLE = ''
    PKEY = 'id'

    COLUMNS = []
    INCR_FIELDS = []

    def __init__(self, **kwargs):
        self._updated_keys = set()
        self._db_incr_values = defaultdict(lambda: 0)
        if not kwargs:
            return

        for field in kwargs.keys():
            setattr(self, field, kwargs.get(field))
        self._updated_keys.clear()
        self._db_incr_values.clear()

    def __setattr__(self, key, value):
        if hasattr(getattr(self.__class__, key, None), '__set__'):
            object.__setattr__(self, key, value)
            return

        old_value = 0
        if key in self.__dict__:
            old_value = self.__dict__[key]
            if value == old_value:
                return

        self.__dict__[key] = value
        if key in self.COLUMNS:
            self._updated_keys.add(key)

        # modified increase field
        if key in self.INCR_FIELDS:
            self._db_incr_values[key] += (value - old_value)

    @classmethod
    def find_or_new(cls, uid, **kwargs):
        obj = cls.find(uid)
        if not obj:
            obj = cls()
            setattr(obj, obj.PKEY, uid)
            if kwargs:
                for field in kwargs.keys():
                    setattr(obj, field, kwargs.get(field))
        return obj

    @classmethod
    def find(cls, value, columns=None):
        if columns:
            fields = ','.join(columns)
        else:
            fields = '*'

        query = 'select %s from %s where %s = %%s' % (fields, cls.TABLE, cls.PKEY)
        result = Postgres.master.run_query_fetch_one(query, (value, ))

        if result:
            return cls(**result)

        return None

    @classmethod
    def finds(cls, values, master=False, columns=None, order_by=None):
        if columns:
            fields = ','.join(columns)
        else:
            fields = '*'

        if order_by:
            query = 'select %s from %s where %s in %%s order by %s' % (
                fields, cls.TABLE, cls.PKEY, order_by)
        else:
            query = 'select * from %s where %s in %%s' % (cls.TABLE, cls.PKEY)

        if master:
            adapter = Postgres.master
        else:
            adapter = Postgres.slave

        results = adapter.run_query(query, (tuple(values), ))

        r_result = {}
        if results:
            for result in results:
                r_result[result[cls.PKEY]] = cls(**result)

        return r_result

    @classmethod
    def query_instance(cls, master=False, columns=None, extra=None, **kwargs):
        conditions = []
        values = []

        for field, value in kwargs.iteritems():
            conditions.append('%s=%%s' % field)
            values.append(value)

        if extra:
            for key, value in extra.iteritems():
                conditions.append('%s %%s' % key)
                values.append(value)

        if columns:
            fields = ','.join(columns)
        else:
            fields = '*'

        query = 'SELECT %s FROM %s WHERE %s' % (
            fields, cls.TABLE, cls.get_filter(conditions))

        if master:
            adapter = Postgres.master
        else:
            adapter = Postgres.slave

        result = adapter.run_query_fetch_one(query, values)

        if result:
            return cls(**result)

    @classmethod
    def query(cls, master=False, columns=None, fetchone=True, orderby=None,
              extra=None, limit=0, offset=0, **kwargs):
        conditions = []
        values = []

        for field, value in kwargs.iteritems():
            conditions.append('%s=%%s' % field)
            values.append(value)

        if extra:
            for key, value in extra.iteritems():
                conditions.append('%s %%s' % key)
                values.append(value)

        if columns:
            fields = ','.join(columns)
        else:
            fields = '*'

        query = 'SELECT %s FROM %s WHERE %s' % (
            fields, cls.TABLE, cls.get_filter(conditions))

        if orderby:
            query = '%s ORDER BY %s' % (query, orderby)
        if limit:
            query = '%s LIMIT %s' % (query, limit)
        if offset:
            query = '%s OFFSET %s' % (query, offset)

        if fetchone:
            if master:
                func = Postgres.master.run_query_fetch_one
            else:
                func = Postgres.slave.run_query_fetch_one
        else:
            if master:
                func = Postgres.master.run_query
            else:
                func = Postgres.slave.run_query

        return func(query, values)


    @classmethod
    def query_all(cls, master=False, columns=None, orderby=None, **kwargs):
        values = []
        if columns:
            fields = ','.join(columns)
        else:
            fields = '*'

        query = 'SELECT %s FROM %s' % (fields, cls.TABLE)

        if master:
            adapter = Postgres.master
        else:
            adapter = Postgres.slave

        if orderby:
            query = '%s ORDER BY %s' % (query, orderby)

        return adapter.run_query(query, values)


    @classmethod
    def count(cls, count_key='1', master=False, extra=None, **kwargs):
        conditions = []
        values = []
        for field, value in kwargs.iteritems():
            conditions.append('%s=%%s' % field)
            values.append(value)
        if extra:
            for key, value in extra.iteritems():
                if value is None:
                    conditions.append('%s' % key)
                else:
                    conditions.append('%s %%s' % key)
                    values.append(value)
        if conditions:
            query = 'SELECT count(%s) FROM %s WHERE %s' % (count_key,
                cls.TABLE, cls.get_filter(conditions))
        else:
            query = 'SELECT count(%s) FROM %s ' % (count_key, cls.TABLE)
        if master:
            adapter = Postgres.master
        else:
            adapter = Postgres.slave

        result = adapter.run_query_fetch_one(query, values)
        if result:
            return result['count']

        return 0

    @classmethod
    def sum(cls, column, master=False, extra=None, **kwargs):
        conditions = []
        values = []
        for field, value in kwargs.iteritems():
            conditions.append('%s=%%s' % field)
            values.append(value)
        if extra:
            for key, value in extra.iteritems():
                if value is None:
                    conditions.append('%s' % key)
                else:
                    conditions.append('%s %%s' % key)
                    values.append(value)
        if conditions:
            query = 'SELECT sum(%s) as sum FROM %s WHERE %s' % (column,
                cls.TABLE, cls.get_filter(conditions))
        else:
            query = 'SELECT sum(%s) as sum FROM %s ' % (column, cls.TABLE)
        if master:
            adapter = Postgres.master
        else:
            adapter = Postgres.slave


        result = adapter.run_query_fetch_one(query, values)
        return result['sum'] if result['sum'] else 0

    def save(self, extra=None, return_keys=None):
        try:
            _fields = []
            _values = []
            if not self.is_new():
                if not self._updated_keys:
                    return 0
                for field in self._updated_keys:
                    if field in self.INCR_FIELDS:
                        _fields.append('%s = %s + (%%s)' % (field, field))
                        _values.append(self._db_incr_values[field])
                    elif field in self.COLUMNS:
                        _fields.append('%s = %%s' % field)
                        _values.append(getattr(self, field))

                update_string = ', '.join(_fields)

                where_conditions = ['%s = %%s' % self.PKEY]
                _values.append(getattr(self, self.PKEY))
                if extra:
                    for key, value in extra.iteritems():
                        where_conditions.append('%s %%s' % key)
                        _values.append(value)

                if return_keys:
                    sql_str = 'update %s set %s where %s returning %s' % (
                        self.TABLE, update_string, self.get_filter(where_conditions), ','.join(return_keys))
                else:
                    sql_str = 'update %s set %s where %s' % (
                        self.TABLE, update_string, self.get_filter(where_conditions))

                if return_keys:
                    return Postgres.master.run_query_fetch_one(sql_str, _values)
                else:
                    return Postgres.master.run_operation(sql_str, _values)

            _placeholders = []
            for field in self.COLUMNS:
                if getattr(self, field, None) is not None:
                    _values.append(getattr(self, field))
                    _fields.append(field)
                    _placeholders.append('%s')

            if _fields:
                sql_str = 'INSERT INTO %s (%s) VALUES (%s)' % (
                    self.TABLE, ', '.join(_fields), ', '.join(_placeholders))

                if return_keys:
                    sql_str = sql_str + ' returning %s' % ','.join(return_keys)
                logging.debug('sql:%s values:%s' % (sql_str, _values))
                if return_keys:
                    return Postgres.master.run_query_fetch_one(sql_str, _values)
                else:
                    return Postgres.master.run_operation(sql_str, _values)
            return

        except Exception, e:
            if e.message.find('duplicate key') == -1:
                traceback.print_exc()
                
        self._updated_keys.clear()
        self._db_incr_values = defaultdict(lambda: 0)

    def destroy(self):
        if self.is_new():
            return

        sql = 'delete from %s where %s=%%s' % (self.TABLE, self.PKEY)
        return Postgres.master.run_operation(sql, [getattr(self, self.PKEY)])

    @classmethod
    def delete(cls, **kwargs):
        conditions = []
        values = []
        for field, value in kwargs.iteritems():
            conditions.append('%s=%%s' % field)
            values.append(value)
        if conditions:
            query = 'DELETE FROM %s WHERE %s' % (
                cls.TABLE, cls.get_filter(conditions))
            return Postgres.master.run_operation(query, values)
        else:
            return 0

    @classmethod
    def incr(cls, id, key, by=1):
        sql = 'update %s set %s=%s+%%s where %s=%%s' % (cls.TABLE, key, key, cls.PKEY)
        return Postgres.master.run_operation(sql, (by, id))

    def to_dict(self, fields=None, no_none=False):
        kwargs = {}
        if not fields:
            fields = self.COLUMNS
        for field in fields:
            value = getattr(self, field, None)
            if value is None and no_none:
                value = ''

            if isinstance(value, (datetime, date)):
                kwargs[field] = dt_to_str(value)
            elif isinstance(value, Decimal):
                kwargs[field] = float(value)
            else:
                kwargs[field] = value

        return kwargs

    def is_new(self):
        return not ((getattr(self, self.PKEY, None) and (self.PKEY not in self._updated_keys)))

    @classmethod
    def get_filter(cls, conditions):
        return ' AND '.join(conditions) if conditions else ' 1=1 '

    def get_id(self):
        return getattr(self, self.PKEY, None)
