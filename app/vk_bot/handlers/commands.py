import abc
from typing import NamedTuple

from loguru import logger
from vkbottle import VKAPIError

from app import models
from app.context import AppContext
from app.vk_bot.handlers.abc import BaseHandler
from app.utils import checks, messages
from app.exceptions import ParamsError
import random


class CheckParams(NamedTuple):
    server_number: int
    steamid: int


class Cmd(BaseHandler):
    pass


class GetChecksCmd(Cmd):
    async def handle(self, data: models.VKEventData, ctx: AppContext):
        try:
            checks_count = checks.get_checks_count(data, ctx)
        except ParamsError:
            msg = "Какая-то ошибка с параметрами, когда то здесь появится объяснения. А пока просто попробуй еще раз"
        else:
            msg = checks_count

        try:
            await messages.send(ctx.vk_api, msg, data.chat_id)
        except VKAPIError as e:
            logger.error(f"Error with send message {e.code}")


### Ниже обработка команд которые адресованы боту меджик раста ###


# TODO: Вынести всю логику отсюда мудак
class CheckCmd(BaseHandler):
    def _parse_params(self, message: str) -> CheckParams:
        params = message.split(" ", maxsplit=2)
        return CheckParams(
            server_number=params[1],
            steamid=params[2],
        )

    def _update_check_stage(
        self, ctx: AppContext, params: CheckParams, check_stage: models.CheckStage
    ):
        logger.debug(
            f"In update check stage func. Params = {params} check_stage = {check_stage}"
        )

        player_name = ctx.redis.get_player_name(params.steamid)
        logger.debug(f"player_name = {player_name}")
        ctx.redis.edit_check_stage(player_name, check_stage)

        logger.info(f"Check {params.steamid} is will {check_stage} soon")


class StopCheckCmd(CheckCmd):
    async def handle(self, data: models.VKEventData, ctx: AppContext):
        params = self._parse_params(data.text)
        self._update_check_stage(ctx, params, "Ended")


class CancelCheckCmd(CheckCmd):
    async def handle(self, data: models.VKEventData, ctx: AppContext):
        params = self._parse_params(data.text)
        self._update_check_stage(ctx, params, "Cancelled")


class BanCheckCmd(CheckCmd):
    async def handle(self, data: models.VKEventData, ctx: AppContext):
        params = self._parse_params(data.text)
        self._update_check_stage(ctx, params, "Ended")
