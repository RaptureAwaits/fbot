from discord import Colour, Embed, Member, RawReactionActionEvent, Reaction, User
from discord.ext.commands import Bot, Cog

from datetime import datetime

from src.config import ServerConfig
from src.extensions import AlertEmbed
from src.models import Pins, Users

start_time = datetime.now()


class PinsCog(Cog):
    colour = Colour.gold()

    def __init__(self, client, server_configs):
        self.client: Bot = client
        self.configs = server_configs

    @Cog.listener("on_reaction_add")
    async def pin_react_listener(self, reaction: Reaction, user: Member):
        server_config: ServerConfig = self.configs.get(reaction.message.guild.id)
        if not server_config:
            return

        if not server_config.pin_channel:
            return

        if reaction.emoji != server_config.pin_symbol:
            return

        if user.id == reaction.message.author.id:
            self_pin_alert_str = (
                f"Tsk tsk. No self-pinning, {user.mention}."
            )
            self_pin_embed = AlertEmbed(
                title="Pin Failed - No Self-pinning!",
                description=self_pin_alert_str,
            )
            return await self_pin_embed.send(reaction.message.channel)

        if (existing_pin := Pins.is_pinned(reaction.message.id, server_config=server_config)) is not None:
            existing_pin: Pins
            pinner: User = self.client.get_user(existing_pin.pinned_by_id)
            duplicate_alert_str = (
                f"Sorry {user.mention}, this message has already been pinned by {pinner.display_name}!"
            )
            duplicate_alert_embed = AlertEmbed(
                title="Pin Failed - Message Already Pinned!",
                description=duplicate_alert_str,
            )
            return await duplicate_alert_embed.send(reaction.message.channel)

        db_user: Users = Users.get_user(user.id, server_config=server_config)
        db_user.create_pin(
            reaction.message.id,
            reaction.message.content,
            reaction.message.author.id,
            server_config=server_config
        )

        pin_str = (
            f"**{reaction.message.author.mention} said: **\n" +
            f'"{reaction.message.content}"'
        )
        pin_embed = Embed(
            title="Message Pinned!",
            colour=self.colour,
            description=pin_str,
        )
        pin_embed.set_thumbnail(url=reaction.message.author.display_avatar.url)
        pin_embed.set_footer(text=f"Pinned by {user.display_name}", icon_url=user.display_avatar.url)
        pin_message = await server_config.pin_channel.send(embed=pin_embed)

        await pin_message.forward(reaction.message.channel)

    @Cog.listener("on_raw_reaction_add")
    async def missed_pin_listener(self, payload: RawReactionActionEvent):
        server_config: ServerConfig = self.configs.get(payload.guild_id)
        if not server_config:
            return

        if not server_config.pin_channel:
            return

        if payload.emoji != server_config.pin_symbol:
            return

        cached_ids = {m.id for m in self.client.cached_messages}
        if payload.message_id in cached_ids:
            return  # Better be quick on the draw

        fail_str = f"Sorry {payload.member.mention}, you were too slow on that one!"
        fail_embed = AlertEmbed(
            title="Pin Failed - Message Not Cached!",
            description=fail_str,
        )

        channel = self.client.get_channel(payload.channel_id)
        await fail_embed.send(channel)

    @Cog.listener("on_reaction_add")
    async def pin_vote_listener(self, reaction: Reaction, user: Member):
        server_config: ServerConfig = self.configs.get(reaction.message.guild.id)
        if not server_config:
            return

        if not server_config.pin_channel:
            return

        if (
            reaction.message.channel == server_config.pin_channel and  # Reaction is to a message in pin channel
            reaction.message.author == self.client.user and (  # Reaction is to a bot message (all pins are bot msgs)
                reaction.emoji == server_config.upvote or
                reaction.emoji == server_config.downvote
            )  # Reaction is up/downvote
        ):
            pass  # Add credit, DB stuff
