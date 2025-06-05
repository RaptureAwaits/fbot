from discord import Colour, Embed, Message, TextChannel

from src.constants import DEFAULT_DELETE_TIMER


class AlertEmbed(Embed):
    def __init__(self, *args, **kwargs):
        self.timer: int = kwargs.pop("delete_after", DEFAULT_DELETE_TIMER)

        self.msg: Message = kwargs.pop("msg", None)
        self.reference = kwargs.pop("reference", None)
        if not self.reference and self.msg:
            self.reference = self.msg.to_reference()

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
        await channel.send(delete_after=self.timer, embed=self, reference=self.reference)
