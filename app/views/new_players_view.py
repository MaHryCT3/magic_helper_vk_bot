from app.models import PlayerInfo


def get_new_players_view(players: list[PlayerInfo]) -> str:
    """Return text for user message with new players information.

    Args:
        players: list of new players
    Return:
        text for user message
    """
    if not players:
        return "Подозрительных новых игроков не найдено"
    cap = "Новые игроки: \n\n"
    body = _get_body(players)
    text = cap + body
    return text


def _get_body(players: list[PlayerInfo]) -> str:
    """Return body of view from list of players"""
    body = ""
    for player in players:
        body += _get_body_from_model(player)
    return body


def _get_body_from_model(player: PlayerInfo) -> str:
    """Return body of view from single model"""
    body = f"{player.steamid}: {player.stats.kill}/{player.stats.death}({round(player.stats.kd, 1)})\n"
    return body
