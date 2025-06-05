from src import client
from src.config import token
from src.constants import APP_NAME
from src.logger import logger


if __name__ == "__main__":
    logger.info(f"Starting {APP_NAME}...")
    client.run(token=token, log_handler=None)
