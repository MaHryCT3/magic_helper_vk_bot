from loguru import logger

from vkbottle import VKAPIError

from app import models
from app import views
from app.context import AppContext
from app.exceptions import ParamsError
from app.helpers import params_parsers as p_parsers
from app.utils import checks, vk
from app.vk_bot.handlers.abc import BaseHandler


class Cmd(BaseHandler):
    pass


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
