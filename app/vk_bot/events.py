import abc
import typing as tp

from app import models
from app.vk_bot.handlers.abc import BaseHandler
from app.vk_bot.handlers.magic_bot import (
    StartCheck,
    StopCheck,
    BanCheck,
    MagicBotHandler,
)
from app.vk_bot.handlers.commands import StopCheckCmd, CancelCheckCmd, BanCheckCmd


vk_callback_dict: tp.TypeAlias = dict


class Events(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_handler(cls, data: models.VKEventData) -> BaseHandler | None:
        """Интерфейс для предоставления хендлера, по заданной вк модели"""
        raise NotImplementedError


class MagicBotEvent(Events):
    @staticmethod
    def _is_bot_msg(message):
        if "твоя команда выполнена." in message:
            return True
        return False

    @staticmethod
    def _is_start_check(message: str) -> bool:
        if "вызван на проверку" in message and "для отмены проверки." in message:
            return True
        return False

    @staticmethod
    def _is_end_check(message: str) -> bool:
        if "больше не проверяется." in message:
            return True
        return False

    @staticmethod
    def _is_ban_check(message: str) -> bool:
        if "забанен с причиной" in message:
            return True
        return False

    @classmethod
    def get_handler(cls, data: models.VKEventData) -> MagicBotHandler | None:
        message = data.text
        if not cls._is_bot_msg(message):
            return None

        # if cls._is_canceled_raid_check(message):
        #     return CancledRaidCheck

        if cls._is_start_check(message):
            return StartCheck()

        if cls._is_end_check(message):
            return StopCheck()

        if cls._is_ban_check(message):
            return BanCheck()

        return None


class CommandEvent(Events):
    @staticmethod
    def _is_cmd_msg(message: str):
        if message[0] == "/":
            return True
        return False

    @staticmethod
    def _is_end_check(cmd: str):
        if cmd == "cc2":
            return True
        return False

    @staticmethod
    def _is_cancel_check(cmd: str):
        if cmd == "cc3":
            return True
        return False

    def _is_ban_check(cmd: str):
        if cmd == "ban":
            return True
        return False

    @classmethod
    def get_handler(
        cls, data: models.VKEventData
    ) -> StopCheckCmd | CancelCheckCmd | None:
        message = data.text
        if not cls._is_cmd_msg(message):
            return None
        cmd = message.replace("/", "", 1).split(" ")[0]

        if cls._is_end_check(cmd):
            return StopCheckCmd()

        if cls._is_cancel_check(cmd):
            return CancelCheckCmd()

        if cls._is_ban_check(cmd):
            return BanCheckCmd()

        return None


events_typle = (MagicBotEvent, CommandEvent)


def get_handler(data: models.VKEventData) -> BaseHandler | None:
    for event in events_typle:
        handler = event.get_handler(data)
        if handler is not None:
            return handler
    return None
