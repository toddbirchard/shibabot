"""Initialize bot."""
from discord.ext.commands import Bot

from shibabot.commands import bot_commands
from shibabot.events import bot_events

from config import DISCORD_TOKEN


def create_bot() -> Bot:
    """Initialize bot, register all commands & events."""
    bot = Bot(command_prefix="!")
    bot = bot_events(bot)
    bot = bot_commands(bot)

    return bot.run(DISCORD_TOKEN)
