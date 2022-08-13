import re
from loguru import logger

import pendulum

from app.helpers import constants
from app.context import AppContext
from app.vk_bot.handlers.abc import BaseHandler
from app.exceptions import NotFoundPattern
from app import models

# TODO: Вынести всю логику отсюда


class MagicBotHandler(BaseHandler):
    def _get_steamid(self, text: str) -> int:
        re_pattern = r"/cc2 \d{,2} (\d+) для"
        match = re.findall(re_pattern, text)
        if not match:
            logger.error(f"Не было найдено стимайди в строке{text}")
            raise NotFoundPattern
        return match[0]

    def _get_player_name(self, text: str) -> str:
        re_pattern = r"Ответ:\s(.+)\s[бвз]"
        match = re.findall(re_pattern, text)
        if not match:
            logger.error(f"Не было найдено ника в строке{text}")
            raise NotFoundPattern
        return match[0]

    def _get_vk_id(self, text: str) -> int:
        re_pattern = r"\[id(\d+)\|"
        match = re.findall(re_pattern, text)
        if not match:
            logger.error(f"Не было найдено вк айди в строке{text}")
            raise NotFoundPattern
        return int(match[0])

    def _get_server_number(self, text: str) -> int:
        re_pattern = r"/cc2\s(\d+)\s"
        match = re.findall(re_pattern, text)
        if not match:
            logger.error(f"Не было найдено вк айди в строке{text}")
            raise NotFoundPattern
        return match[0]

    def _clear_redis_data(self, ctx: AppContext, player_name: str):
        ctx.redis.clear_data(player_name)

        logger.info(f"Clear redis data for {player_name}")

    def _to_complete_check(
        self,
        ctx: AppContext,
        player_name: str,
        check_stage: models.CheckStage,
        is_ban: bool = False,
    ):
        if check_stage == "Ended":
            row_id = ctx.redis.get_db_row_id(player_name)
            ctx.postgres.edit_check_end(row_id, pendulum.now(tz=constants.TZ))
            if is_ban:
                ctx.postgres.edit_is_ban(row_id, is_ban=is_ban)

        self._clear_redis_data(ctx, player_name)
        logger.info(f"Check {player_name} completed.")

    def _define_check_stage(
        self, ctx: AppContext, player_name: str
    ) -> models.CheckStage:
        return ctx.redis.get_check_stage(player_name)


# TODO: DRY


class StartCheck(MagicBotHandler):
    def _collect_check_data(self, message: str) -> models.CheckInfo:
        moder_vk = self._get_vk_id(message)
        player_name = self._get_player_name(message)
        steamid = self._get_steamid(message)
        server_number = self._get_server_number(message)
        return models.CheckInfo(
            steamid=steamid,
            player_name=player_name,
            moder_vk=moder_vk,
            start_time=pendulum.now(tz=constants.TZ),
            server_number=server_number,
        )

    def _record_data_to_db(self, ctx: AppContext, check_info: models.CheckInfo):
        row_id = ctx.postgres.new_check(check_info)
        ctx.redis.new_check(
            player_name=check_info.player_name,
            steamid=check_info.steamid,
            db_row_id=row_id,
        )

    async def handle(self, data: models.VKEventData, ctx: AppContext):
        message = data.text
        check_data = self._collect_check_data(message)
        self._record_data_to_db(ctx, check_data)
        logger.info(f"Start check {check_data}")


class StopCheck(MagicBotHandler):
    async def handle(self, data: models.VKEventData, ctx: AppContext):
        player_name = self._get_player_name(data.text)
        check_stage = self._define_check_stage(ctx, player_name)
        logger.debug(f"Check stage is {check_stage}")
        self._to_complete_check(ctx, player_name, check_stage=check_stage)


class BanCheck(MagicBotHandler):
    async def handle(self, data: models.VKEventData, ctx: AppContext):
        player_name = self._get_player_name(data.text)
        check_stage = self._define_check_stage(ctx, player_name)
        self._to_complete_check(ctx, player_name, check_stage=check_stage, is_ban=True)

    # TODO: Добавить игнорирование проверок при бане за игру с читером
