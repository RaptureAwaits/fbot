from os.path import dirname
from os.path import join as os_join

APP_NAME = "fbot"

ROOT_DIR = dirname(dirname(__file__))
CONFIG_DIR = os_join(ROOT_DIR, "config")
INSTANCE_DIR = os_join(ROOT_DIR, "instance")
LOG_DIR = os_join(ROOT_DIR, "logs")
TEMPLATE_DIR = os_join(ROOT_DIR, "templates")

DB_FILENAME = "fbot.sqlite"
DB_FILEPATH = os_join(INSTANCE_DIR, DB_FILENAME)

TOKEN_FILENAME = "token.yaml"
TOKEN_FILEPATH = os_join(ROOT_DIR, TOKEN_FILENAME)
TOKEN_TEMPLATE = os_join(TEMPLATE_DIR, "token_template.yaml")

SOURCE_URL = "https://github.com/RaptureAwaits/fbot"

DEFAULT_DELETE_TIMER = 10
