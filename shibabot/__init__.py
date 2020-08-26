"""Initialize bot."""
from discord.ext import commands as discord_cmd
from .commands import bot_commands
from .events import bot_events
from config import DISCORD_TOKEN


def create_bot():
    """Initialize bot, register all commands & events."""
    bot = discord_cmd.Bot(command_prefix='!')
    bot = bot_events(bot)
    bot = bot_commands(bot)
    bot.run(DISCORD_TOKEN)

    return bot
