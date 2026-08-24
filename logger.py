"""Create logger to catch and notify on failure."""

import json
import re
from datetime import datetime
from os import path
from sys import stdout

from loguru import logger

from config import ENVIRONMENT


def json_formatter(record: dict) -> str:
    """
    Format info message logs.

    :param dict record: Log object containing log metadata & message.

    :returns: str
    """
    if isinstance(record, (str, bool)):
        return construct_json_from_corrupted_log(record)

    record["time"] = record["time"].strftime("%m/%d/%Y, %H:%M:%S")
    record["elapsed"] = record["elapsed"].total_seconds()

    def serialize_as_admin(log: dict) -> str:
        """
        Construct JSON info log record where user is room admin.

        :param dict log: Dictionary containing logged message with metadata.

        :returns: str
        """
        try:
            chat_data = re.search(
                r"(?P<room>\[\S+]) (?P<user>\[\S+]) (?P<ip>\[\S+])", log.get("message")
            )
            if chat_data and log.get("message"):
                message = log["message"].split(": ", 1)[1].replace("\n", "\t")
                subset = {
                    "time": log["time"],
                    "message": message,
                    "level": log["level"].name,
                    "room": chat_data["room"].replace("[", "").replace("]", ""),
                    "user": chat_data["user"].replace("[", "").replace("]", ""),
                    "ip": chat_data["ip"].replace("[", "").replace("]", ""),
                }
                return json.dumps(subset)
        except Exception as e:
            subset["error"] = f"Logging error occurred: {str(e)}"
            return serialize_error(subset)

    def serialize_event(log: dict) -> str:
        """
        Construct warning log.

        :param dict log: Dictionary containing logged message with metadata.

        :returns: str
        """
        try:
            chat_data = re.search(r"(?P<room>\[\S+]) (?P<user>\[\S+])", log["message"])
            if bool(chat_data) and log.get("message") is not None:
                subset = {
                    "time": log["time"],
                    "message": log["message"].split(": ", 1)[1],
                    "level": log["level"].name,
                    "room": chat_data["room"].replace("[", "").replace("]", ""),
                    "user": chat_data["user"].replace("[", "").replace("]", ""),
                }
                return json.dumps(subset)
        except Exception as e:
            log["error"] = f"Logging error occurred: {str(e)}"

    def serialize_error(log: dict) -> str:
        """
        Construct error log record.

        :param dict log: Dictionary containing logged message with metadata.

        :returns: str
        """
        if log and log.get("message"):
            subset = {
                "time": log["time"],
                "level": log["level"].name,
                "message": log["message"],
            }
            return json.dumps(subset)

    if record["level"].name == "INFO":
        record["extra"]["serialized"] = serialize_as_admin(record)
        return "{extra[serialized]},\n"
    if record["level"].name in ("TRACE", "WARNING", "SUCCESS"):
        record["extra"]["serialized"] = serialize_event(record)
        return "{extra[serialized]},\n"
    if record["level"].name in ("ERROR", "CRITICAL"):
        record["extra"]["serialized"] = serialize_error(record)
        serialize_error(record)
        return "{extra[serialized]},\n"
    record["extra"]["serialized"] = serialize_error(record)
    return "{extra[serialized]},\n"


def construct_json_from_corrupted_log(log: str) -> str:
    """
    Create JSON log record from corrupt string.

    :param str log: Corrupt log string.

    :returns: str
    """
    return {
        "time": datetime.strftime(datetime.now(), "%m/%d/%Y, %H:%M:%S"),
        "level": "ERROR",
        "message": log,
    }


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


def create_logger():
    """Customer logger creation."""
    logger.remove()
    logger.add(stdout, colorize=True, catch=True, format=log_formatter)
    if ENVIRONMENT == "production" and path.isdir("/var/log/shibabot"):
        logger.add(
            "/var/log/shibabot/access.json",
            format=json_formatter,
            rotation="200 MB",
            compression="zip",
            catch=True,
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
