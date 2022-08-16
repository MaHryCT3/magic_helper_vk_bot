import abc

from app import models
from app.context import AppContext


class BaseHandler(abc.ABC):
    async def __call__(
        self, data: models.VKEventData, ctx: AppContext, *args, **kwargs
    ):
        await self.handle(data, ctx)

    @abc.abstractmethod
    async def handle(self, data: models.VKEventData, ctx: AppContext):
        raise NotImplemented
