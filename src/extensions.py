from discord import Colour, Embed


class AlertEmbed(Embed):
    def __init__(self, *args, **kwargs):
        kwargs["colour"] = Colour.dark_red()
        kwargs["footer"] = "This message will self-destruct after 30 seconds..."
        kwargs["delete_after"] = 30

        super().__init__(
            *args,
            **kwargs
        )
