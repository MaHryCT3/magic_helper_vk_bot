from typing import NamedTuple
import re

from loguru import logger
import pendulum
from pendulum.datetime import DateTime

from app import models
from app.helpers import constants
from app.helpers import regex_parser


class MonthYear(NamedTuple):
    month: int
    year: int


def _get_start_month_and_year(date: pendulum.DateTime) -> MonthYear:
    if date.day <= constants.DAY_WORK_MONTH_END:
        date = date.subtract(month=1)
    return MonthYear(month=date.month, year=date.year)


def _get_time_start(date: pendulum.DateTime) -> pendulum.DateTime:
    m_y = _get_start_month_and_year(date)
    return pendulum.datetime(
        year=m_y.year, month=m_y.month, day=constants.DAY_WORK_MONTH_END
    )


def _time_interval_model(start, end) -> models.TimeInterval:
    return models.TimeInterval(
        start=start,
        end=end,
    )


def get_all_time_interval() -> models.TimeInterval:
    start = pendulum.datetime(2020, 1, 1)
    end = pendulum.datetime(3000, 1, 1)
    return _time_interval_model(
        start=start,
        end=end,
    )


def get_current_work_month_time_interval() -> models.TimeInterval:
    """Return work-month time intraval
    Example
    --------
    const DAY_WORK_MONTH_END = 9
    Date 30.08.2022 -> Return 09.08.2022 - 30.08.2022
    Date 1.10.2022 -> Return 09.09.2022 -  1.10.2022
    Date 15.02.2022 -> Return 09.02.2022 - 15.02.2022
    Date 8.05.2022 -> Return 09.04.2022 - 08.05.2022
    """
    time_now = pendulum.now(tz=constants.TZ)
    start = _get_time_start(time_now)
    end = time_now
    return _time_interval_model(start, end)


def get_today_time_interval() -> models.TimeInterval:
    """Return today TimeInterval"""
    time_now = pendulum.now(tz=constants.TZ)
    start = pendulum.datetime(time_now.year, time_now.month, time_now.day)
    end = start.add(hours=24)
    return _time_interval_model(start, end)


def get_time_interval_from_string(
    string: str, format: str = constants.STRING_DATE_FORMAT, sep: str = "-"
) -> models.TimeInterval:
    """Get time interval from string

    Args:
        string: string with date, like 11.11.2022{sep}24.12.2022
        format: string with format instruction, located in constants
        sep: separtor between dates
    """
    times = string.split(sep)
    start = pendulum.from_format(times[0], format)
    end = pendulum.from_format(times[1], format)
    return _time_interval_model(start, end)


def parse_time_interval_from_string(string: str) -> models.TimeInterval | None:
    logger.debug(f"in parse time interval from string string - {string}")
    if regex_parser.is_string_is_date(string):
        return get_time_interval_from_string(string)

    if is_word_mean_time(string):
        return get_time_interval_from_word(string)

    return None


def get_time_interval_from_word(word: str) -> models.TimeInterval | None:
    if word == "today":
        return get_today_time_interval()

    if word == "gg":
        return get_current_work_month_time_interval()

    if word == "all":
        return get_all_time_interval()

    return None


def is_word_mean_time(word) -> bool:
    """Checks if word is mean time interval

    Return:
        True if word is mean time interval
    """
    words_mean_time = ["today"]
    if word in words_mean_time:
        return True
    return False


def is_word_mean_unique_time(word) -> bool:
    word_mean_unique_time = ["gg", "all"]
    if word in word_mean_unique_time:
        return True
    return False


# TODO: СДелать что то вроде gg-1 gg-2 и всякое такое, чтобы прошлые месяца чекать
