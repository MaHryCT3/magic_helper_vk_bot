from __future__ import annotations

from typing import Callable, Optional, TypeVar

from loguru import logger

from app import models

RT = TypeVar("RT")  # return type

__all__ = (
    "Event",
    "on_cmd",
    "on_message",
)


class Event:
    _commands_events: list[Event] = []
    _messages_events: list[Event] = []

    def __init__(
        self,
        handler: Callable,
        signs: list[str | list[str]],
        on_cmd: bool = False,
        on_message: bool = False,
    ) -> None:
        self.handler: Callable = handler
        self.signs: list[str | list[str]] = signs

        if on_cmd:
            self._new_command_event()
        elif on_message:
            self._new_message_event()

    def _new_command_event(self) -> None:
        self._commands_events.append(self)

    def _new_message_event(self) -> None:
        self._messages_events.append(self)

    @classmethod
    def find_handler(cls, vk_data: models.VKEventData) -> Optional[Callable]:
        """Try find a handler in all events

        Args:
            vk_data: event data from vk
        Return
            Handler that will be called or None if no handler is found
        """
        text = vk_data.text
        if cls.is_cmd(text):
            # Get only cmd from all message. Example: /`checks` all.
            cmd = text[1:].split(" ")[0]
            for event in cls._commands_events:
                if event.check_signs(cmd):
                    return event.handler
        else:
            for event in cls._messages_events:
                if event.check_signs(text):
                    return event.handler
        return None

    @staticmethod
    def is_cmd(message: str) -> bool:
        """Check if message is a command"""
        try:
            first_symbol = message[0]
        except Exception:
            return False
        else:
            if first_symbol == "/":
                return True
            return False

    def check_signs(self, message: str) -> bool:
        """Checks matches signs in message

        Args:
            message: message where trying finding a signs
        Return:
            True if message matches else False
        """
        logger.debug(f"Checking signs in {message}")
        for sign in self.signs:
            if isinstance(sign, list):
                if self._check_signs_in_list(message, sign):
                    return True
            else:
                if sign in message:
                    return True

        logger.debug(f"Not found sign in {message}")
        return False

    def _check_signs_in_list(self, message: str, signs: list[str]) -> bool:
        """Checks if the all given signs are in the message

        Args:
            message: The message to check
            signs: The signs to check
        Returns:
            True: If all the signs are in the message
            False: If all the signs are not in the message

        """
        for sign in signs:
            if sign not in message:
                return False
        return True


def on_cmd(signs: list[str | list[str]]):  # type: ignore
    """Decorator to add a new command handler to events

    Args:
        handler: handler for given signs
        signs: The signs of handler
    """

    def decorator(cls: Callable[..., Callable]) -> None:
        Event(handler=cls(), signs=signs, on_cmd=True)
        return None

    return decorator


def on_message(signs: list[str | list[str]]):  # type: ignore
    """Decorator to add a new message handler to events

    Args:
        handler: handler for given signs
        signs: The signs of handler
    """

    def decorator(cls: Callable[..., Callable]) -> None:
        Event(handler=cls(), signs=signs, on_message=True)
        return None

    return decorator
