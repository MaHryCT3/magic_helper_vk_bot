from aiohttp import web
import asyncio
import os

from app import models
from app.context import AppContext
from app.vk_bot.events import get_handler


async def handle(request: web.Request, ctx: AppContext) -> web.Response:
    data = models.VKEventData.from_json(await request.json())
    try:
        handler = get_handler(data)
    except:
        pass
    if handler is not None:
        asyncio.get_running_loop().create_task(handler(data=data, ctx=ctx))
    return web.Response(text="ok", status=200)
