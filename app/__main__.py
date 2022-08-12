from aiohttp import web
import asyncio
import os

from loguru import logger

from app.context import AppContext
from app.vk_bot import routes


logger.add(
    "logs.log",
    format="{time:HH:mm::ss} {name}:{function}:{line} {level} - {message}",
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    colorize=True,
    level=os.getenv("LOGURU_LEVEL", "INFO"),
)


async def create_app():
    app = web.Application()

    ctx = AppContext()

    app.on_startup.append(ctx.on_startup)
    app.on_shutdown.append(ctx.on_shutdown)

    routes.setup_webhook(app, ctx)

    return app


def main():
    app = asyncio.get_event_loop().run_until_complete(create_app())

    logger.info("Application starting...")
    web.run_app(
        app,
        port=int(os.getenv("PORT", 8080)),
        access_log=logger,
    )


if __name__ == "__main__":
    main()
