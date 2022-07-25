from os.path import dirname
from os.path import join as os_join

DATA_PATH = dirname(__file__)
BASE_PATH = dirname(DATA_PATH)
DATABASE_PATH = os_join(DATA_PATH, "database")
