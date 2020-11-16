"""Create logger to catch and notify on failure."""
import re
import sys

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
    chat_data = re.findall(r"\[(\S+)\]", record["message"])
    if bool(chat_data):
        # server = chat_data[0]
        # room = chat_data[1]
        user = chat_data[0]
        message = record["message"].split(":", 1)[1]
        subset = {
            "time": record["time"].strftime("%m/%d/%Y, %H:%M:%S"),
            "message": message,
            # "room": room,
            # "server": server,
            "user": user,
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
    if ENVIRONMENT == "production":
        # Datadog
        logger.add("logs/info.json", format=formatter, level="INFO")
        logger.add("logs/errors.json", format=formatter, level="ERROR")
    else:
        logger.add(sys.stdout, format=formatter, level="INFO")
        logger.add(sys.stderr, format=formatter, level="ERROR")
        logger.add(
            sys.stdout,
            colorize=True,
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan>"
            + " | <light-green>{level}</light-green>: "
            + " <light-white>{message}</light-white>",
            level="INFO",
        )
        logger.add(
            sys.stderr,
            colorize=True,
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan>"
            + " | <light-red>{level}</light-red>: "
            + " <light-white>{message}</light-white>",
            catch=True,
            level="ERROR",
        )
    return logger


LOGGER = create_logger()
