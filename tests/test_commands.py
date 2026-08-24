"""Verify bot commands are registered correctly and behave as expected."""

from datetime import datetime
from unittest.mock import patch

import pytest
import pytz

TZ = pytz.timezone("America/New_York")

EXPECTED_COMMANDS = {
    "420",
    "crypto",
    "giphy",
    "imdb",
    "stock",
    "urban",
    "weather",
    "wiki",
}


class TestRegistration:
    """Commands and aliases are wired onto the bot."""

    def test_every_command_is_registered(self, bot):
        """Every user-facing command is reachable by name."""
        assert EXPECTED_COMMANDS <= set(bot.all_commands)

    def test_every_command_has_help_text(self, bot):
        """`!help` is only useful if each command describes itself."""
        missing = [
            name for name in EXPECTED_COMMANDS if not bot.all_commands[name].help
        ]
        assert missing == [], f"commands missing help text: {missing}"

    @pytest.mark.parametrize(
        "alias, target",
        [("define", "urban"), ("!", "giphy")],
    )
    def test_aliases_resolve_to_their_command(self, bot, alias, target):
        """Regression: `alias=` (singular) was silently dropped by **kwargs."""
        assert bot.all_commands[alias] is bot.all_commands[target]


class TestTimeRemaining:
    """`!420` counts down to the next 4:20, and must survive month boundaries."""

    async def _countdown_at(self, invoke, when: datetime) -> str:
        """Run `!420` with the clock frozen at `when`, returning what it sent."""
        with patch("shibabot.commands.datetime") as mock_datetime:
            mock_datetime.now.return_value = TZ.localize(when)
            return await invoke("420")

    @pytest.mark.parametrize(
        "when, expected",
        [
            # Before 4:20am -> counts to this morning.
            (datetime(2026, 8, 24, 2, 0, 0), "2 hours, 20 minutes"),
            # Between 4:20am and 4:20pm -> counts to this afternoon.
            (datetime(2026, 8, 24, 12, 0, 0), "4 hours, 20 minutes"),
            # After 4:20pm -> rolls over to tomorrow morning.
            (datetime(2026, 8, 24, 20, 0, 0), "8 hours, 20 minutes"),
        ],
    )
    async def test_picks_the_next_target_time(self, invoke, when, expected):
        """The countdown targets whichever 4:20 comes next."""
        assert (await self._countdown_at(invoke, when)).startswith(expected)

    @pytest.mark.parametrize(
        "when",
        [
            pytest.param(datetime(2026, 1, 31, 20, 0, 0), id="end-of-31-day-month"),
            pytest.param(datetime(2026, 4, 30, 20, 0, 0), id="end-of-30-day-month"),
            pytest.param(datetime(2026, 2, 28, 20, 0, 0), id="end-of-feb"),
            pytest.param(datetime(2024, 2, 29, 20, 0, 0), id="end-of-leap-feb"),
            pytest.param(datetime(2026, 12, 31, 20, 0, 0), id="end-of-year"),
        ],
    )
    async def test_rolls_over_month_and_year_boundaries(self, invoke, when):
        """Regression: `now.replace(day=now.day + 1)` raised ValueError here."""
        assert await self._countdown_at(invoke, when) == (
            "8 hours, 20 minutes, & 00 seconds until 4:20"
        )

    async def test_seconds_are_not_fractional(self, invoke):
        """Without microsecond=0 this rendered e.g. `23.456789 seconds`."""
        message = await self._countdown_at(
            invoke, datetime(2026, 8, 24, 12, 0, 0, 123456)
        )
        assert "." not in message


class TestApiBackedCommands:
    """Commands delegate to their API helper and send back the result."""

    @pytest.mark.parametrize(
        "command, helper, args",
        [
            ("giphy", "get_giphy_image", ("shiba", "inu")),
            ("wiki", "get_wiki_summary", ("shiba", "inu")),
            ("imdb", "get_imdb_movie", ("blade", "runner")),
            ("urban", "get_urban_definition", ("bussin",)),
            ("weather", "get_weather", ("brooklyn",)),
        ],
    )
    async def test_sends_helper_response(self, invoke, command, helper, args):
        """Trailing args are joined into one query and the reply is relayed."""
        with patch(f"shibabot.commands.{helper}", return_value="result") as mock_helper:
            assert await invoke(command, *args) == "result"
        mock_helper.assert_called_once_with(" ".join(args))

    @pytest.mark.parametrize(
        "command, handler",
        [("stock", "stock_chart_handler"), ("crypto", "crypto_chart_handler")],
    )
    async def test_sends_chart_url(self, invoke, command, handler):
        """Chart commands forward the symbol and relay the chart URL."""
        with patch(f"shibabot.commands.{handler}") as mock_handler:
            mock_handler.get_chart.return_value = "https://example.com/chart.png"
            assert await invoke(command, "SHIB") == "https://example.com/chart.png"
        mock_handler.get_chart.assert_called_once_with("SHIB")
