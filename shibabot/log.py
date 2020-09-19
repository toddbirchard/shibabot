"""Create logger to catch and notify on failure."""
import sys
import simplejson as json
from loguru import logger
from config import ENVIRONMENT


def serialize(record):
    """Construct JSON log record."""
    if record['function'] == 'on_message':
        subset = {
            "time": record["time"].strftime("%m/%d/%Y, %H:%M:%S"),
            "message": record['message'].content,
            "room": record['message'].channel.name,
            "server": record['message'].guild.name,
            "user": record['message'].author.name,
        }
        return json.dumps(subset)
    subset = {
        "time": record["time"].strftime("%m/%d/%Y, %H:%M:%S"),
        "message": record['message']
    }
    return json.dumps(subset)


def formatter(record):
    print('RECORD = ', record)
    record["extra"]["serialized"] = serialize(record)
    return "{extra[serialized]},\n"


def create_logger() -> logger:
    """Customer logger creation."""
    logger.remove()
    if ENVIRONMENT == 'production':
        # Datadog
        logger.add(
            'logs/info.json',
            format=formatter,
            level="INFO"
        )
        logger.add(
            'logs/errors.json',
            format=formatter,
            level="ERROR"
        )
    else:
        logger.add(
            sys.stdout,
            format=formatter,
            level="INFO"
        )
        logger.add(
            sys.stderr,
            format=formatter,
            level="ERROR"
        )
        logger.add(
            sys.stdout,
            colorize=True,
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan>"
                   + " | <light-green>{level}</light-green>: "
                   + " <light-white>{message}</light-white>",
            level="INFO"
        )
        logger.add(
            sys.stderr,
            colorize=True,
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan>"
                   + " | <light-red>{level}</light-red>: "
                   + " <light-white>{message}</light-white>",
            catch=True,
            level="ERROR"
        )
    return logger


LOGGER = create_logger()
