import re

from loguru import logger

from app.helpers.constants import REGEX_PATTERNS


def get_vk_id(message: str) -> int | None:
    """
    Args:
        message: The message with vk mentions.
    Return:
        First vk id in the message or None if not match.
    """
    match = re.findall(REGEX_PATTERNS.VK_ID, message)
    return int(match[0]) if len(match) != 0 else None


def is_string_is_date(string: str) -> bool:
    logger.debug("IN is_string_is_date")
    if re.match(REGEX_PATTERNS.STRING_IS_DATE, string):
        return True
    return False
