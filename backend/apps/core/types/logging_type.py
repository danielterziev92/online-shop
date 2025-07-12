from enum import StrEnum


class LoggingConfigKeysType(StrEnum):
    SYSTEM_LOGGING_LEVEL = "system_logging_level"

    LOGGING_MODULE = "logging_{}"


class LoggingLevel(StrEnum):
    """Enum за logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
