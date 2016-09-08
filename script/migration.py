# -*- coding: utf-8 -*-

__author__ = 'wills'

import sys
import os
import traceback

sys.path.append("..")
import sys
import getopt
import psycopg2
import psycopg2.extras
import Queue
import yaml


def check_version():
    if sys.version_info[:2] != (2, 7):
        print '当前版本不是python2.7版本，请切换至2.7的虚拟环境运行!!'
        sys.exit(1)


def hashopts(pattern):
    try:
        opts, args = getopt.getopt(sys.argv[1:], pattern)
        myopts = {}
        for key, value in opts:
            myopts[key] = value or True
        return myopts
    except Exception:
        usage()


def usage():
    print '''
Description: 数据库迁移

Usage:
    python %s [options]

OPTIONS:
   -h    查看帮助文档
   -p    端口

''' % __file__
    sys.exit(1)


conf = yaml.load(open(os.getenv("HOME") + '/.fudan_coffee.yaml'))
SQLDB_DSN = conf.get('db')
MIGRATION_PATH = 'migration'


def candicates():
    migrations = Queue.PriorityQueue()
    files = os.listdir(MIGRATION_PATH)
    for each in files:
        seq = each.split('_')[0]
        try:
            seq = int(seq)
            migrations.put((seq, each))
        except:
            pass

    return migrations


def init_db(conn, cur):
    cur.execute('''
        SELECT schemaname, tablename, tableowner
        FROM pg_tables
        WHERE tablename='fc_migration' AND tableowner='fudan_coffee';
    ''')

    mirgation_schema = cur.fetchall()
    if not mirgation_schema:
        print 'create new schema: pw_migration'
        cur.execute('''
            CREATE TABLE fc_migration (
                    id              BIGSERIAL PRIMARY KEY,
                    key                    VARCHAR NOT NULL,
                    create_time     TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
                    );
            CREATE UNIQUE INDEX fc_migration_key ON fc_migration(key);
        ''')
        conn.commit()

def sql_ok(info):
    #for keyword in ('DROP', 'drop', 'delete', 'DELETE', 'TRUNCATE', 'truncate'):
    #    if keyword in info and 'pw_tag' not in info:
    #        return False

    return True


def migrate_sql(conn, cur, key, filename):
    cur.execute('SELECT id from fc_migration where key=%s;', (key,))
    hist = cur.fetchall()
    if not hist:
        print 'migrating ', str(filename), '........'
        try:
            sql_file = open('%s/%s' % (MIGRATION_PATH, filename))
            info = sql_file.read()
            sql_file.close()

            print 'exec: ', str(info)
            if not sql_ok(info):
                print 'drop, delete sql not permitted ', filename
                cur.close()
                conn.close()
                sys.exit(1)
            cur.execute(info)
            cur.execute('INSERT into fc_migration (key) values(%s);', (key,))
            conn.commit()
            print 'done'
        except:
            print 'migration fail for ', filename
            import traceback
            traceback.print_exc()
            cur.close()
            conn.close()
            sys.exit(1)


def work():
    myopts = hashopts('ht:p:')
    myopts.get('-h') and usage()
    port = myopts.get('-p') or usage()
    try:
        conn = psycopg2.connect(SQLDB_DSN)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    except:
        traceback.print_exc()
        return

    init_db(conn, cur)

    sql_files = candicates()
    while not sql_files.empty():
        each = sql_files.get()
        migrate_sql(conn, cur, str(each[0]), each[1])

    cur.close()
    conn.close()


if __name__ == '__main__':
    check_version()
    work()
