"""Create logger to catch and notify on failure."""
import sys
from loguru import logger
from config import ENVIRONMENT


def create_logger() -> logger:
    """Customer logger creation."""
    logger.remove()
    if ENVIRONMENT == 'production':
        logger.add(
            'logs/info.log',
            colorize=True,
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan>"
            + " | <light-red>{level}</light-red>:"
            + " <light-white>{message}</light-white>",
            rotation="300 MB",
            level="INFO"
        )
        logger.add(
            'logs/errors.log',
            colorize=True,
            format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan>"
            + " | <light-red>{level}</light-red>: "
            + " <light-white>{message}</light-white>",
            catch=True,
            rotation="300 MB",
            level="ERROR"
        )
    else:
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
