#!/usr/bin/env python

"""Benchmark DB.

Usage:
  bench.py generate
  bench.py [1000|10000|20000] (mysql|pg|sqlite3) ... [--fork] [--myisam]
  bench.py [1000|10000|20000] --all-db [--fork] [--myisam]
  bench.py -h | --help

Options:
  generate      Generate csv files.
  -h --help     Show this screen.
  --all-db      Run for all databases.
  --myisam      Use MyISAM engine for MySQL tables.
  --fork        Use 2 concurrent processes.
"""


import csv
import os
import random
import sqlite3
import timeit

from datetime import datetime

import MySQLdb
import psycopg2
from docopt import docopt

import conf


class DataGenerator(object):
    lorem = ("Ultricies, habitasse aliquam. Odio? Dolor nunc massa pid phasellus,"
             "augue? Et platea nec augue, urna odio arcu eros magnis mauris!"
             "Dignissim! Dis turpis sociis. Ultricies, sed mauris amet, risus cras"
             "tincidunt adipiscing, elementum, sagittis, amet adipiscing arcu"
             "adipiscing! Elementum pid, est etiam? Scelerisque in, integer lorem"
             "tincidunt, odio enim scelerisque turpis ac adipiscing risus"
             "parturient aliquet! Odio rhoncus porta turpis, ridiculus nunc mauris,"
             "est quis mid, velit magna ac, facilisis augue magna in magna nisi eu"
             "dolor et ac rhoncus ac enim non placerat proin vel habitasse elit"
             "arcu vel, enim est? Pulvinar lorem elementum, enim, augue dapibus?")
    lorem_list = lorem.split()

    @classmethod
    def rand_words(cls, count=None):
        if not count:
            count = random.randrange(len(cls.lorem_list))

        result = [random.choice(cls.lorem_list) for i in range(count)]
        return ' '.join(result)

    @classmethod
    def rand_str(cls, count=None):
        if not count:
            count = random.randrange(len(cls.lorem))

        result = []
        try:
            result = random.sample(cls.lorem, count)
        except ValueError:
            pass
        return ''.join(result)

    @classmethod
    def rand_user(cls):
        return [
            cls.rand_words(3), # name
            cls.rand_words(random.randint(100, 1000)), # description
            datetime.now().isoformat(), # created_at %Y-%m-%d %H:%i:%s
            datetime.now().isoformat(), # updated_at
        ] + [cls.rand_str(100) for i in range(13)]

    @classmethod
    def gen_and_write_csv(cls, lines):
        with open('users_%d.csv' % lines, 'w') as f:
            writer = csv.writer(f)
            for i in range(lines):
                writer.writerow(cls.rand_user())


class DB(object):
    insert_q = \
        """INSERT INTO users (
            pid_index, pid_no_index, name, description, created_at, updated_at,
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

    @classmethod
    def get_connection(cls, db):
        if db == 'mysql':
            return MySQLdb.connect(**conf.mysql)
        if db == 'pg':
            return psycopg2.connect(**conf.pg)

        if db == 'sqlite3':
            return sqlite3.connect(conf.sqlite3['file'])

    @classmethod
    def setup(cls, db, engine=None):
        conn = cls.get_connection(db)
        c = conn.cursor()
        with open('tables_%s.sql' % db) as f:
            if (db == 'mysql') and engine and (engine.lower() == 'myisam'):
                c.execute(f.read().replace('InnoDB', 'MyISAM'))
            else:
                c.execute(f.read())
            conn.commit()

    @classmethod
    def teardown(cls, db):
        conn = cls.get_connection(db)
        c = conn.cursor()
        c.execute("DROP TABLE users;")
        conn.commit()

def run_inserts(db, count=1000):
    query = DB.insert_q
    if db == 'sqlite3':
        query = query.replace('%s', '?')

    pid = os.getpid()

    conn = DB.get_connection(db)
    c = conn.cursor()

    with open('users_%d.csv' % count) as csvfile:
        reader = csv.reader(csvfile)
        i = 1
        for row in reader:
            if i%1000 == 0: print '> %d - %d' % (pid, i)
            i += 1
            c.execute(query, [pid, pid] + row)

        conn.commit()

def run_mysql_inserts(count=1000):
    run_inserts('mysql', count)

def run_pg_inserts(count=1000):
    run_inserts('pg', count)

def run_sqlite3_inserts(count=1000):
    run_inserts('sqlite3', count)

def run_bench(job):
    t = timeit.timeit('run_%(db)s_inserts(%(count)d)' % job,
                      'from __main__ import run_%(db)s_inserts' % job, number=1)
    print '> %d TIME: %.2f' % (os.getpid(), t)

def run_fork(job):
    child_pid = os.fork()

    if child_pid == 0:
        print '>', 'Starting child with pid:', os.getpid()
    else:
        print '>', 'Starting parent with pid:', os.getpid()

    run_bench(job)

    if child_pid == 0:
        print '>', 'CHILD DONE'
        quit()
    else:
        print '>', 'PARENT DONE'
        os.wait()

def run(jobs, fork=False):
    print('')

    for job in jobs:
        print '>', 'Setting up:', job['db']
        DB.setup(job['db'], engine=job['engine'])

        if fork:
            run_fork(job)
        else:
            run_bench(job)

        print '>', 'Shutting down:', job['db'], '\n\n'
        DB.teardown(job['db'])

if __name__ == '__main__':
    args = docopt(__doc__)

    #print(args)
    #quit()

    if args['generate']:
        DataGenerator.gen_and_write_csv( 1000)
        DataGenerator.gen_and_write_csv(10000)
        DataGenerator.gen_and_write_csv(20000)
        print '3 csv files generated in the current directory.'
        quit()

    count_opts = [1000, 10000, 20000]
    count = 1000

    db_opts = ['mysql', 'pg', 'sqlite3']

    for op in count_opts:
        if args[str(op)]:
            count = op

    dbs = []
    if args['--all-db']:
        dbs = db_opts
    else:
        for db in db_opts:
            if args[db] > 0:
                dbs.append(db)
        #dbs = args['<db>']

    jobs = []
    for db in dbs:
        job = {
            'db': db,
            'count': count,
            'engine': 'myisam' if args['--myisam'] else '',
        }
        jobs.append(job)

    if not jobs:
        print '\n', 'No valid databases to benchmark!', '\n'
        quit()

    print '\n', 'Starting benchmark:'
    print '    dbs:', ', '.join(dbs)
    print '    count:', count
    print '    myisam:', args['--myisam']
    print '    fork:', args['--fork']

    run(jobs, fork=args['--fork'])
