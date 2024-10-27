import re

from discord import Member
from src.config import ServerConfig


def parse_f_message(message: str, f: int, user: Member) -> str:
    message = re.sub(r"<x>", str(f), message)
    message = re.sub(r"<u>", user.mention, message)
    return message


def get_f_message(f: int, user: Member, server_config: ServerConfig) -> str:
    if f == 1:
        return parse_f_message(server_config.first, f=f, user=user)
    for m in sorted(list(server_config.milestones.keys()), reverse=True):
        if f % m == 0:
            return parse_f_message(server_config.milestones.get(m), f=f, user=user)
