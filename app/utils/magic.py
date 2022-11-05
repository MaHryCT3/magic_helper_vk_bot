from typing import Optional
import os

import aiohttp
import pendulum

from app.models import PlayerInfo, PlayerStats
from app.helpers import constants

stats_api = os.getenv("STATS_API_LINK")
player_api = os.getenv("PLAYERS_API_LINK")

SERVERS_ID = {
    1: 1655,
    2: 41,
    3: 39,
    4: 1930,
    5: 2011,
    6: 2098,
    7: 2342,
    8: 2343,
    9: 3558,
    10: 3771,
    11: 4265,
    12: 4663,
    13: 4721,
    14: 5088,
    15: 7773,
    16: 9096,
    17: 9097,
    18: 9360,
}


async def _get_json(
    url: str,
    session: aiohttp.ClientSession = None,
    content_type: Optional[str] = "application/json",
    encoding: Optional[str] = None,
) -> dict:
    session = session or aiohttp.ClientSession()
    response = await session.get(url)
    await response.read()
    await session.close()
    return await response.json(encoding=encoding, content_type=content_type)


async def get_all_online_players(
    session: aiohttp.ClientSession = None,
) -> list[PlayerInfo]:
    """Return list of all online players"""
    players_online_api_url = f"{player_api}/getPlayersList.php"
    response = await _get_json(
        players_online_api_url, content_type=None, encoding=None, session=session
    )
    players = PlayerInfo.from_json(response)
    return players


async def get_new_online_players(
    day: int = 7,
    session: aiohttp.ClientSession = None,
) -> list[PlayerInfo]:
    """Return list of new online players

    Args:
        session: aiohttp.ClientSession
        day: int - time when account is considered new
    """
    players = await get_all_online_players(session)
    time_skip = pendulum.now(tz=constants.TZ).subtract(days=day)
    return list(filter(lambda v: v.join_time >= time_skip, players))


async def get_player_stats(
    steamid: int,
    server: int,
    session: aiohttp.ClientSession = None,
) -> Optional[PlayerStats]:
    """Return player stats from steamid"""
    player_stats_api_url = (
        f"{stats_api}/getPlayerStat.php?server={SERVERS_ID[server]}&steamid={steamid}"
    )
    response = await _get_json(
        player_stats_api_url,
        content_type="application/json",
        encoding=None,
        session=session,
    )
    if not response:
        return None
    stats = PlayerStats.from_json(response)
    return stats


async def get_stats_from_players(
    players: list[PlayerInfo],
    session: aiohttp.ClientSession = None,
) -> list[PlayerInfo]:
    """Return list of players with stats"""
    for player in players:
        stats = await get_player_stats(player.steamid, player.server, session)
        if stats:
            player.stats = stats
        else:
            player.stats = PlayerStats()
    return players
