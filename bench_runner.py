#!/usr/bin/env python

machine = 'localvm'

commands = [
    './bench.py 10000 --all-db > results_%s_10000_1.txt' % machine,
    './bench.py 10000 --all-db > results_%s_10000_2.txt' % machine,
    './bench.py 20000 --all-db > results_%s_20000_1.txt' % machine,
    './bench.py 20000 --all-db > results_%s_20000_2.txt' % machine,
    './bench.py 20000 mysql pg --fork > results_%s_20000_fork_1.txt' % machine,
    './bench.py 20000 mysql pg --fork > results_%s_20000_fork_2.txt' % machine,
    './bench.py 20000 mysql --myisam > results_%s_20000_myisam_1.txt' % machine,
    './bench.py 20000 mysql --myisam > results_%s_20000_myisam_2.txt' % machine,
    './bench.py 20000 mysql --fork --myisam > results_%s_20000_fork_myisam_1.txt' % machine,
    './bench.py 20000 mysql --fork --myisam > results_%s_20000_fork_myisam_2.txt' % machine,
]


import os

total = len(commands)
for i,cmd in enumerate(commands):
    print 'Running %d of %d: %s' % (i, total, cmd)
    os.system(cmd)
