from app.models import PlayerInfo


def filter_bad_stats(players: list[PlayerInfo]) -> list[PlayerInfo]:
    """Return list of players with stats"""
    return list(filter(lambda v: v.stats.kd > 1, players))


def sorted_by_kd(players: list[PlayerInfo]) -> list[PlayerInfo]:
    """Return list of players with stats"""
    return sorted(players, key=lambda v: v.stats.kd, reverse=True)
