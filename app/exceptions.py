class VKJsonError(Exception):
    """Raised for errors with json from vk"""


class NotFoundPattern(Exception):
    """Raised for error with regex pattern"""


class NotSupportedEvent(Exception):
    """Raised for error with unsupported event type from vk"""


class FailedToDatabaseConnection(Exception):
    """Raised for error with database connection"""


class ParamsError(Exception):
    """Raised for error with parameters from user"""


class CantGetChecksInfo(Exception):
    """Raised for error when cant get checks info from database"""
