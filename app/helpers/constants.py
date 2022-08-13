DAY_WORK_MONTH_END = 9
TZ = "Europe/Moscow"
STRING_DATE_FORMAT = "DD.MM.YYYY"


class REGEX_PATTERNS:
    VK_ID = r"\[id(\d+)\|"  # -> [id`163811405`|@mahryct]
    STRING_IS_DATE = (
        r"\d{,2}.\d{2}.\d{4}-\d{,2}.\d{2}.\d{4}"  # -> `9.04.2022-8.05.2022`
    )
