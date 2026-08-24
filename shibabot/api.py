"""External API integrations."""

from random import randint
from typing import Optional

import requests
import wikipediaapi
from emoji import emojize
from imdb import IMDb, IMDbError
from requests.exceptions import HTTPError

from config import GIPHY_API_KEY, WEATHERSTACK_API_KEY
from logger import LOGGER


def get_giphy_image(query: str) -> str:
    """
    Search for Gif matching query.

    :param str query: Image search query

    :returns: str
    """
    rand = randint(0, 20)
    params = {
        "api_key": GIPHY_API_KEY,
        "q": query,
        "limit": 1,
        "offset": rand,
        "rating": "R",
        "lang": "en",
    }
    try:
        req = requests.get(
            "https://api.giphy.com/v1/gifs/search", params=params, timeout=20
        )
        if req.status_code != 200 or bool(req.json()["data"]) is False:
            return "image not found :("
        image = req.json()["data"][0]["images"]["downsized"]["url"]
        return image
    except HTTPError as e:
        LOGGER.error(f"Giphy failed to fetch `{query}`: {e.response.content}")
        return emojize(
            f":warning: yoooo giphy is down rn lmao :warning:\n\n{e}", language="en"
        )
    except LookupError as e:
        LOGGER.error(f"Giphy KeyError for `{query}`: {e}")
        return emojize(
            f":warning: holy sht u broke the bot im telling bro :warning:\n\n{e}",
            language="en",
        )
    except Exception as e:
        LOGGER.error(f"Giphy unexpected error for `{query}`: {e}")
        return emojize(
            f":warning: AAAAAA I'M BROKEN WHAT DID YOU DO :warning:\n\n{e}",
            language="en",
        )


def get_wiki_summary(query: str) -> str:
    """
    Fetch Wikipedia summary for a given query.

    :param str query: Wiki search query

    :returns: str
    """
    wiki = wikipediaapi.Wikipedia("en")
    page = wiki.page(query)
    return page.summary[0:1000]


def get_imdb_movie(movie_title: str) -> Optional[str]:
    """
    Get movie information from IMDB.

    :param str movie_title: IMDB movie search query

    :returns: Optional[str]
    """
    try:
        ia = IMDb()
        movies = ia.search_movie(movie_title)
        if not movies:
            LOGGER.warning(f"No IMDB results found for `{movie_title}`.")
            return None
        movie = ia.get_movie(movies[0].getID())
    except IMDbError as e:
        LOGGER.error(f"IMDB command threw error for command `{movie_title}`: {e}")
        return None
    except Exception as e:
        LOGGER.error(f"Unexpected error fetching IMDB movie `{movie_title}`: {e}")
        return None

    data = getattr(movie, "data", None) or {}
    title = data.get("title")
    if not title:
        LOGGER.warning(f"IMDB result for `{movie_title}` has no title.")
        return None

    # Each field is omitted entirely when IMDB doesn't supply it, rather than
    # rendering as "None" or a placeholder in the middle of the response.
    parts = [f"{title.upper()},"]

    rating = data.get("rating")
    if rating:
        parts.append(f"{rating}/10")

    genres = data.get("genres") or []
    year = data.get("year")
    descriptor = ", ".join([*genres, str(year)] if year else genres)
    if descriptor:
        parts.append(f"({descriptor}).")

    cast = [actor.get("name") for actor in (data.get("cast") or [])[:2]]
    cast = [name for name in cast if name]
    if cast:
        parts.append(f"STARRING {', '.join(cast)}.")

    directors = data.get("director") or []
    director = directors[0].get("name") if directors else None
    if director:
        parts.append(f"DIRECTED by {director}.")

    synopsis = data.get("synopsis")
    if synopsis:
        # `synopsis` is a list of blurbs; keep the first two sentences of the first.
        parts.append(". ".join(synopsis[0].split(". ")[:2]))

    box_office = imdb_box_office_data(movie)
    if box_office:
        parts.append(box_office)

    art = data.get("cover url")
    if art:
        parts.append(art)

    return " ".join(parts)


def imdb_box_office_data(movie) -> Optional[str]:
    """
    Get IMDB box office performance for a given film.

    :returns: Optional[str]
    """
    box_office = getattr(movie, "data", None) or {}
    box_office = box_office.get("box office") or {}
    fields = (
        ("Budget", "BUDGET"),
        ("Opening Weekend United States", "OPENING WEEK"),
        ("Cumulative Worldwide Gross", "CUMULATIVE WORLDWIDE GROSS"),
    )
    response = [
        f"{label} {box_office[key]}." for key, label in fields if box_office.get(key)
    ]
    return " ".join(response) or None


def get_urban_definition(word: str) -> Optional[str]:
    """
    Fetch UrbanDictionary word definition.

    :param str word: UD search query

    :returns: Optional[str]
    """
    params = {"term": word}
    headers = {"Content-Type": "application/json"}
    try:
        req = requests.get(
            "http://api.urbandictionary.com/v0/define",
            params=params,
            headers=headers,
            timeout=20,
        )
        req.raise_for_status()
        results = req.json().get("list")
        if results:
            results = sorted(results, key=lambda i: i["thumbs_down"], reverse=True)
            definition = str(results[0].get("definition"))
            example = str(results[0].get("example"))
            word = word.upper()
            return f"{word}: {definition}. EXAMPLE: {example}."
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError while trying to get Urban definition for `{word}`: {e.response}"
        )
        return emojize(
            ":warning: wtf urban dictionary is down :warning:", language="en"
        )
    except LookupError as e:
        LOGGER.error(
            f"LookupError error when fetching Urban definition for `{word}`: {e}"
        )
        return emojize(":warning: mfer you broke bot :warning:", language="en")
    except Exception as e:
        LOGGER.error(
            f"Unexpected error when fetching Urban definition for `{word}`: {e}"
        )
        return emojize(":warning: mfer you broke bot :warning:", language="en")


def get_weather(location: str) -> str:
    """
    Return temperature and weather per city/state/zip.

    :param str location: Weather search query

    :returns: str
    """
    endpoint = "http://api.weatherstack.com/current"
    params = {"access_key": WEATHERSTACK_API_KEY, "query": location, "units": "f"}
    try:
        req = requests.get(endpoint, params=params, timeout=20)
        req.raise_for_status()
        data = req.json()
        condition = data["current"]["weather_descriptions"][0]
        icon_name = condition.lower()
        if "lightning" in icon_name or "storm" in icon_name:
            icon = emojize(":cloud_with_lightning_and_rain:", language="en")
        elif "snow" in icon_name or "ice" in icon_name:
            icon = emojize(":snowflake:", language="en")
        elif "rain" in icon_name or "showers" in icon_name:
            icon = emojize(":cloud_with_rain:", language="en")
        elif "cloudy" in icon_name or "partly" in icon_name:
            icon = emojize(":partly_sunny:", language="en")
        elif "cloud" in icon_name or "fog" in icon_name:
            icon = emojize(":cloud_with_rain:", language="en")
        else:
            icon = emojize(":sunny:", language="en")
        return (
            f'{data["request"]["query"]}:\n'
            f'{icon}  {data["current"]["weather_descriptions"][0]}.  {data["current"]["temperature"]}°f (feels like {data["current"]["feelslike"]}°f). \
               {data["current"]["precip"]}% precipitation.'
        )
    except HTTPError as e:
        LOGGER.error(f"Failed to get weather for `{location}`: {e.response}")
        return emojize(
            ":warning:️️ fk me the weather API is down :warning:",
            language="en",
        )
    except LookupError as e:
        LOGGER.error(f"LookupError while fetching weather for `{location}`: {e}")
        return emojize(
            ":warning:️️ omfg u broke the bot WHAT DID YOU DO IM DEAD AHHHHHH :warning:",
            language="en",
        )
    except Exception as e:
        LOGGER.error(f"Failed to get weather for `{location}`: {e}")
        return emojize(
            ":warning:️️ omfg u broke the bot WHAT DID YOU DO IM DEAD AHHHHHH :warning:",
            language="en",
        )
