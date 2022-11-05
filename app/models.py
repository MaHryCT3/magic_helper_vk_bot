from __future__ import annotations

import dataclasses
from typing import Optional, TypeAlias, Literal

import pendulum

from app.exceptions import NotSupportedEvent, VKJsonError
from app.helpers import constants

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
    group_id: int
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
            group_id=json["group_id"],
            event_type=event_type,
            date=DateTime.fromtimestamp(event_info.get("date")),
            user_id=event_info.get("from_id"),
            chat_id=event_info.get("peer_id"),
            text=event_info.get("text"),
        )


@dataclasses.dataclass
class PlayerStats:
    steamid: int = 0
    kill: int = 0
    death: int = 0
    kd: float = 0
    headshot: int = 0

    @classmethod
    def from_json(cls, json: dict) -> PlayerStats:
        kill: int = json.get("kp_total", 0)  # type: ignore
        death: int = json.get("d_player", 0)  # type: ignore
        kd = kill / death if death != 0 else kill
        return cls(
            steamid=json.get("steamid", 0),  # type: ignore
            kill=kill,
            death=death,
            kd=kd,
            headshot=json.get("kp_head", 0),  # type: ignore
        )


@dataclasses.dataclass
class PlayerInfo:
    steamid: int
    ip: str
    nickname: str
    server: int
    join_time: DateTime
    vk: int
    stats: Optional[PlayerStats] = None

    @classmethod
    def from_json(cls, json: list) -> list[PlayerInfo]:
        players = []
        for player_json in json:
            players.append(
                cls(
                    steamid=int(player_json.get("id")),  # type: ignore
                    ip=player_json.get("ip"),  # type: ignore
                    nickname=player_json.get("nickname"),  # type: ignore
                    server=int(player_json.get("server")),  # type: ignore
                    join_time=pendulum.from_timestamp(int(player_json.get("firstjoin")), tz=constants.TZ),  # type: ignore
                    vk=player_json.get("vk"),  # type: ignore
                )
            )
        return players
