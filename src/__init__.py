from src.setup import setup_required
if setup_required:
    exit()

from datetime import datetime

import discord
from discord.ext.commands import (
    Bot,
    Cog,
)
from typing import Type

from src.config import ServerConfig, token
from src.constants import APP_NAME
from src.modules.f import get_f_message
from src.logger import logger
from src.models import Users, Fs

from src.modules.f import F
from src.modules.misc import Misc
from src.modules.pins import Pins

intents = discord.Intents(
    guilds=True,
    members=True,
    messages=True,
    message_content=True,
    reactions=True
)

client = Bot(command_prefix='f.', intents=intents)
server_configs = None


def _add_cog(cog: Type[Cog]):
    client.add_cog(cog(client, server_configs))


_add_cog(F)
_add_cog(Misc)
_add_cog(Pins)


@client.event
async def on_ready():
    logger.info("Loading server configs...")
    global server_configs
    server_configs = ServerConfig.load_configs(client)

    logger.info("Loading server emoji...")
    for sc in server_configs.values():
        sc: ServerConfig
        await sc.load_emoji()

    logger.info(f"{APP_NAME} online. Listening...")
