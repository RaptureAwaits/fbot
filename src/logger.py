import logging
import os
import sys

from logging.handlers import RotatingFileHandler

from src.constants import APP_NAME, LOG_DIR

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

logging.getLogger('discord.http').setLevel(logging.INFO)

stream_handler = logging.StreamHandler(stream=sys.stdout)
file_handler = RotatingFileHandler(
    filename=os.path.join(LOG_DIR, f'{APP_NAME}.log'),
    maxBytes=128 * 1024 * 1024,
    backupCount=4
)  # Maximum of 4 * 128MiB files for 512MiB total

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[stream_handler, file_handler]
)
