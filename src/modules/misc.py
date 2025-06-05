from discord import Colour
from discord.ext.commands import Cog, command, Context

from datetime import datetime, timedelta
from math import floor

from src.constants import APP_NAME, SOURCE_ICON, SOURCE_URL
from src.extensions import AlertEmbed

start_time = datetime.now()


class MiscCog(Cog, name="Miscellaneous"):
    colour = Colour.darker_gray()

    def __init__(self, *args, **kwargs):
        pass

    @command("source")
    async def source_command(self, context: Context):
        source_str = f"Feeling curious...?\n{SOURCE_URL}"
        source_embed = AlertEmbed(
            title=f"{APP_NAME} Source Code",
            description=source_str,
            url=SOURCE_URL,
            msg=context.message
        )
        source_embed.set_thumbnail(url=SOURCE_ICON)
        await source_embed.send(context.channel)

    @command("uptime")
    async def uptime_command(self, context: Context):
        uptime_td: timedelta = datetime.now() - start_time

        s = uptime_td.total_seconds()
        years, rem = divmod(s, 60 * 60 * 24 * 365)
        days, rem = divmod(rem, 60 * 60 * 24)
        hours, rem = divmod(rem, 60 * 60)
        mins, secs = divmod(rem, 60)
        uptime_str = (
            f"Current uptime:\n" +
            f"- {floor(years):02} years,\n" +
            f"- {floor(days):02} days,\n"
            f"- {floor(hours):02} hours,\n"
            f"- {floor(mins):02} minutes, and\n"
            f"- {floor(secs):02} seconds."
        )

        uptime_embed = AlertEmbed(
            title=f"{APP_NAME} Uptime Report",
            description=uptime_str,
            msg=context.message
        )

        th = {1: "st", 2: "nd", 3: "rd"}.get(start_time.day, "th")
        footer_str = (
            f"This instance has been live since {start_time.strftime(f'%A %d{th} %B %Y, %H:%M:%S')}."
        )
        uptime_embed.set_footer(text=footer_str)
        await uptime_embed.send(context.channel)
