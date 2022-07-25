#!/usr/bin/env python3

from discord.ext import commands
import time

from data.secrets import token
from src.db import get_db_connection, USER_DB, SERVER_DB, LOG_DB, PINS_DB

client = commands.Bot(command_prefix="f.")

users_db = get_db_connection(USER_DB)
servers_db = get_db_connection(SERVER_DB)
logs_db = get_db_connection(LOG_DB)
pins_db = get_db_connection(PINS_DB)


@client.event
async def on_ready():
    print(time.asctime(time.localtime()))
    print("Ready!")

client.run(token)
