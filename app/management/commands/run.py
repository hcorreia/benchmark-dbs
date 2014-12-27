import os
import random
import timeit

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from app.models import Data, Content, Tag
from bench import DataGenerator as gen


def rand_content():
    return {
        'name':        gen.rand_words(3),
        'description': gen.rand_words(random.randint(100, 1000)),
    }

def rand_data():
    data = {
        'data': gen.rand_words(random.randint(1000, 5000)),
    }
    for i in xrange(1, 16+1):
        data['col%d'%i] = gen.rand_str(100)
    return data

def rand_tag():
    num = random.randint(1, 5)
    return {
        'label': Tag.LABEL_CHOICES[num-1][0],
        'label_index': Tag.LABEL_CHOICES[num-1][0],
        'label_num': num,
        'label_num_index': num,
        'tag': gen.rand_words(random.randint(1, 2)),
    }

def prepare_db(db):
    print '\nPreparing %s DB...\n' % db

    os.system('./benchdb.py migrate --database=%s app zero' % db)
    print
    os.system('./benchdb.py migrate --database=%s app' % db)

def clean_db(db):
    print '\nCleaning %s DB...\n' % db

    if db == 'default':
        os.system('rm %s' % settings.DATABASES['default']['NAME'])
    else:
        os.system('./benchdb.py migrate --database=%s app zero' % db)

def generate(lines):
    # print rand_tag()

    prepare_db('default')

    print '\nGenerating Tags...\n'

    Tag.objects.bulk_create([Tag(**rand_tag()) for i in xrange(lines)])

    print '\nGenerating Content...\n'

    for i in xrange(lines):
        content = Content(**rand_content())
        content.save()
        content.tags.add(*[Tag.objects.get(pk=j) for j in xrange(1, 11)])


    print '\nGenerating Data...\n'

    data_list = []
    for i in xrange(lines):
        data = Data(**rand_data())
        data.parent_id = i+1
        data_list.append(data)
    Data.objects.bulk_create(data_list)

    print '\nDumping DB...\n'
    os.system('./benchdb.py dumpdata > data_%d.json' % lines)

    # clean_db('default')

    print '\nDone\n'


def run_inserts(db, lines):
    print '\nRunning inserts on %s DB...\n' % db
    os.system('./benchdb.py loaddata data_%d.json --database=%s' % (lines, db))
    # os.system('./benchdb.py runscript data_%d.py --database=%s' % (lines, db))

def test_insert(db, lines):
    prepare_db(db)

    t = timeit.timeit('run_inserts("%s", %d)' % (db, lines),
                      'from %s import run_inserts' % __name__, number=1)
    print '> %d TIME: %.2f' % (os.getpid(), t)

    clean_db(db)

class Command(BaseCommand):
    # args = ('generate', '<mysql>')

    def handle(self, *args, **options):
        print args
        print options

        lines = 10

        if 'generate' in args:
            generate(lines)

        if 'test_insert' in args:
            test_insert('pg', lines)

