import re
from typing import Optional

from loguru import logger

from app.helpers.constants import REGEX_PATTERNS

__all__ = [
    "get_vk_id",
    "get_steamid",
    "get_player_name",
    "get_server_number",
    "is_string_is_date",
]


def _match(regex_pattern: str, message: str, type_: str = None) -> Optional[str]:
    """Helps match a regex pattern and loging when not matching

    Args:
        regex_pattern: The regex pattern to match
        message: The message when use regex pattern
        type_: The type of regex for logger

    """
    match = re.findall(regex_pattern, message)
    if match is None:
        logger.error(f"Could not find match {type_} in {message}")
    return (match[0]) if len(match) != 0 else None


def get_vk_id(message: str) -> Optional[int]:
    """Return vk_id form any message with mentions.
    Args:
        message: The message with vk mentions.
    Return:
        First vk id in the message or None if not matching.
    """
    return int(_match(REGEX_PATTERNS.VK_ID, message, "VK ID"))


def get_steamid(message: str) -> Optional[int]:
    """Return steamid from magic bot message.

    Args:
        message: The message with steamid
    Return:
        steamid from magic bot message or None if not matching.
    """
    return int(_match(REGEX_PATTERNS.STEAMID, message, "steamid"))


def get_player_name(message: str) -> Optional[str]:
    """Return player name from magic bot message.

    Args:
        message: The message from the bot when starting/cancelling/banning check

    Return:
        player name from magic bot message or None if not matching.
    """
    player_name = _match(REGEX_PATTERNS.PLAYER_NAME, message, "player name")
    return player_name.replace(" ", "")


def get_server_number(message: str) -> Optional[int]:
    """Return server number from magic bot message

    Args:
        message: The message from the bot when starting checks

    Return:
        server number from magic bot message or None if not matching.
    """

    return int(_match(REGEX_PATTERNS.SERVER_NUMBER, message, "server number"))


def is_string_is_date(string: str) -> bool:
    if re.match(REGEX_PATTERNS.STRING_IS_DATE, string):
        return True
    return False
