#!/usr/bin/env python3

import discord
from discord.ext import commands
import os
import random
import psycopg2
import time as Time
from data.secrets import token

client = commands.Bot(command_prefix="f.")


@client.event
async def on_ready():
    print(Time.asctime(Time.localtime()))

client.run(token)
