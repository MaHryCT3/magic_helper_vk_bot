from __future__ import annotations

import dataclasses
import typing as tp


from pendulum.datetime import DateTime

from app.exceptions import VKJsonError, NotSupportedEvent

vk_callback_dict: tp.TypeAlias = dict

CheckStage = tp.Literal["Process", "Ended", "Cancelled"]


@dataclasses.dataclass
class ChecksCount:
    moder: Moderator
    checks_count: int = None
    checks_ban: int = None


@dataclasses.dataclass
class VKUser:
    id_: int
    name: tp.Optional[str] = None
    surname: tp.Optional[str] = None

    def __repr__(self) -> str:
        return f"{self.name} {self.surname}"


class Moderator(VKUser):
    steamid: tp.Optional[int] = None


@dataclasses.dataclass
class TimeInterval:
    start: DateTime
    end: DateTime


@dataclasses.dataclass
class CheckInfo:
    steamid: int
    player_name: str = None
    moder_vk: int = None
    start_time: DateTime = None
    end_time: DateTime = None
    server_number: int = None
    is_ban: bool = False

    @classmethod
    def from_db(cls, row):
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
    chat_id: tp.Optional[int] = None
    text: tp.Optional[str] = None

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
