"""Application entry point."""
from config import DISCORD_TOKEN
from shibabot import discord_bot


def start():
    """Start Discord bot."""
    discord_bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    start()
