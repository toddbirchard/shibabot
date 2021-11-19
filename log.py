"""Create logger to catch and notify on failure."""
import re
from os import path
from sys import stdout

import json
from loguru import logger

from config import ENVIRONMENT

DD_APM_FORMAT = (
    "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
    "[dd.service=%(dd.service)s dd.env=%(dd.env)s "
    "dd.version=%(dd.version)s "
    "dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s]"
    "- %(message)s"
)


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
        subset = {
            "time": log["time"].strftime("%m/%d/%Y, %H:%M:%S"),
            "message": log["message"],
            "level": log["level"].name,
            "function": log.get("function"),
            "module": log.get("name"),
        }
        if log.get("exception", None):
            subset.update({"exception": log["exception"]})
        return json.dumps(subset)

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
    if record["level"].name == "INFO":
        return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #b3cfe7>{level}</fg #b3cfe7>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "WARNING":
        return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> |  <fg #b09057>{level}</fg #b09057>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "SUCCESS":
        return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #6dac77>{level}</fg #6dac77>: <light-white>{message}</light-white>\n"
    elif record["level"].name == "ERROR":
        return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #a35252>{level}</fg #a35252>: <light-white>{message}</light-white>\n"
    return "<fg #5278a3>{time:MM-DD-YYYY HH:mm:ss}</fg #5278a3> | <fg #b3cfe7>{level}</fg #b3cfe7>: <light-white>{message}</light-white>\n"


def create_logger() -> logger:
    """Customer logger creation."""
    logger.remove()
    logger.add(
        stdout,
        colorize=True,
        format=log_formatter,
    )
    if ENVIRONMENT == "production" and path.isdir("/var/log/api"):
        logger.add(
            "/var/log/shibabot/info.json",
            format=json_formatter,
            rotation="200 MB",
            compression="zip",
            catch=True,
        )
        # Datadog APM tracing
        logger.add(
            "/var/log/shibabot/apm.log",
            format=DD_APM_FORMAT,
            rotation="200 MB",
            compression="zip",
        )
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
