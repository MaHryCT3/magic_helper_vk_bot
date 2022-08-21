from __future__ import annotations

import dataclasses
from typing import Optional, TypeAlias, Literal

from app.exceptions import NotSupportedEvent, VKJsonError

from pendulum.datetime import DateTime


vk_callback_dict: TypeAlias = dict

CheckStage = Literal["Process", "Ended", "Cancelled"]


@dataclasses.dataclass
class ChecksCount:
    moder: Moderator
    checks_count: Optional[int] = None
    checks_ban: Optional[int] = None


@dataclasses.dataclass
class VKUser:
    id_: int
    name: Optional[str] = None
    surname: Optional[str] = None

    def __repr__(self) -> str:
        return f"{self.name} {self.surname}"


class Moderator(VKUser):
    steamid: Optional[int] = None


@dataclasses.dataclass
class TimeInterval:
    start: DateTime
    end: DateTime


@dataclasses.dataclass
class CheckInfo:
    steamid: int
    player_name: Optional[str] = None
    moder_vk: Optional[int] = None
    start_time: Optional[DateTime] = None
    end_time: Optional[DateTime] = None
    server_number: Optional[int] = None
    is_ban: bool = False

    @classmethod
    def from_db(cls, row) -> CheckInfo:  # type: ignore
        return cls(
            steamid=row.steamid,
            moder_vk=row.moder_vk,
            start_time=row.start_time,
            end_time=row.end_time,
            server_number=row.server_number,
            is_ban=row.is_ban,
        )


@dataclasses.dataclass
class VKEventData:
    event_type: str
    user_id: int
    date: DateTime
    chat_id: Optional[int] = None
    text: Optional[str] = None

    @classmethod
    def from_json(cls, json: vk_callback_dict) -> VKEventData:
        event_type = json.get("type")
        if event_type is None:
            raise VKJsonError("Event type is None")
        elif event_type == "wall_post_new":
            event_info = json["object"]
        elif event_type == "message_new":
            event_info = json["object"]["message"]
        else:
            raise NotSupportedEvent
        return cls(
            event_type=event_type,
            date=DateTime.fromtimestamp(event_info.get("date")),
            user_id=event_info.get("from_id"),
            chat_id=event_info.get("peer_id"),
            text=event_info.get("text"),
        )
