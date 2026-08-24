"""Initialize bot."""

from discord import Intents
from discord.ext.commands import Bot

from config import DISCORD_TOKEN
from shibabot.commands import bot_commands
from shibabot.events import bot_events


def create_bot() -> None:
    """Initialize bot, register all commands & events."""
    if not DISCORD_TOKEN:
        raise RuntimeError("DISCORD_TOKEN is unset; add it to your .env file.")

    bot = Bot(command_prefix="!", intents=Intents.all())
    bot = bot_events(bot)
    bot = bot_commands(bot)

    bot.run(DISCORD_TOKEN)
