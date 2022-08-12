from aiohttp import web

from app.vk_bot.webhook.v1 import vk_webhook
from app.context import AppContext


def wrap_handler(handler, context):
    async def wrapper(request):
        return await handler(request, context)

    return wrapper


def setup_webhook(app: web.Application, ctx: AppContext):
    app.router.add_post(
        "/v1/vkbot",
        wrap_handler(
            vk_webhook.handle,
            ctx,
        ),
    )
