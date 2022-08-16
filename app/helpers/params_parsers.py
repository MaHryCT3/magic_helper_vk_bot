from typing import Optional

from loguru import logger

from app.helpers import regex_parser
from app.helpers import time_help
from app.helpers import params_models as p_models
from app.helpers.constants import REGEX_PATTERNS
from app.helpers import constants
from app.exceptions import ParamsError
from app import models


__all__ = [
    "parse_get_check_count_params",
    "parse_check_params",
    "parse_ban_params",
]


# def _get_check_count_params(data: models.VKEventData) -> p_models.GetChecksParameters:
#     params = data.text.split(" ")
#     params.pop(0)  # remove cmd

#     moder_vk = data.user_id
#     time_interval = time_help.get_today_time_interval()

#     if not params:
#         pass

#     elif time_help.is_word_mean_unique_time(params[0]):
#         time_interval = time_help.get_time_interval_from_word(params[0])
#         moder_vk = None

#     else:
#         vk_id = regex_parser.get_vk_id(params[0])
#         if vk_id is not None:
#             moder_vk = vk_id

#     return p_models.GetChecksParameters(moder_vk=moder_vk, time_interval=time_interval)


def _get_check_count_params(data: models.VKEventData) -> p_models.GetChecksParameters:
    params = data.text.split(" ")
    params.pop(0)  # remove cmd

    moder_vk = None
    time_interval = time_help.get_current_work_month_time_interval()

    return p_models.GetChecksParameters(moder_vk=moder_vk, time_interval=time_interval)


def parse_get_check_count_params(
    data: models.VKEventData,
) -> Optional[p_models.GetChecksParameters]:
    """Parse parameters from vk event data. Return GetChecksParams model

    Examples:
        /checks -> return ur today checks count.
        /checks gg -> return all checks from this work month.
        /checks @user -> return today checks count @user.

    Args:
        data - data from vk
    Return:
        p_models.GetChecksParameters or None if check can't get check parameters from this data.
    """
    try:
        return _get_check_count_params(data)
    except Exception as e:
        logger.error(e)
        raise ParamsError


def parse_check_params(data: models.VKEventData) -> p_models.ChecksCmdParams:
    """Parse parameters for command /cc /cc2 /cc3.

    Args:
        data: vk event data

    Return:
        Check cmd params model instance

    """
    params = data.text.split(" ")
    params.pop(0)  # remove cmd
    if len(params) < 2:
        raise ParamsError
    return p_models.ChecksCmdParams(
        server_number=params[0],
        steamid=params[1],
    )


def parse_ban_params(data: models.VKEventData) -> p_models.BanCmdParams:
    """Parse parameters for command /ban.

    Args: vk event data

    Return:
        Ban cmd params model instance
    """
    params = data.text.split(" ", maxsplit=3)
    params.pop(0)  # remove cmd
    if len(params) < 2:
        raise ParamsError
    return p_models.BanCmdParams(
        server_number=params[0],
        steamid=params[1],
        reason=(params[2] if len(params) == 3 else "Забанен по результатам проверки."),
    )


# TODO: Сделать общую реализацию для всех парсеров
