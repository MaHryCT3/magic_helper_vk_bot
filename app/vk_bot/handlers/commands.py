import abc
from typing import NamedTuple

from loguru import logger
from vkbottle import VKAPIError

from app import models
from app.helpers import params_parsers as p_parsers
from app.context import AppContext
from app.vk_bot.handlers.abc import BaseHandler
from app.utils import checks, messages
from app.exceptions import ParamsError
import random


class Cmd(BaseHandler):
    pass


class GetChecksCmd(Cmd):
    async def handle(self, data: models.VKEventData, ctx: AppContext):
        try:
            params = p_parsers.parse_get_check_count_params(data)
        except ParamsError:
            msg = "Какая-то ошибка с параметрами, когда то здесь появится объяснения. А пока просто попробуй еще раз"
        try:
            checks.get_checks_count(params, ctx)
        except Exception as e:
            msg = "Произошла непредвиденная ошибка, скорее всего нету доступа к базе данных."
        try:
            await messages.send(ctx.vk_api, msg, data.chat_id)
        except VKAPIError as e:
            logger.error(f"Error with send message {e.code}")


### Ниже обработка команд которые адресованы боту меджик раста ###


class CheckCmds(BaseHandler):
    pass


class StopCheckCmd(CheckCmds):
    async def handle(self, data: models.VKEventData, ctx: AppContext):
        params = p_parsers.parse_check_params(data)
        checks.update_check_stage(ctx, params, "Ended")


class CancelCheckCmd(CheckCmds):
    async def handle(self, data: models.VKEventData, ctx: AppContext):
        params = p_parsers.parse_check_params(data)
        checks.update_check_stage(ctx, params, "Cancelled")


class BanCheckCmd(CheckCmds):
    async def handle(self, data: models.VKEventData, ctx: AppContext):
        params = p_parsers.parse_ban_params(data)
        checks.update_check_stage(ctx, params, "Ended")
