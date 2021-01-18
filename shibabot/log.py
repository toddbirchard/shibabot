"""Create logger to catch and notify on failure."""
import re
from sys import stdout

import simplejson as json
from loguru import logger

from config import ENVIRONMENT


def serialize_trace(record: dict) -> str:
    """Construct JSON log record."""
    subset = {
        "time": record["time"].strftime("%m/%d/%Y, %H:%M:%S"),
        "message": record["message"],
    }
    return json.dumps(subset)


def serialize_info(record) -> str:
    """Construct JSON log record."""
    subset = {
        "time": record["time"].strftime("%m/%d/%Y, %H:%M:%S"),
        "message": record["message"],
        # "room": room,
        # "server": server,
        # "user": user,
    }
    return json.dumps(subset)


def formatter(record: dict) -> str:
    if record["level"].name in ("TRACE", "ERROR"):
        record["extra"]["serialized"] = serialize_trace(record)
        return "{extra[serialized]},\n"
    record["extra"]["serialized"] = serialize_info(record)
    return "{extra[serialized]},\n"


def create_logger() -> logger:
    """Customer logger creation."""
    logger.remove()
    logger.add(
        stdout,
        colorize=True,
        format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan>"
        + " | <light-green>{level}</light-green>: "
        + " <light-white>{message}</light-white>",
    )
    if ENVIRONMENT == "production":
        logger.add(
            "/var/log/shibabot/info.json",
            format=formatter,
            rotation="300 MB",
            compression="zip",
            catch=True,
        )
        logger.add(
            "/var/log/shibabot/error.log",
            colorize=True,
            catch=True,
            level="ERROR",
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
            + "<red>{level}</red>: "
            + "<light-white>{message}</light-white>",
            rotation="300 MB",
            compression="zip",
        )
    return logger


LOGGER = create_logger()
