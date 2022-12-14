import os

import vkbottle

from app.storage import database_controller as db_cntrl


class AppContext:
    def __init__(self) -> None:
        self.vk_api = vkbottle.API(token=os.getenv("VK_API_TOKEN"))
        self.redis = db_cntrl.RedisController()
        self.postgres = db_cntrl.PostgresController()

    async def on_startup(self, app=None) -> None:  # type: ignore
        self.postgres.create_table()

    async def on_shutdown(self, app=None) -> None:  # type: ignore
        pass
