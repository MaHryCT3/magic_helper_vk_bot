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
    time_interval = time_help.get_current_work_month_time_interval()

    if len(params) == 2:
        time_interval = time_help.parse_time_interval_from_string(params[1])
        moder_vk = regex_parser.get_vk_id(params[0])

    elif len(params) == 1:

        if time_help.is_word_mean_unique_time(params[0]):
            time_interval = time_help.get_time_interval_from_word(params[0])
            moder_vk = None

        if time_help.is_word_mean_time(params[0]):
            time_interval = time_help.get_time_interval_from_word(params[0])

    return ChecksParams(
        moder_vk=moder_vk,
        time_interval=time_interval,
    )


def parse_check_params(data: models.VKEventData) -> ChecksParams | None:
    """
    /checks "@user=автор" "time=gg"
    /checks -> Твои проверки за рабочий месяц
    /checks today-> Твои проверки за сегодня
    /checks @mahryct today -> Проверки @ за день
    /checks @mahryct 10.10.2022-12.10.2022 -> Провери за указанный срок,
    /checks gg -> Все проверки за рабочий месяц
    /checks all -> Проверки за все время работы бота
    """
    try:
        return _get_check_params(data)
    except Exception as e:
        logger.debug(e)
        return None
