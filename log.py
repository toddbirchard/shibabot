"""Create logger to catch and notify on failure."""
import json
import re
from os import path
from sys import stdout

from loguru import logger

from config import ENVIRONMENT


def json_formatter(record: dict):
    """
    Pass raw log to be serialized.

    :param dict record: Dictionary containing logged message with metadata.
    """

    def serialize(log: dict):
        """
        Parse log message into Datadog JSON format.

        :param dict log: Dictionary containing logged message with metadata.
        """
        try:
            subset = {
                "time": log["time"].strftime("%m/%d/%Y, %H:%M:%S"),
                "message": log["message"],
                "level": log["level"].name,
                # "function": log.get("function"),
                # "module": log.get("name"),
            }
            if log.get("exception", None):
                subset.update({"exception": log["exception"]})
            return json.dumps(subset)
        except Exception as e:
            log["error"] = f"Logging error occurred: {e}"
            return serialize_error(log)

    def serialize_error(log: dict) -> str:
        """
        Construct error log record.

        :param dict log: Dictionary containing logged message with metadata.

        :returns: str
        """
        subset = {
            "time": log["time"].strftime("%m/%d/%Y, %H:%M:%S"),
            "level": log["level"].name,
            "message": log["message"],
        }
        return json.dumps(subset)

    if record["level"].name == "ERROR":
        record["extra"]["serialized"] = serialize_error(record)
    else:
        record["extra"]["serialized"] = serialize(record)

    return "{extra[serialized]},\n"


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
        "room": record["room"],
        "server": record["server"],
        "user": record["user"],
    }
    return json.dumps(subset)


def log_formatter(record: dict) -> str:
    """
    Formatter for .log records

    :param dict record: Key/value object containing a single log's message & metadata.

    :returns: str
    """
    if record["level"].name == "TRACE":
        return "<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> | <fg #cfe2f3>{level}</fg #cfe2f3>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "INFO":
        return "<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> | <fg #9cbfdd>{level}</fg #9cbfdd>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "DEBUG":
        return "<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> | <fg #8598ea>{level}</fg #8598ea>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "WARNING":
        return "<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> |  <fg #dcad5a>{level}</fg #dcad5a>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "SUCCESS":
        return "<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> | <fg #3dd08d>{level}</fg #3dd08d>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "ERROR":
        return "<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> | <fg #ae2c2c>{level}</fg #ae2c2c>: <light-white>{message}</light-white>\n"
    return "<fg #70acde>{time:MM-DD-YYYY HH:mm:ss}</fg #70acde> | <fg #b3cfe7>{level}</fg #b3cfe7>: <light-white>{message}</light-white>\n"


def create_logger() -> logger:
    """Customer logger creation."""
    logger.remove()
    logger.add(stdout, colorize=True, catch=True, format=log_formatter)
    if ENVIRONMENT == "production" and path.isdir("/var/log/shibabot"):
        logger.add(
            "/var/log/shibabot/info.json",
            format=json_formatter,
            rotation="200 MB",
            compression="zip",
            catch=True,
        )
        # Datadog APM tracing
        """logger.add(
            "/var/log/shibabot/apm.log",
            format=DD_APM_FORMAT,
            rotation="200 MB",
            compression="zip",
        )"""
        logger.add(
            "/var/log/shibabot/info.log",
            colorize=True,
            catch=True,
            level="INFO",
            format=log_formatter,
            rotation="200 MB",
            compression="zip",
        )
        logger.add(
            "/var/log/shibabot/error.log",
            colorize=True,
            catch=True,
            level="ERROR",
            format=log_formatter,
            rotation="200 MB",
            compression="zip",
        )
    return logger


LOGGER = create_logger()
