import dataclasses

import pendulum

from app.helpers import time_help
from app.helpers import constants
from app import models


@dataclasses.dataclass
class ChecksParams:
    moder_vk: int
    time_interval: models.TimeInterval
