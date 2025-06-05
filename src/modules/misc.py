from discord import Colour, Embed
from discord.ext.commands import Cog, command, Context

from datetime import datetime, timedelta

from src.constants import APP_NAME, SOURCE_URL

start_time = datetime.now()


class Misc(Cog):
    colour = Colour.darker_gray()

    def __init__(self, *args, **kwargs):
        pass

    @command("source")
    async def source_command(self, context: Context):
        source_str = "Feeling curious...?"
        source_embed = Embed(
            title=f"{APP_NAME} Source Code",
            colour=self.colour,
            description=source_str,
            url=SOURCE_URL
        )
        await context.channel.send(embed=source_embed)

    @command("uptime")
    async def uptime_command(self, context: Context):
        uptime_td: timedelta = datetime.now() - start_time
        uptime_str = f"Current uptime: {str(uptime_td)}"
        uptime_embed = Embed(
            title=f"{APP_NAME} Uptime Report",
            colour=self.colour,
            description=uptime_str,
        )
        await context.channel.send(embed=uptime_embed)
