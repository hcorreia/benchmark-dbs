#!/usr/bin/env python

import os


mysql = {
    'db': 'bench_db',
    'user': 'root',
    'pass': 'root',
}
pg = {
    'db': 'bench_db',
    'user': 'bench_user',
    'pass': 'bench',
}

os.system("""apt-get install -y \\
    mysql-server \\
    postgresql \\
    postgresql-server-dev-all \\
    python-mysqldb \\
    python-psycopg2 \\
    python-docopt""")

# MySQL
os.system('echo "CREATE DATABASE %(db)s;" | mysql -u %(user)s -p%(pass)s' % mysql)

# PG
os.system('echo "CREATE DATABASE %(db)s;" | sudo -u postgres psql' % pg)
os.system('echo "CREATE ROLE %(user)s WITH LOGIN PASSWORD \'%(pass)s\';" | sudo -u postgres psql' % pg)
os.system('echo "GRANT ALL ON DATABASE %(db)s TO %(user)s;" | sudo -u postgres psql' % pg)
