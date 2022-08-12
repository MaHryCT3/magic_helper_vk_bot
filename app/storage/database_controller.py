import datetime
import os
from typing import Literal

import peewee
import redis

from app.storage.orm_models import CheckModel
from app.models import CheckInfo, TimeInterval, CheckStage


class PostgresController:
    def new_check(self, check_info: CheckInfo) -> CheckModel.id:
        """Create a new check row in database and return the line id"""
        check = CheckModel.create(
            steamid=check_info.steamid,
            moder_vk=check_info.moder_vk,
            start_time=check_info.start_time,
            end_time=check_info.end_time,
            server_number=check_info.server_number,
            is_ban=check_info.is_ban,
        )
        return check.id

    def create_table(self):
        CheckModel.create_table()

    def edit_check_end(self, _id: CheckModel.id, end_time: datetime.datetime):
        CheckModel.update(end_time=end_time).where(CheckModel.id == _id).execute()

    def edit_is_ban(self, _id: CheckModel.id, is_ban: bool):
        CheckModel.update(is_ban=is_ban).where(CheckModel.id == _id).execute()

    def get_check_info(self, steamid: int) -> CheckInfo:
        max_id = CheckModel.select(peewee.fn.MAX(CheckModel.id)).where(
            CheckModel.steamid == steamid
        )
        raw_row = (
            CheckModel.select().where(CheckModel.id.in_(max_id)).namedtuples().execute()
        )
        return CheckInfo.from_db(raw_row[0])

    def get_checks_by_time_interval(
        self, time_interval: TimeInterval, moder_vk: int = None
    ) -> list[CheckInfo]:
        if moder_vk is None:
            query_moder_vk = CheckModel.moder_vk.is_null(False)
        else:
            query_moder_vk = CheckModel.moder_vk == moder_vk

        rows = (
            CheckModel.select()
            .where(
                (CheckModel.start_time >= time_interval.start)
                & (CheckModel.end_time <= time_interval.end)
                & (CheckModel.end_time.is_null(False))
                & (query_moder_vk)
            )
            .namedtuples()
            .execute()
        )
        return [CheckInfo.from_db(row) for row in rows]


class RedisController:
    def __init__(self) -> None:
        self.rd = redis.StrictRedis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            password=os.getenv("REDIS_PASSWORD", None),
            db=int(os.getenv("REDIS_DB", 0)),
            decode_responses=True,
        )
        self.players_pattern = "players:{player_name}:{key}"

    def new_check(
        self,
        player_name: str,
        steamid: int,
        db_row_id: int,
        check_stage: CheckStage = "Process",
    ):
        """Add new keys to set players"""
        self.rd.set("players", player_name)
        self.edit_steamid(player_name, steamid)
        self.edit_db_row_id(player_name, db_row_id)
        self.edit_check_stage(player_name, check_stage)

    def edit_steamid(self, player_name: str, steamid: int):
        self.rd.set(
            self.players_pattern.format(player_name=player_name, key="steamid"), steamid
        )
        self.rd.set(steamid, player_name)

    def edit_db_row_id(self, player_name: str, db_row_id: int):
        self.rd.set(
            self.players_pattern.format(player_name=player_name, key="db_row_id"),
            db_row_id,
        )

    def edit_check_stage(self, player_name: str, check_stage: CheckStage):
        self.rd.set(
            self.players_pattern.format(player_name=player_name, key="check_stage"),
            check_stage,
        )

    def get_steamid(self, player_name: str) -> int:
        return int(
            self.rd.get(
                self.players_pattern.format(player_name=player_name, key="steamid")
            )
        )

    def get_db_row_id(self, player_name: str) -> int:
        return int(
            self.rd.get(
                self.players_pattern.format(player_name=player_name, key="db_row_id")
            )
        )

    def get_check_stage(self, player_name: str) -> CheckStage:
        return str(
            self.rd.get(
                self.players_pattern.format(player_name=player_name, key="check_stage")
            )
        )

    def get_player_name(self, steamid: int) -> str:
        return str(self.rd.get(steamid))

    def clear_data(self, player_name: str):
        steamid = self.get_steamid(player_name)
        keys = self.rd.keys(
            self.players_pattern.format(player_name=player_name, key="*")
        )
        self.rd.delete(*keys)
        self.rd.delete(steamid)
