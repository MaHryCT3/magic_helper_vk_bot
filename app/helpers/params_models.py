from typing import NamedTuple, Optional
import dataclasses

import pendulum

from app.helpers import time_help
from app.helpers import constants
from app import models


@dataclasses.dataclass
class ChecksCmdParams:
    """Model for commands /cc /cc2 /cc3"""

    server_number: int
    steamid: int


@dataclasses.dataclass
class BanCmdParams(ChecksCmdParams):
    """Model for command /ban"""

    reason: str = "Забанен по результатам проверки."


@dataclasses.dataclass
class GetChecksParameters:
    moder_vk: int
    time_interval: models.TimeInterval
