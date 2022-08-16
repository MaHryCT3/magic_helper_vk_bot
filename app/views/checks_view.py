from typing import Union

from app.helpers import params_models as p_models
from app import models

__all__ = ["get_check_view"]


def get_check_view(
    checks_count: Union[list[models.ChecksCount], models.ChecksCount],
    params: p_models.GetChecksParameters,
) -> str:
    """Returns text for user message with checks count

    Args:
        check_count: ChecksCount instance
        params: user parameters
    """
    cap_text = _get_cap_from_time_interval(params)
    body_text = _get_body_from_checks_count(checks_count)
    text = cap_text + "\n\n" + body_text
    return text


def _get_cap_from_time_interval(params: p_models.GetChecksParameters) -> str:
    """Define params type and returns cap with time interval"""
    t_i = params.time_interval
    return f"Статистика по проверкам за {t_i.start.date()} - {t_i.end.date()}"


def _get_body_from_checks_count(
    checks_count: Union[list[models.ChecksCount], models.ChecksCount]
) -> str:
    """Defines checks_count type and returns body of view"""
    if isinstance(checks_count, list):
        return _get_body_from_list(checks_count)
    elif isinstance(checks_count, models.ChecksCount):
        return _get_body_from_model(checks_count)
    else:
        return ""


def _get_body_from_list(checks_count: list[models.ChecksCount]) -> str:
    """Returns body of view from list of checks count"""
    body = ""
    for checks_info in checks_count:
        body += _get_body_from_model(checks_info)
    return body


def _get_body_from_model(check_count: models.ChecksCount) -> str:
    """Return body of view from single model"""
    body = f"{check_count.moder} - 📝{check_count.checks_count} проверок из них {check_count.checks_ban} закончились баном\n"
    return body
