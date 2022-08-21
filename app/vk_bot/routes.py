from typing import Callable
from collections.abc import Awaitable

from aiohttp import web
from aiohttp.typedefs import Handler

from app.context import AppContext
from app.vk_bot.webhook.v1 import vk_webhook


def wrap_handler(handler, context: AppContext):  # type: ignore
    async def wrapper(request: web.Request):  # type: ignore
        return await handler(request, context)

    return wrapper


def setup_webhook(app: web.Application, ctx: AppContext) -> None:
    app.router.add_post(
        "/v1/vkbot",
        wrap_handler(
            vk_webhook.handle,
            ctx,
        ),
    )
