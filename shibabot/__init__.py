"""Initialize bot."""
from discord.ext.commands import Bot

from .commands import bot_commands
from .events import bot_events


def create_bot() -> Bot:
    """Initialize bot, register all commands & events."""
    bot = Bot(command_prefix="!")
    bot = bot_events(bot)
    bot = bot_commands(bot)

    return bot


discord_bot = create_bot()
