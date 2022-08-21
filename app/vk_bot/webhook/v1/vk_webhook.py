import asyncio

from aiohttp import web

from loguru import logger

from app import models
from app.context import AppContext
from app.vk_bot.events import Event

from app.vk_bot.handlers import *  # init handlers  # FIXME: хуйня так то какая то


async def handle(request: web.Request, ctx: AppContext) -> web.Response:
    try:
        data = models.VKEventData.from_json(await request.json())
    except Exception:
        logger.error(f"Error when trying to get event data {request.text}")
    handler = Event.find_handler(data)
    if handler is not None:
        asyncio.get_running_loop().create_task(handler(data=data, ctx=ctx))
    return web.Response(text="ok", status=200)
