from discord import TextChannel, Colour, Embed


class AlertEmbed(Embed):
    def __init__(self, *args, **kwargs):
        self.timer = kwargs.get("delete_after", 30)

        kwargs["colour"] = Colour.dark_red()

        super().__init__(
            *args,
            **kwargs
        )

        if self.timer:
            self.set_footer(text=f"This message will self-destruct after {self.timer} seconds...")

    async def send(self, channel: TextChannel):
        await channel.send(embed=self, delete_after=self.timer)
