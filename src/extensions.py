from discord import TextChannel, Colour, Embed


class AlertEmbed(Embed):
    def __init__(self, *args, **kwargs):
        self.timer = kwargs.get("delete_after", 30)

        kwargs["colour"] = Colour.dark_red()
        if self.timer:
            kwargs["footer"] = f"This message will self-destruct after {self.timer} seconds..."

        super().__init__(
            *args,
            **kwargs
        )

    async def send(self, channel: TextChannel):
        await channel.send(embed=self, delete_after=self.timer)
