"""External API integrations."""
from random import randint
from typing import Optional

import requests
import wikipediaapi
from emoji import emojize
from imdb import IMDb, IMDbError
from requests.exceptions import HTTPError

from config import GIPHY_API_KEY, WEATHERSTACK_API_KEY
from log import LOGGER


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
        req = requests.get("https://api.giphy.com/v1/gifs/search", params=params)
        if req.status_code != 200 or bool(req.json()["data"]) is False:
            return "image not found :("
        image = req.json()["data"][0]["images"]["downsized"]["url"]
        return image
    except HTTPError as e:
        LOGGER.error(f"Giphy failed to fetch `{query}`: {e.response.content}")
        return emojize(
            f":warning: yoooo giphy is down rn lmao :warning:", use_aliases=True
        )
    except LookupError as e:
        LOGGER.error(f"Giphy KeyError for `{query}`: {e}")
        return emojize(
            f":warning: holy sht u broke the bot im telling bro :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.error(f"Giphy unexpected error for `{query}`: {e}")
        return emojize(
            f":warning: AAAAAA I'M BROKEN WHAT DID YOU DO :warning:", use_aliases=True
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
    ia = IMDb()
    movie_id = None
    try:
        movies = ia.search_movie(movie_title)
        movie_id = movies[0].getID()
    except IMDbError as e:
        LOGGER.error(f"IMDB command threw error for command `{movie_title}`: {e}")
    if movie_id:
        movie = ia.get_movie(movie_id)
        cast = f"STARRING {', '.join([actor['name'] for actor in movie.data['cast'][:2]])}."
        art = movie.data.get("cover url", None)
        director = f"DIRECTED by {movie.data.get('director')[0].get('name')}."
        year = movie.data.get("year")
        genres = f"({', '.join(movie.data.get('genres'))}, {year})."
        title = f"{movie.data.get('title').upper()},"
        rating = f"{movie.data.get('rating')}/10"
        box_office = imdb_box_office_data(movie)
        synopsis = movie.data.get("synopsis")
        if synopsis:
            try:
                synopsis = synopsis[0]
                synopsis = " ".join(synopsis[0].split(". ")[:2])
            except KeyError as e:
                LOGGER.error(f"IMDB movie `{title}` does not have a synopsis: {e}")
        response = " ".join(
            filter(
                None, [title, rating, genres, cast, director, synopsis, box_office, art]
            )
        )
        return response


def imdb_box_office_data(movie) -> Optional[str]:
    """
    Get IMDB box office performance for a given film.

    :returns: Optional[str]
    """
    response = []
    if movie.data.get("box office", None):
        budget = movie.data["box office"].get("Budget", None)
        opening_week = movie.data["box office"].get(
            "Opening Weekend United States", None
        )
        gross = movie.data["box office"].get("Cumulative Worldwide Gross", None)
        if budget:
            response.append(f"BUDGET {budget}.")
        if opening_week:
            response.append(f"OPENING WEEK {opening_week}.")
        if gross:
            response.append(f"CUMULATIVE WORLDWIDE GROSS {gross}.")
        return " ".join(response)


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
            "http://api.urbandictionary.com/v0/define", params=params, headers=headers
        )
        results = req.json().get("list")
        if results:
            results = sorted(results, key=lambda i: i["thumbs_down"], reverse=True)
            definition = str(results[0].get("definition"))
            example = str(results[0].get("example"))
            word = word.upper()
            return f"{word}: {definition}. EXAMPLE: {example}."
    except HTTPError as e:
        LOGGER.error(
            f"HTTPError while trying to get Urban definition for `{word}`: {e.response.content}"
        )
        return emojize(
            f":warning: wtf urban dictionary is down :warning:", use_aliases=True
        )
    except LookupError as e:
        LOGGER.error(f"LookupError error when fetching Urban definition for `{word}`: {e}")
        return emojize(":warning: mfer you broke bot :warning:", use_aliases=True)
    except Exception as e:
        LOGGER.error(
            f"Unexpected error when fetching Urban definition for `{word}`: {e}"
        )
        return emojize(":warning: mfer you broke bot :warning:", use_aliases=True)


def get_weather(location: str) -> str:
    """
    Return temperature and weather per city/state/zip.

    :param str location: Weather search query

    :returns: str
    """
    endpoint = "http://api.weatherstack.com/current"
    params = {"access_key": WEATHERSTACK_API_KEY, "query": location, "units": "f"}
    try:
        req = requests.get(endpoint, params=params)
        data = req.json()
        condition = data["current"]["weather_descriptions"][0]
        icon_name = condition.lower()
        if "lightning" in icon_name or "storm" in icon_name:
            icon = emojize(":cloud_with_lightning_and_rain:", use_aliases=True)
        elif "snow" in icon_name or "ice" in icon_name:
            icon = emojize(":snowflake:", use_aliases=True)
        elif "rain" in icon_name or "showers" in icon_name:
            icon = emojize(":cloud_with_rain:", use_aliases=True)
        elif "cloudy" in icon_name or "partly" in icon_name:
            icon = emojize(":partly_sunny:", use_aliases=True)
        elif "cloud" in icon_name or "fog" in icon_name:
            icon = emojize(":cloud_with_rain:", use_aliases=True)
        else:
            icon = emojize(":sunny:", use_aliases=True)
        return (
            f'{data["request"]["query"]}:\n'
            f'{icon}  {data["current"]["weather_descriptions"][0]}.  {data["current"]["temperature"]}°f (feels like {data["current"]["feelslike"]}°f). \
               {data["current"]["precip"]}% precipitation.'
        )
    except HTTPError as e:
        LOGGER.error(f"Failed to get weather for `{location}`: {e.response.content}")
        return emojize(
            f":warning:️️ fk me the weather API is down :warning:",
            use_aliases=True,
        )
    except LookupError as e:
        LOGGER.error(f"LookupError while fetching weather for `{location}`: {e}")
        return emojize(
            f":warning:️️ omfg u broke the bot WHAT DID YOU DO IM DEAD AHHHHHH :warning:",
            use_aliases=True,
        )
    except Exception as e:
        LOGGER.error(f"Failed to get weather for `{location}`: {e}")
        return emojize(
            f":warning:️️ omfg u broke the bot WHAT DID YOU DO IM DEAD AHHHHHH :warning:",
            use_aliases=True,
        )
