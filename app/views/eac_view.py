from calendar import c
from typing import Union

from eac_info.model import EACInfo

from app.helpers import params_models as p_models
from app import models


__all__ = ["get_eac_view"]


def get_eac_view(eac_info: EACInfo) -> str:
    """Return text for user message with eac information.

    Args:
        eac_info: eac info received from eac info package
    Return:
        text for user message
    """
    if eac_info.is_ban:
        cap = f"{eac_info.steamid} - получал EAC блокировку🚫\n"
        body = _get_body(eac_info)
        text = cap + body
    else:
        text = f"{eac_info.steamid} - не получал EAC блокировок✅."
    return text


def _get_body(eac_info: EACInfo) -> str:
    body = f"Прошло {eac_info.days_since_ban} дней c бана\n\n"
    body += f"Твиттер: {eac_info.post_link}\n"
    body += f"Nexus: {eac_info.nexus_link}"
    return body


# TODO: Добавить какие то смайлики для разного кол-ва дней
