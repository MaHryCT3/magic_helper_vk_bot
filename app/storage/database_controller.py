import os
import datetime as dt
from typing import Optional

import peewee

import redis

from pendulum.datetime import DateTime

from loguru import logger

from app.storage.orm_models import CheckModel
from app.models import CheckInfo, TimeInterval, CheckStage


class PostgresController:
    def new_check(self, check_info: CheckInfo) -> int:
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

    def create_table(self) -> None:
        CheckModel.create_table()

    def edit_check_end(
        self, _id: CheckModel.id, end_time: DateTime | dt.datetime
    ) -> None:
        CheckModel.update(end_time=end_time).where(CheckModel.id == _id).execute()

    def edit_is_ban(self, _id: CheckModel.id, is_ban: bool) -> None:
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

    def get_count_checks_by_time_interval(
        self,
        time_interval: TimeInterval,
        moder_vk: int = None,
        only_banned: bool = False,
    ) -> int:
        """Returns a checks count by time interval

        Args:
            time_interval: time interval
            moder_vk: moderator vk id
            only_banned: if is True returns only checks that ended in a ban

        Returns:
            Number of checks by arguments
        """
        if moder_vk is None:
            query_moder_vk = CheckModel.moder_vk.is_null(False)
        else:
            query_moder_vk = CheckModel.moder_vk == moder_vk

        if only_banned:
            query_is_ban = CheckModel.is_ban == True
        else:
            query_is_ban = (CheckModel.is_ban == True) | (CheckModel.is_ban == False)

        count = (
            CheckModel.select()
            .where(
                (CheckModel.start_time >= time_interval.start)
                & (CheckModel.end_time <= time_interval.end)
                & (CheckModel.end_time.is_null(False))
                & (query_moder_vk)
                & (query_is_ban)
            )
            .count()
        )
        return count

    def get_moderators(self) -> list[int]:
        """Returns all moderators in database"""
        moders = (
            CheckModel.select(CheckModel.moder_vk).distinct().namedtuples().execute()
        )
        return [int(i.moder_vk) for i in moders]


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
    ) -> None:
        """Add new keys to set players"""
        self.rd.set("players", player_name)
        self.edit_steamid(player_name, steamid)
        self.edit_db_row_id(player_name, db_row_id)
        self.edit_check_stage(player_name, check_stage)

    def edit_steamid(self, player_name: str, steamid: int) -> None:
        self.rd.set(
            self.players_pattern.format(player_name=player_name, key="steamid"), steamid
        )
        self.rd.set(str(steamid), player_name)

    def edit_db_row_id(self, player_name: str, db_row_id: int) -> None:
        self.rd.set(
            self.players_pattern.format(player_name=player_name, key="db_row_id"),
            db_row_id,
        )

    def edit_check_stage(self, player_name: str, check_stage: CheckStage) -> None:
        self.rd.set(
            self.players_pattern.format(player_name=player_name, key="check_stage"),
            check_stage,
        )

    def get_steamid(self, player_name: str) -> Optional[int]:
        steamid = self.rd.get(
            self.players_pattern.format(player_name=player_name, key="steamid")
        )
        return int(steamid) if steamid else None

    def get_db_row_id(self, player_name: str) -> Optional[int]:
        db_row_id = self.rd.get(
            self.players_pattern.format(player_name=player_name, key="db_row_id")
        )

        return int(db_row_id) if db_row_id else None

    def get_check_stage(self, player_name: str) -> CheckStage:
        return str(
            self.rd.get(
                self.players_pattern.format(player_name=player_name, key="check_stage")
            )
        )

    def get_player_name(self, steamid: int) -> str:
        return str(self.rd.get(str(steamid)))

    def clear_data(self, player_name: str) -> None:
        steamid = self.get_steamid(player_name)
        keys = self.rd.keys(
            self.players_pattern.format(player_name=player_name, key="*")
        )
        self.rd.delete(*keys)
        if steamid is None:
            logger.critical(f"Can't find steamid from player {player_name}")
        self.rd.delete(str(steamid))
