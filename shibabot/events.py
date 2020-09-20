"""Room events."""
from .log import LOGGER
from discord.ext.commands import Bot


def bot_events(bot) -> Bot:
    """Register actions to be taken upon room actions."""
    @bot.event
    async def on_ready() -> None:
        """Confirm bot is connected."""
        for guild in bot.guilds:
            LOGGER.info(f'Connected to {guild.name}')

    @bot.event
    async def on_message(message) -> None:
        """Log chat messages"""
        LOGGER.info(message)

    @bot.event
    async def on_error(event, *args) -> None:
        """Log chat messages"""
        LOGGER.error(f'Unhandled error: {event} | args: {" ".join(args)}')

    return bot
