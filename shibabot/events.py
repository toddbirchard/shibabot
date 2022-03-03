"""Room events."""
from discord.ext.commands import Bot

from log import LOGGER


def bot_events(bot) -> Bot:
    """Register actions to be taken upon room actions."""

    @bot.event
    async def on_ready() -> None:
        """Confirm bot is connected."""
        for guild in bot.guilds:
            LOGGER.success(f"Connected to {guild.name}")
        LOGGER.info(f"Available commands: {bot.all_commands.keys()}")

    @bot.event
    async def on_message(message) -> None:
        """Log chat messages"""
        # print(bot.__dict__.keys())
        LOGGER.info(f"[{bot.user.name}]: {message}")

    @bot.event
    async def on_error(event, *args) -> None:
        """Log chat messages"""
        LOGGER.error(f'Unhandled error: {event} | args: {" ".join(args)}')

    return bot
