from typing import Optional

import pendulum
from loguru import logger

from app.context import AppContext
from app.exceptions import CantGetChecksInfo
from app.helpers import params_models as p_models
from app.helpers.params_parsers import parse_get_check_count_params
from app.helpers import constants
from app import models

__all__ = [
    "get_checks_count",
    "record_check_info_to_db",
    "define_check_stage",
    "complete_check",
]


def get_checks_count(params: p_models.GetChecksParameters, ctx: AppContext) -> int:
    """Return check count from database

    Raise ParamsError if params is invalid
    """
    try:
        check_count = ctx.postgres.get_count_checks_by_time_interval(
            time_interval=params.time_interval,
            moder_vk=params.moder_vk,
        )
    except Exception as e:
        logger.critical(f"Cant get check info from database {e}")
        raise CantGetChecksInfo
    logger.info(f"Returns checks count by params {params}: {check_count}")
    return check_count


def record_check_info_to_db(ctx: AppContext, check_info: models.CheckInfo):
    """Record new row to database with check info

    Args:
        ctx: AppContext
        check_info: instance of CheckInfo
    """
    row_id = ctx.postgres.new_check(check_info)
    ctx.redis.new_check(
        player_name=check_info.player_name,
        steamid=check_info.steamid,
        db_row_id=row_id,
    )
    logger.info(f"New record in database with params - {check_info}")


def update_check_stage(
    ctx: AppContext,
    params: p_models.ChecksCmdParams,
    check_stage: models.CheckStage,
):
    """Update check stage to player

    Args:
        ctx: AppContext
        params: User parameters
        check_stage: What stage to change
    """
    player_name = ctx.redis.get_player_name(params.steamid)
    ctx.redis.edit_check_stage(player_name, check_stage)
    logger.info(f"Update check stage for {player_name} to {check_stage}")


def define_check_stage(
    ctx: AppContext, player_name: str
) -> Optional[models.CheckStage]:
    """Return player check stage.

    Args:
        ctx: AppContext
        plaeyr_name: name of player under review

    Return:
        Player check stage or None if player not found
    """
    check_stage = ctx.redis.get_check_stage(player_name)
    logger.info(f"Returns check stage for {player_name}: {check_stage}")
    return check_stage


def complete_check(
    ctx: AppContext,
    player_name: str,
    check_stage: models.CheckStage,
    is_ban: bool = False,
):
    """Performs database operations to complete the check.

    Update row with player name if checks is not cancelled.
    Clean redis data.

    Args:
        ctx: AppContext
        player_name: player name under review
        check_stage: Stage of check
        is_ban(Optional): is the player banned
    """
    if check_stage == "Ended":
        _update_check_if_ended(ctx, player_name, is_ban)
    logger.info(
        f"Check is {check_stage} for {player_name} {'and banned' if is_ban else ''}"
    )
    _clear_redis_data(ctx, player_name)


def _update_check_if_ended(ctx: AppContext, player_name: str, is_ban: bool):
    """Update database row with player name if check is end.

    Note: If check is cancelled (etc /cc3) check is not ended.
    """
    row_id = ctx.redis.get_db_row_id(player_name)
    ctx.postgres.edit_check_end(row_id, pendulum.now(tz=constants.TZ))
    ctx.postgres.edit_is_ban(row_id, is_ban)


def _clear_redis_data(ctx: AppContext, player_name: str):
    """Clear redis data after checks is comleted"""
    ctx.redis.clear_data(player_name)
