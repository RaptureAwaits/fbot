import sqlite3
from os.path import isfile
from os.path import join as os_join

from data.constants import DATA_PATH, DATABASE_PATH

USER_DB = "users"
SERVER_DB = "servers"
LOG_DB = "logs"
PINS_DB = "pins"

DATABASES = [USER_DB, SERVER_DB, LOG_DB, PINS_DB]

DB_PATHS = {name: os_join(DATABASE_PATH, f"{name}.db") for name in DATABASES}
SCHEMA_PATHS = {name: os_join(DATA_PATH, f"{name}_schema.sql") for name in DATABASES}
db_connections = {name: None for name in DATABASES}


class Connection:
    def __init__(self, target):
        db_connections[target] = self

        self.target = target

        self.conn = None
        self.c = None
        self.create = False

        self.create_connection()
        self.create_cursor()

        if self.create:
            self.execute_schema()

    def create_connection(self):
        if not isfile(DB_PATHS[self.target]):
            self.create = True

        self.conn = sqlite3.connect(DB_PATHS[self.target])

    def create_cursor(self):
        self.c = self.conn.cursor()

    def execute_schema(self):
        with open(SCHEMA_PATHS[self.target], 'r') as schema:
            self.c.executescript(schema.read())


def get_db_connection(db):
    if db_connections[db]:
        return db_connections[db]
    else:
        return Connection(db)
