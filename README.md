Tested in Ubuntu 14.04 with python 2.7.

**For now only tests inserts.**

#### DB's:
 * MySQL
 * PostgreSQL
 * SQLite3

## Provisioning and settings.

This command is meant to be executed in a clean VPS or cloud server.

```sh
$ sudo ./provision_ubuntu.py
```

Copy conf.py.sample to conf.py and set database credentials.
If using the provision_ubuntu.py script, there is no need to change settings .

In a desktop its probably a good idea to created a virtual environment.

```sh
$ virtualenv .env
$ source .env/bin/activate
$ pip install MySQL-python psycopg2 docopt
```

## Examples

Generate data files.

```sh
$ ./bench.py generate
```

Run on all DB's with 1000 rows.

```sh
$ ./bench.py --all-db
```

Run mysql and postgres with 20000 using 2 concurrent processes with 20000 rows each.

```sh
$ ./bench.py 20000 mysql pg --fork
```

Run on all DB's using 2 concurrent processes with 1000 rows each.
Use MyISAM engine insted of InnoDB for mysql tables.

```sh
$ ./bench.py 1000 --all-db --fork --myisam
```

**Do not run sqlite3 with more than 1000 rows with --fork, the database will be locked for a long time and it will throw an error on one of the processes.**

## Usage

```
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
```
