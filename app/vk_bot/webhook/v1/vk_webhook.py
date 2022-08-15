from aiohttp import web
import asyncio
import os

from loguru import logger

from app import models
from app.context import AppContext
from app.vk_bot.events import get_handler


async def handle(request: web.Request, ctx: AppContext) -> web.Response:
    try:
        data = models.VKEventData.from_json(await request.json())
    except:
        logger.error(f"Error when trying to get event data {request.text}")
    handler = get_handler(data)
    if handler is not None:
        asyncio.get_running_loop().create_task(handler(data=data, ctx=ctx))
    return web.Response(text="ok", status=200)
