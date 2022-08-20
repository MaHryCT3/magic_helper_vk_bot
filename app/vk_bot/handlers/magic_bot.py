import re
from loguru import logger

import pendulum

from app.helpers import constants
from app.helpers import regex_parser
from app.helpers import params_parsers as p_parsers
from app.utils import checks
from app.context import AppContext
from app.vk_bot.handlers.abc import BaseHandler
from app.exceptions import NotFoundPattern
from app import models


class CheckCmds(BaseHandler):
    pass


### Ниже обработка команд которые адресованых боту меджик раста ###


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


class MagicBotHandler(BaseHandler):
    pass


## Ниже обработка сообщений от бота мейджик раста##


class StartCheck(MagicBotHandler):
    def _collect_check_data(self, message: str) -> models.CheckInfo:
        moder_vk = regex_parser.get_vk_id(message)
        player_name = regex_parser.get_player_name(message)
        steamid = regex_parser.get_steamid(message)
        server_number = regex_parser.get_server_number(message)
        return models.CheckInfo(
            steamid=steamid,
            player_name=player_name,
            moder_vk=moder_vk,
            start_time=pendulum.now(tz=constants.TZ),
            server_number=server_number,
        )

    async def handle(self, data: models.VKEventData, ctx: AppContext):
        message = data.text
        check_data = self._collect_check_data(message)
        checks.record_check_info_to_db(ctx, check_data)

        logger.info(f"Start check {check_data}")


class StopCheck(MagicBotHandler):
    async def handle(self, data: models.VKEventData, ctx: AppContext):
        player_name = regex_parser.get_player_name(data.text)
        check_stage = checks.define_check_stage(ctx, player_name)
        checks.complete_check(ctx, player_name, check_stage=check_stage)


class BanCheck(MagicBotHandler):
    async def handle(self, data: models.VKEventData, ctx: AppContext):
        player_name = regex_parser.get_player_name(data.text)
        check_stage = checks.define_check_stage(ctx, player_name)
        checks.complete_check(ctx, player_name, check_stage=check_stage, is_ban=True)

    # TODO: Добавить игнорирование проверок при бане за игру с читером
