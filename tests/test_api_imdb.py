"""Verify IMDB lookups degrade gracefully on incomplete or missing data."""

from unittest.mock import MagicMock, patch

import pytest
from imdb import IMDbError

from shibabot.api import get_imdb_movie, imdb_box_office_data

FULL_DATA = {
    "title": "Blade Runner",
    "rating": 8.1,
    "year": 1982,
    "genres": ["Action", "Sci-Fi"],
    "cast": [
        {"name": "Harrison Ford"},
        {"name": "Rutger Hauer"},
        {"name": "Sean Young"},
    ],
    "director": [{"name": "Ridley Scott"}],
    "synopsis": [
        "A blade runner must pursue four replicants. He hunts them. Then rain."
    ],
    "box office": {
        "Budget": "$28,000,000",
        "Cumulative Worldwide Gross": "$41,722,000",
    },
    "cover url": "https://example.com/poster.jpg",
}


def fake_imdb(data, results=1):
    """Build a patched IMDb client returning `results` hits with `data`."""
    movie = MagicMock()
    movie.data = data
    client = MagicMock()
    client.search_movie.return_value = [MagicMock() for _ in range(results)]
    client.get_movie.return_value = movie
    return client


@pytest.fixture
def lookup():
    """Run get_imdb_movie against a stubbed IMDb client."""

    def _lookup(data, results=1):
        """Look up a movie whose IMDB record is `data`."""
        with patch("shibabot.api.IMDb", return_value=fake_imdb(data, results)):
            return get_imdb_movie("blade runner")

    return _lookup


class TestHappyPath:
    """A complete record renders every field."""

    def test_includes_all_fields(self, lookup):
        """Title, rating, genres, cast, director, gross and art all appear."""
        response = lookup(FULL_DATA)
        assert "BLADE RUNNER," in response
        assert "8.1/10" in response
        assert "(Action, Sci-Fi, 1982)." in response
        assert "STARRING Harrison Ford, Rutger Hauer." in response
        assert "DIRECTED by Ridley Scott." in response
        assert "BUDGET $28,000,000." in response
        assert "https://example.com/poster.jpg" in response

    def test_caps_cast_at_two_actors(self, lookup):
        """Only the top two billed actors are named."""
        assert "Sean Young" not in lookup(FULL_DATA)

    def test_synopsis_keeps_two_whole_sentences(self, lookup):
        """Regression: `synopsis[0][0]` truncated the blurb to one character."""
        response = lookup(FULL_DATA)
        assert "A blade runner must pursue four replicants. He hunts them" in response
        assert "Then rain" not in response


class TestMissingFields:
    """Absent fields are omitted rather than rendered as `None`."""

    @pytest.mark.parametrize(
        "field",
        [
            "rating",
            "year",
            "genres",
            "cast",
            "director",
            "synopsis",
            "box office",
            "cover url",
        ],
    )
    def test_omits_absent_field_without_crashing(self, lookup, field):
        """Any single missing key still yields a clean response."""
        data = {k: v for k, v in FULL_DATA.items() if k != field}
        response = lookup(data)
        assert response is not None
        assert "None" not in response
        assert "N/A" not in response

    @pytest.mark.parametrize(
        "field",
        ["genres", "cast", "director", "synopsis", "box office"],
    )
    def test_tolerates_empty_collections(self, lookup, field):
        """Regression: `data['cast'][:2]` raised KeyError; `director[0]` IndexError."""
        response = lookup({**FULL_DATA, field: []})
        assert response is not None
        assert "None" not in response

    def test_title_only_record_still_renders(self, lookup):
        """A record with nothing but a title is the minimum viable response."""
        assert lookup({"title": "Untitled"}) == "UNTITLED,"

    def test_returns_none_without_a_title(self, lookup):
        """An untitled record is unusable and yields nothing."""
        assert lookup({"rating": 8.1}) is None


class TestLookupFailures:
    """Search failures return None instead of raising."""

    def test_returns_none_when_search_finds_nothing(self):
        """Regression: `movies[0]` raised IndexError on an empty result list."""
        client = fake_imdb(FULL_DATA, results=0)
        with (
            patch("shibabot.api.IMDb", return_value=client),
            patch("shibabot.api.LOGGER") as logger,
        ):
            assert get_imdb_movie("blade runner") is None
        # An empty result set is expected input, not an error to be caught.
        logger.warning.assert_called_once()
        logger.error.assert_not_called()

    def test_returns_none_on_imdb_error(self):
        """Upstream IMDbError is logged, not raised at the command."""
        client = MagicMock()
        client.search_movie.side_effect = IMDbError("upstream is down")
        with patch("shibabot.api.IMDb", return_value=client):
            assert get_imdb_movie("blade runner") is None

    def test_returns_none_when_get_movie_raises(self):
        """Regression: get_movie() sat outside the try block."""
        client = MagicMock()
        client.search_movie.return_value = [MagicMock()]
        client.get_movie.side_effect = IMDbError("lookup failed")
        with patch("shibabot.api.IMDb", return_value=client):
            assert get_imdb_movie("blade runner") is None


class TestBoxOffice:
    """Box office reporting handles partial and absent data."""

    def test_renders_available_figures(self):
        """Only the figures IMDB actually supplied are listed."""
        movie = MagicMock()
        movie.data = FULL_DATA
        result = imdb_box_office_data(movie)
        assert "BUDGET $28,000,000." in result
        assert "CUMULATIVE WORLDWIDE GROSS $41,722,000." in result
        assert "OPENING WEEK" not in result

    @pytest.mark.parametrize("data", [{}, {"box office": {}}, {"box office": None}])
    def test_returns_none_when_unavailable(self, data):
        """Missing or empty box office data yields None, not an empty string."""
        movie = MagicMock()
        movie.data = data
        assert imdb_box_office_data(movie) is None
