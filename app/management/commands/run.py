import csv
import os
import random
import timeit

from django.conf import settings
from django.db import transaction, connections
from django.core.management.base import BaseCommand, CommandError

from app.models import Data, Content, Tag, ContentTag
from bench import DataGenerator as gen


def rand_content():
    return [
        gen.rand_words(3), # name
        gen.rand_words(random.randint(100, 1000)), # description
    ]

def rand_data():
    data = [
        gen.rand_words(random.randint(1000, 5000)), # data
    ]
    for i in xrange(1, 16+1):
        data.append(gen.rand_str(100))
    return data

def rand_tag():
    num = random.randint(1, 5)
    return [
        gen.rand_words(random.randint(1, 2)), # tag
        Tag.LABEL_CHOICES[num-1][0], # label
        Tag.LABEL_CHOICES[num-1][0], # label_index
        num, # label_num
        num, # label_num_index
    ]

def prepare_db(db):
    print '\nPreparing %s DB...\n' % db

    os.system('./benchdb.py migrate --database=%s app zero' % db)
    print
    os.system('./benchdb.py migrate --database=%s app' % db)

def clean_db(db):
    print '\nCleaning %s DB...\n' % db

    if db in ['default', 'sqlite3']:
        os.system('rm %s' % settings.DATABASES[db]['NAME'])
    else:
        os.system('./benchdb.py migrate --database=%s app zero' % db)

def generate(lines):
    os.system('mkdir -p data')

    print '\nGenerating Tags...\n'

    with open('data/%d_tags.csv' % lines, 'w') as f:
        writer = csv.writer(f)
        for i in range(lines):
            writer.writerow(rand_tag())

    print '\nGenerating Content...\n'

    with open('data/%d_content.csv' % lines, 'w') as f:
        writer = csv.writer(f)
        for i in range(lines):
            writer.writerow(rand_content())

    print '\nGenerating Data...\n'

    with open('data/%d_data.csv' % lines, 'w') as f:
        writer = csv.writer(f)
        for i in range(lines):
            writer.writerow(rand_data())

    print '\nGenerating Tag relations...\n'

    with open('data/%d_content_tags.csv' % lines, 'w') as f:
        writer = csv.writer(f)
        for t in range(5):
            for i in xrange(lines):
                if random.choice((True, False)):
                    content_id = i+1
                    tag_id = random.randint(1, lines)
                    writer.writerow((content_id, tag_id))

    print '\nDone\n'


def run_insert_tags(db, lines):
    pid = os.getpid()

    print '\nInserting Tags on %s DB...\n' % db

    with open('data/%d_tags.csv' % lines) as csvfile, transaction.atomic(using=db):
        reader = csv.reader(csvfile)
        i = 1
        for row in reader:
            Tag.objects.using(db).create(
                tag=row[0],
                label=row[1],
                label_index=row[2],
                label_num=int(row[3]),
                label_num_index=int(row[4]),
            )
            if i%1000 == 0: print '> %d - %d' % (pid, i)
            i += 1

def run_insert_content(db, lines):
    pid = os.getpid()

    print '\nInserting Content on %s DB...\n' % db

    with open('data/%d_content.csv' % lines) as csvfile, transaction.atomic(using=db):
        reader = csv.reader(csvfile)
        i = 1
        for row in reader:
            Content.objects.using(db).create(
                pid=pid,
                pid_index=pid,
                name=row[0],
                description=row[1],
            )
            if i%1000 == 0: print '> %d - %d' % (pid, i)
            i += 1

def run_insert_content_tags(db, lines):
    pid = os.getpid()

    print '\nInserting Tag relations on %s DB...\n' % db

    with open('data/%d_content_tags.csv' % lines) as csvfile, transaction.atomic(using=db):
        reader = csv.reader(csvfile)
        i = 1
        for row in reader:
            # Content.objects.using(db).get(pk=row[0]).tags.add(
            #     Tag.objects.using(db).get(pk=row[1])
            # )
            ContentTag.objects.using(db).create(content_id=row[0], tag_id=row[1])
            if i%1000 == 0: print '> %d - %d' % (pid, i)
            i += 1

def run_insert_data(db, lines):
    pass
    pid = os.getpid()

    print '\nInserting Data on %s DB...\n' % db

    with open('data/%d_data.csv' % lines) as csvfile, transaction.atomic(using=db):
        reader = csv.reader(csvfile)
        i = 1
        for row in reader:
            Data.objects.using(db).create(
                # parent=Content.objects.using(db).get(pk=i),
                parent_id=i,
                data=row[0],
                col1=row[1],
                col2=row[2],
                col3=row[3],
                col4=row[4],
                col5=row[5],
                col6=row[6],
                col7=row[7],
                col8=row[8],
                col9=row[9],
                col10=row[10],
                col11=row[11],
                col12=row[12],
                col13=row[13],
                col14=row[14],
                col15=row[15],
                col16=row[16],
            )
            if i%1000 == 0: print '> %d - %d' % (pid, i)
            i += 1

def run_inserts(db, lines):
    print '\nRunning inserts on %s DB...\n' % db

    for test in ['tags', 'content', 'content_tags', 'data']:
        t = timeit.timeit('run_insert_%s("%s", %d)' % (test, db, lines),
                          'from %s import run_insert_%s' % (__name__, test), number=1)
        print '> PID: ', os.getpid(), ', TIME: ', t

def test_insert(db, lines):
    prepare_db(db)

    try:
        t = timeit.timeit('run_inserts("%s", %d)' % (db, lines),
                          'from %s import run_inserts' % __name__, number=1)
        print
        print '> DB: ', db
        print '> PID: ', os.getpid()
        print '> TOTAL TIME: ', t
        print

    finally:
        # return
        clean_db(db)

class Command(BaseCommand):
    # args = ('generate', '<mysql>')

    def handle(self, *args, **options):
        print args
        print options

        lines = 1000

        if 'generate' in args:
            generate(lines)

        if 'test_insert' in args:
            test_insert('mysql', lines)

            # sqlite3, mysql, pg
            # *, 26, 5
            # 1, 0.70, 0.80