"""Initialize bot."""
from .log import LOGGER
from discord.ext import commands as discord_cmd
from .commands import bot_commands
from .events import bot_events


def create_bot():
    """Initialize bot, register all commands & events."""
    bot = discord_cmd.Bot(command_prefix='!')
    bot = bot_events(bot)
    bot = bot_commands(bot)

    return bot
