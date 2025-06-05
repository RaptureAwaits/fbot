from discord import Colour, Embed, Message, TextChannel


class AlertEmbed(Embed):
    def __init__(self, *args, **kwargs):
        self.timer: int = kwargs.pop("delete_after", 30)
        self.msg: Message = kwargs.pop("msg", None)

        kwargs["colour"] = Colour.dark_red()

        super().__init__(
            *args,
            **kwargs
        )

        if self.timer:
            self.set_footer(text=f"This message will self-destruct after {self.timer} seconds...")

    async def send(self, channel: TextChannel):
        if self.msg and self.timer:
            await self.msg.delete(delay=self.timer)
        await channel.send(embed=self, delete_after=self.timer)
