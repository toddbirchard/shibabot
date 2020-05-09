"""Application entry point."""
from application import create_bot
from config import DISCORD_TOKEN

bot = create_bot()

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
