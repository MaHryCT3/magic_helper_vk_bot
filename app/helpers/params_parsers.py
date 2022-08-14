from loguru import logger

from app.helpers.params_models import ChecksParams
from app.helpers import regex_parser
from app.helpers import time_help
from app.helpers.constants import REGEX_PATTERNS
from app.helpers import constants
from app import models


# TODO: Я больше никогда не скажу тебе-е-е, что я загадал


def _get_check_params(data: models.VKEventData) -> ChecksParams:
    params = data.text.split(" ")
    params.pop(0)  # remove cmd

    moder_vk = data.user_id
    time_interval = time_help.get_today_time_interval()

    if not params:
        pass

    elif time_help.is_word_mean_unique_time(params[0]):
        time_interval = time_help.get_time_interval_from_word(params[0])
        moder_vk = None

    else:
        vk_id = regex_parser.get_vk_id(params[0])
        if vk_id is not None:
            moder_vk = vk_id

    return ChecksParams(moder_vk=moder_vk, time_interval=time_interval)


def parse_check_params(data: models.VKEventData) -> ChecksParams | None:
    """Parse parameters from vk event data. Return ChecksParams model

    Examples:
        /checks -> return ur today checks count.
        /checks gg -> return all checks from this work month.
        /checks @user -> return today checks count @user.

    Args:
        data - data from vk
    Return:
        params_models.ChecksParams or None if check can't get check parameters from this data.
    """
    try:
        return _get_check_params(data)
    except Exception as e:
        logger.debug(e)
        return None
