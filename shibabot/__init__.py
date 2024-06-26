"""Initialize bot."""

from discord import Intents
from discord.ext.commands import Bot

from config import DISCORD_TOKEN
from shibabot.commands import bot_commands
from shibabot.events import bot_events


def create_bot() -> Bot:
    """Initialize bot, register all commands & events."""
    bot = Bot(command_prefix="!", intents=Intents.all())
    bot = bot_events(bot)
    bot = bot_commands(bot)

    return bot.run(DISCORD_TOKEN)
