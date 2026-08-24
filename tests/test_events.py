"""Verify event handlers gate messages and surface errors."""

import types
from unittest.mock import AsyncMock, PropertyMock, patch

import pytest
from discord.ext.commands import Bot

APPROVED = "Hackers and Slackers"


@pytest.fixture
def gated_bot(bot):
    """A bot whose allow-list is a single known guild, with dispatch stubbed."""
    bot.process_commands = AsyncMock()
    with patch("shibabot.events.DISCORD_GUILDS", [APPROVED]):
        yield bot


def message(author, guild_name, content="!420"):
    """Minimal stand-in for a discord Message."""
    return types.SimpleNamespace(
        author=author,
        guild=types.SimpleNamespace(name=guild_name) if guild_name else None,
        content=content,
    )


class TestOnMessage:
    """Only messages from approved guilds reach command dispatch."""

    async def test_dispatches_from_approved_guild(self, gated_bot):
        """Messages from an allow-listed guild reach command dispatch."""
        await gated_bot.on_message(message(object(), APPROVED))
        gated_bot.process_commands.assert_awaited_once()

    @pytest.mark.parametrize(
        "guild_name, reason",
        [
            ("Some Random Server", "guild not in allow-list"),
            (None, "direct message has no guild"),
        ],
    )
    async def test_ignores_unapproved_source(self, gated_bot, guild_name, reason):
        """Unapproved guilds and DMs never reach command dispatch."""
        await gated_bot.on_message(message(object(), guild_name))
        assert gated_bot.process_commands.await_count == 0, reason

    async def test_ignores_its_own_messages(self, gated_bot):
        """Guards against the bot answering its own `!`-prefixed output."""
        me = object()
        with patch.object(Bot, "user", new_callable=PropertyMock, return_value=me):
            await gated_bot.on_message(message(me, APPROVED))
        gated_bot.process_commands.assert_not_awaited()


class TestOnReady:
    """Startup reports which connected guilds are approved."""

    async def test_distinguishes_approved_from_ignored(self, bot):
        """Connected guilds are logged as success or warning per the allow-list."""
        guilds = [
            types.SimpleNamespace(name=APPROVED),
            types.SimpleNamespace(name="Some Random Server"),
        ]
        with (
            patch("shibabot.events.DISCORD_GUILDS", [APPROVED]),
            patch.object(Bot, "guilds", new_callable=PropertyMock, return_value=guilds),
            patch("shibabot.events.LOGGER") as logger,
        ):
            await bot.on_ready()

        assert APPROVED in logger.success.call_args.args[0]
        assert "Some Random Server" in logger.warning.call_args.args[0]


class TestOnError:
    """Unhandled event exceptions are logged with a traceback."""

    async def test_logs_traceback(self, bot):
        """Regression: on_error discarded the exception, logging only the event name."""
        with patch("shibabot.events.LOGGER") as logger:
            try:
                raise AttributeError("'Bot' object has no attribute 'ctx'")
            except AttributeError:
                await bot.on_error("on_ready")

        logged = logger.error.call_args.args[0]
        assert "on_ready" in logged
        assert "AttributeError" in logged
        assert "no attribute 'ctx'" in logged
