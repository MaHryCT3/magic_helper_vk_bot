from loguru import logger

from vkbottle import VKAPIError

from eac_info import get_eac_info
from eac_info.exceptions import SteamIsNotFound

from app import models
from app import views
from app.context import AppContext
from app.exceptions import ParamsError
from app.helpers import params_parsers as p_parsers
from app.utils import checks, vk, magic
from app.vk_bot.handlers.abc import BaseHandler
from app.helpers import players as players_helpers

from app.vk_bot import events

__all__ = ("GetChecksCmd",)


class Cmd(BaseHandler):
    pass


@events.on_cmd(signs=["checks"])
class GetChecksCmd(Cmd):
    async def handle(self, data: models.VKEventData, ctx: AppContext) -> None:
        try:
            params = p_parsers.parse_get_check_count_params(data)
        except ParamsError:
            msg = "Какая-то ошибка с параметрами, когда то здесь появится объяснения. А пока просто попробуй еще раз"

        try:
            checks_count = await checks.get_checks_count(params, ctx)
        except Exception as e:
            msg = "Произошла непредвиденная ошибка, скорее всего нету доступа к базе данных."
            logger.error(e)
        else:
            msg = views.get_check_view(checks_count=checks_count, params=params)

        try:
            await vk.send_message(ctx.vk_api, msg, data.chat_id)
        except VKAPIError as e:
            logger.critical(f"Error with send message {e.code}")


@events.on_cmd(signs=["иак", "eac"])
class GetEacInfoCmd(Cmd):
    async def handle(self, data: models.VKEventData, ctx: AppContext) -> None:
        try:
            params = p_parsers.parse_eac_params(data)
        except ParamsError:
            msg = "Информация об иаке пользователя.\n/eac [steamid]"

        try:
            eac_info = await get_eac_info(params.steamid)
        except:
            msg = "Информации об данном аккаунте не найдено, проверьте правильность данных"
        else:
            msg = views.get_eac_view(eac_info)

        try:
            await vk.send_message(ctx.vk_api, msg, data.chat_id)
        except VKAPIError as e:
            logger.critical(f"Error with send message {e.code}")


@events.on_cmd(signs=["новые", "new", "пидорасы", "туц"])
class GetNewPlayersCmd(Cmd):
    async def handle(self, data: models.VKEventData, ctx: AppContext) -> None:

        try:
            new_players = await magic.get_new_online_players()
        except:
            msg = "Не удалось получить список игроков"
            return await vk.send_message(ctx.vk_api, msg, data.chat_id)

        try:
            new_players_info = await magic.get_stats_from_players(new_players)
        except:
            msg = "Не удалось получить статистику игроков"
            return await vk.send_message(ctx.vk_api, msg, data.chat_id)

        new_players_info = players_helpers.filter_bad_stats(new_players_info)
        new_players_info = players_helpers.sorted_by_kd(new_players_info)

        msg = views.get_new_players_view(new_players_info)
        return await vk.send_message(ctx.vk_api, msg, data.chat_id)
