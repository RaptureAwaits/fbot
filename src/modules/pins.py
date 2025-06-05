from discord import Colour, Embed, Member, RawReactionActionEvent, Reaction
from discord.ext.commands import Cog

from datetime import datetime

from src.config import ServerConfig
from src.extensions import AlertEmbed
from src.models import Users

start_time = datetime.now()


class Pins(Cog):
    colour = Colour.gold()

    def __init__(self, client, server_configs):
        self.client = client
        self.configs = server_configs

    @Cog.listener("on_reaction_add")
    async def pin_react_listener(self, reaction: Reaction, user: Member):
        server_config: ServerConfig = self.configs.get(reaction.message.guild.id)
        if not server_config:
            return

        if reaction.emoji != server_config.pin_symbol:
            return

        db_user: Users = Users.get_user(user.id)
        db_user.create_pin(
            reaction.message.id,
            reaction.message.content,
            reaction.message.author.id
        )

        pin_title = f"{reaction.message.author.mention} said:"
        pin_embed = Embed(
            title=pin_title,
            colour=self.colour,
            description=reaction.message.content
        )
        pin_message = await server_config.pin_channel.send(embed=pin_embed)

        pin_alert_str = (
            f"{user.mention} has pinned a message from {reaction.message.author.mention}, check it out:\n" +
            f"{pin_message.to_reference()}"
        )
        pin_alert_embed = AlertEmbed(
            title="Message Pinned!",
            description=pin_alert_str
        )
        await pin_alert_embed.send(reaction.message.channel)

    @Cog.listener("on_raw_reaction_add")
    async def missed_pin_listener(self, payload: RawReactionActionEvent):
        server_config: ServerConfig = self.configs.get(payload.guild_id)
        if not server_config:
            return

        fail_str = f"Sorry {payload.member.mention}, you were too slow on that one!",
        fail_embed = AlertEmbed(
            title="Pin Failed!",
            description=fail_str
        )
        await fail_embed.send(server_config.pin_channel)

    @Cog.listener("on_reaction_add")
    async def pin_vote_listener(self, reaction: Reaction, user: Member):
        server_config: ServerConfig = self.configs.get(reaction.message.guild.id)
        if not server_config:
            return

        if (
            reaction.message.channel == server_config.pin_channel and  # Reaction is to a message in pin channel
            reaction.message.author == self.client.user and (  # Reaction is to a bot message (all pins are bot msgs)
                reaction.emoji == server_config.upvote or
                reaction.emoji == server_config.downvote
            )  # Reaction is up/downvote
        ):
            pass  # Add credit, DB stuff
