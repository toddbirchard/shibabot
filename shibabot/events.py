"""Room events."""

from traceback import format_exc

from discord.ext.commands import Bot

from config import DISCORD_GUILDS
from logger import LOGGER


def bot_events(bot) -> Bot:
    """Register actions to be taken upon room actions."""

    @bot.event
    async def on_ready() -> None:
        """Confirm bot is connected."""
        LOGGER.info(f"Available commands: {bot.all_commands.keys()}")
        for guild in bot.guilds:
            if guild.name in DISCORD_GUILDS:
                LOGGER.success(f"Connected to {guild.name}")
            else:
                LOGGER.warning(f"Ignoring unapproved guild: {guild.name}")

    @bot.event
    async def on_message(message) -> None:
        """Log chat messages & dispatch commands from approved guilds."""
        if message.author == bot.user:
            return
        if message.guild is None or message.guild.name not in DISCORD_GUILDS:
            return
        LOGGER.info(f"[{message.guild.name}] {message.author}: {message.content}")
        await bot.process_commands(message)

    @bot.event
    async def on_error(event, *args, **kwargs) -> None:
        """Log unhandled exceptions raised while handling an event."""
        LOGGER.error(f"Unhandled error in {event} (args={args!r}):\n{format_exc()}")

    return bot
