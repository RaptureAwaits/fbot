from src.setup import setup_required
if setup_required:
    exit()

from discord import Intents, Message
from discord.ext.commands import (
    Bot,
    Cog,
    CommandNotFound
)
from typing import Type

from src.config import ServerConfig, token
from src.constants import APP_NAME
from src.modules.f import get_f_message
from src.logger import logger
from src.models import Users, Fs

from src.modules.f import FCog
from src.modules.misc import MiscCog
from src.modules.pins import PinsCog

intents = Intents(
    guilds=True,
    members=True,
    messages=True,
    message_content=True,
    reactions=True
)

client = Bot(command_prefix='f.', intents=intents)
server_configs = None


async def _add_cog(cog: Type[Cog]):
    await client.add_cog(cog(client, server_configs))


@client.event
async def on_ready():
    logger.info("Loading server configs...")
    global server_configs
    server_configs = ServerConfig.load_configs(client)

    logger.info("Registering cogs...")
    await _add_cog(FCog)
    await _add_cog(MiscCog)
    await _add_cog(PinsCog)

    logger.info("Loading server emoji...")
    for sc in server_configs.values():
        sc: ServerConfig
        await sc.load_emoji()

    logger.info(f"{APP_NAME} online. Listening...")


@client.event
async def on_message(message: Message):
    try:
        await client.process_commands(message)
    except CommandNotFound:
        pass
