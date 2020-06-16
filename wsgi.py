"""Application entry point."""
from shibabot import create_bot
from config import DISCORD_TOKEN


def start():
    """Initialize bot."""
    bot = create_bot()
    bot.run(DISCORD_TOKEN)
