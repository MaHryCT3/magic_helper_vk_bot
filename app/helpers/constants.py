DAY_WORK_MONTH_END = 9
TZ = "Europe/Moscow"
STRING_DATE_FORMAT = "DD.MM.YYYY"


class VK_FOR_CMD:
    id_: int = 166700992
    ignore_users: list[int] = [215360486, 179043503]


class VK_FOR_MESSAGE:
    id_: int = 215360486
    ignore_users: list[int] = []


class REGEX_PATTERNS:
    VK_ID = r"\[id(\d+)\|"  # -> [id`163811405`|@mahryct]
    STRING_IS_DATE = (
        r"\d{,2}.\d{2}.\d{4}-\d{,2}.\d{2}.\d{4}"  # -> `9.04.2022-8.05.2022`
    )
    STEAMID = r"/cc2 \d{,2} (\d+) для"
    PLAYER_NAME = r"Ответ:\s(.+)\s[бвз][оыа][лзб]"
    SERVER_NUMBER = r"/cc2\s(\d+)\s"
