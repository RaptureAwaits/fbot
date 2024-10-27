import os
import yaml

from discord import Client, Emoji, Guild, Role, TextChannel
from sqlalchemy import create_engine, Engine

from src.constants import CONFIG_DIR, INSTANCE_DIR, ROOT_DIR
from src.orm_models import FbotBase
from src.logger import logger

token_path = os.path.join(ROOT_DIR, "token.yaml")
with open(token_path, "r") as token_file:
    token = yaml.safe_load(token_file).get("token")


class FbotMissingEntity(BaseException):
    def __init__(self, entity: str, **kwargs):
        kwarg_str = ", ".join([f"{key}={val}" for key, val in kwargs.items()])
        message = (
            f"Could not get details for specified {entity}. Does this {entity} exist, and does the bot have " +
            f"permission to view it? ({kwarg_str})"
        )
        super().__init__(message)


class ServerConfig:
    @staticmethod
    def load_configs(client: Client):
        server_configs: dict[int: ServerConfig] = {}

        config_files = os.listdir(CONFIG_DIR)
        for cfg_filename in config_files:
            if cfg_filename == "config_template.yaml":
                continue

            cfg_filepath = os.path.join(CONFIG_DIR, cfg_filename)
            try:
                cfg = ServerConfig(cfg_filepath, client)
                server_configs[cfg.guild.id] = cfg
            except Exception as err:
                logger.error(
                    f"Failed to load server config {cfg_filename}: {err}"
                )
        return server_configs

    async def load_emoji(self) -> None:
        self.upvote = await self.guild.fetch_emoji(self.raw_config["emoji"]["upvote"])
        self.downvote = await self.guild.fetch_emoji(self.raw_config["emoji"]["downvote"])

    def __init__(self, config_filepath: str, client: Client):
        with open(config_filepath, "r") as cfg_file:
            cfg_yaml: dict[str, str | int | dict] = yaml.safe_load(cfg_file)
        self.raw_config = cfg_yaml

        # Core
        self.client = client
        self.guild: Guild = self.get_guild(cfg_yaml["info"]["guild"])

        # Channels
        self.bot_channel: TextChannel = self.get_channel(cfg_yaml["channels"]["bot"])
        self.pin_channel: TextChannel = self.get_channel(cfg_yaml["channels"]["pin"])

        # Roles
        self.mod_role: Role = self.get_role(cfg_yaml["roles"]["privileged"])

        # Vote symbols
        self.upvote: Emoji | None = None
        self.downvote: Emoji | None = None

        # Milestones
        self.milestones: dict[int, str] = {}
        for milestone in cfg_yaml["milestones"]["after"]:
            milestone: dict[str, int | str]
            self.milestones[milestone["number"]] = milestone["message"]
        if 1 not in self.milestones:  # Makes sure there's at least one message
            self.milestones[1] = "Respects have been paid <x> times."
        self.first = cfg_yaml["milestones"]["first"] or self.milestones[1]

        # Database
        self.db_filepath = os.path.join(INSTANCE_DIR, f"{self.guild.id}.db")
        self.db_engine = self.get_db_engine()

    def get_guild(self, guild_id: int) -> Guild:
        guild = self.client.get_guild(guild_id)
        if not guild:
            raise FbotMissingEntity("guild", guild_id=guild_id)
        return guild

    def get_channel(self, channel_id: int) -> TextChannel:
        channel = self.guild.get_channel(channel_id)
        if not channel:
            raise FbotMissingEntity("channel", channel_id=channel_id, guild_id=self.guild.id)
        return channel

    def get_role(self, role_id: int) -> Role:
        role = self.guild.get_role(role_id)
        if not role:
            raise FbotMissingEntity("role", role_id=role_id, guild_id=self.guild.id)
        return role

    async def set_emoji(self, emoji_id: int) -> Emoji:
        emoji = await self.guild.fetch_emoji(emoji_id)
        if not emoji:
            raise FbotMissingEntity("emoji", emoji_id=emoji_id, guild_id=self.guild.id)
        return emoji

    def get_db_engine(self) -> Engine:
        new_file = False
        if not os.path.isfile(self.db_filepath):
            new_file = True
            with open(self.db_filepath, "w") as _:
                pass

        engine: Engine = create_engine("sqlite:///" + self.db_filepath)
        if new_file:
            FbotBase.metadata.create_all(engine)

        return engine

    def __str__(self):
        return self.guild.name

    def __int__(self):
        return self.guild.id
