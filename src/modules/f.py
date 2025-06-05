import re

from discord import (
    Colour,
    Embed,
    Member,
    Message,
)

from discord.ext.commands import (
    Cog,
    command,
    Context
)

from src.config import ServerConfig
from src.models import Fs, Users


def parse_f_message(message: str, f: int, user: Member) -> str:
    message = re.sub(r"<x>", str(f), message)
    message = re.sub(r"<u>", user.mention, message)
    return message


def get_f_message(f: int, user: Member, server_config: ServerConfig) -> str:
    if f == 1:
        return parse_f_message(server_config.first, f=f, user=user)
    for m in sorted(list(server_config.milestones.keys()), reverse=True):
        if f % m == 0:
            return parse_f_message(server_config.milestones.get(m), f=f, user=user)


class FCog(Cog, name="F"):
    colour = Colour.fuchsia()

    def __init__(self, client, server_config):
        self.client = client
        self.configs = server_config

    @Cog.listener("on_message")
    async def f_listener(self, message: Message):
        if message.author == self.client.user:
            return

        server_config: ServerConfig = self.configs.get(message.guild.id)
        if not server_config:
            return

        if message.content.lower() == "f":
            user: Users = Users.get_user(message.author.id, server_config=server_config)
            user.create_f(server_config=server_config)
            await server_config.bot_channel.send(get_f_message(
                Fs.get_total_f(server_config=server_config), message.author, server_config)
            )

    @command("respects")
    async def respects_command(self, context: Context):
        # Display a breakdown of Fs by user
        server_config: ServerConfig = self.configs.get(context.guild.id)
        if not server_config:
            return

        db_user: Users = Users.get_user(context.message.author.id, server_config=server_config)
        fs = db_user.get_user_f(server_config=server_config)

        response_str = (
            f"You have paid **{fs}** " +
            f"out of **{Fs.get_total_f(server_config=server_config)}** total respects."
        )
        response_embed = Embed(
            title=f"{context.message.author.display_name}'s Respects Report: {fs}",
            colour=self.colour,
            description=response_str
        )

        await context.channel.send(embed=response_embed)
