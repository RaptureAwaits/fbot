from src.setup import setup_required
if setup_required:
    exit()

import re

from datetime import datetime, timedelta

import discord
from discord import (
    Member, Message, Reaction, RawReactionActionEvent
)
from discord.ext import commands

from src.config import ServerConfig, token
from src.constants import APP_NAME
from src.f import get_f_message
from src.logger import logger
from src.orm_models import Users, F, Pins, Votes

intents = discord.Intents(
    guilds=True,
    members=True,
    messages=True,
    message_content=True,
    reactions=True
)

client = commands.Bot(command_prefix='f.', intents=intents)
server_configs: dict[int: ServerConfig]
start_time: datetime | None = None


@client.event
async def on_ready():
    global server_configs
    global start_time

    server_configs = ServerConfig.load_configs(client)
    for sc in server_configs.values():
        sc: ServerConfig
        await sc.load_emoji()
    start_time = datetime.now()
    logger.info(f"{APP_NAME} online. Listening...")


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    server_config: ServerConfig = server_configs.get(message.guild.id)

    if re.match(r"\s*f\s*[^.]]", message.content):
        user: Users = Users.get_user(message.author.id, server_config=server_config)
        user.create_f(server_config=server_config)
        await server_config.bot_channel.send(get_f_message(
            F.get_total_f(server_config=server_config), message.author, server_config)
        )


@client.event
async def on_reaction_add(reaction: Reaction, user: Member):
    server_config: ServerConfig = server_configs.get(reaction.message.guild.id)
    # if (
    #     reaction.message.channel == server_config.pin_channel and  # Reaction is to a message in pin channel
    #     reaction.message.author == client.user and  # Reaction is to a bot message (all pins are bot msgs)
    #     reaction.emoji == server_config.upvote or reaction.emoji == server_config.downvote  # Reaction is up/downvote
    # ):
    #     pass  # Add credit, DB stuff


@client.event
async def on_raw_reaction_add(payload: RawReactionActionEvent):
    server_config: ServerConfig = server_configs.get(payload.guild_id)
    # await server_config.pin_channel.send(
    #     f"Sorry {payload.member.mention}, you were too slow on that one!",
    #     delete_after=30
    # )


@client.command()
async def uptime(context: commands.Context):
    uptime_td: timedelta = datetime.now() - start_time
    uptime_str = f"Current uptime: {str(uptime_td)}"
    await context.message.channel.send(uptime_str)


@client.command()
async def credit(context: commands.Context):
    # Display user's social credit rating and a leaderboard
    server_config: ServerConfig = server_configs.get(context.guild.id)


@client.command()
async def respects(context: commands.Context):
    # Display a breakdown of Fs by user
    server_config: ServerConfig = server_configs.get(context.guild.id)


@client.command()
async def source(context: commands.Context):
    await context.channel.send("https://github.com/RaptureAwaits/fbot")


if __name__ == "__main__":
    logger.info(f"Starting {APP_NAME}...")
    client.run(token=token, log_handler=None)
