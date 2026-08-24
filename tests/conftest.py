"""Shared fixtures for the shibabot test suite."""

from unittest.mock import AsyncMock

import pytest
from discord import Intents
from discord.ext.commands import Bot

from shibabot.commands import bot_commands
from shibabot.events import bot_events


@pytest.fixture
def bot() -> Bot:
    """A fully registered bot that is never connected to Discord."""
    return bot_commands(bot_events(Bot(command_prefix="!", intents=Intents.all())))


@pytest.fixture
def ctx() -> AsyncMock:
    """Stand-in for a command Context, recording whatever the bot sends."""
    return AsyncMock()


@pytest.fixture
def invoke(bot, ctx):
    """Invoke a registered command by name, returning what it sent."""

    async def _invoke(name: str, *args):
        """Call a command by name and return the single message it sent."""
        command = bot.all_commands[name]
        await command.callback(ctx, *args)
        ctx.send.assert_awaited_once()
        return ctx.send.await_args.args[0]

    return _invoke
