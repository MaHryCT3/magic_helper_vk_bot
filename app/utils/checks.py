from app.context import AppContext
from app.exceptions import ParamsError
from app.helpers.params_models import ChecksParams
from app.helpers.params_parsers import parse_check_params
from app.models import VKEventData


def get_checks_count(data: VKEventData, ctx: AppContext) -> int:
    """Return check count from database

    Raise ParamsError if params is invalid
    """
    params = parse_check_params(data)
    if params is None:
        raise ParamsError
    check_count = ctx.postgres.get_count_checks_by_time_interval(
        time_interval=params.time_interval,
        moder_vk=params.moder_vk,
    )
    return check_count
