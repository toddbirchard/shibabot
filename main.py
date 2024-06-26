"""Application entry point."""

import asyncio

from shibabot import create_bot

if __name__ == "__main__":
    asyncio.run(create_bot())
