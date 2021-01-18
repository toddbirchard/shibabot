"""External API integrations."""
from random import randint
from typing import Optional

import emoji
import requests
import wikipediaapi
from imdb import IMDb, IMDbError
from requests.exceptions import HTTPError

from config import GIPHY_API_ENDPOINT, GIPHY_API_KEY, WEATHERSTACK_API_KEY
from shibabot.log import LOGGER


def get_giphy_image(query: str) -> str:
    """
    Search for Gif matching query.

    :param query: Image search query
    :type query: str
    :returns: str
    """
    error_message = "No image found for `query` lern2search smh."
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
        req = requests.get(GIPHY_API_ENDPOINT, params=params)
        image = req.json()["data"][0]["images"]["original"]["url"]
        return image
    except HTTPError as e:
        LOGGER.error(e)
        return error_message
    except KeyError as e:
        LOGGER.error(e)
        return error_message
    except Exception as e:
        LOGGER.error(e)
        return error_message


def get_wiki_summary(query: str) -> str:
    """
    Fetch Wikipedia summary for a given query.

    :param query: Wiki search query
    :type query: str
    :returns: str
    """
    wiki = wikipediaapi.Wikipedia("en")
    page = wiki.page(query)
    return page.summary[0:1000]


def get_imdb_movie(movie_title: str) -> Optional[str]:
    """
    Get movie information from IMDB.

    :param movie_title: IMDB movie search query
    :type movie_title: str
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
    return None


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
    return None


def get_urban_definition(word: str) -> Optional[str]:
    """
    Fetch UrbanDictionary word definition.

    :param word: UD search query
    :type word: str
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
            f"Failed to get Urban definition for `{word}`: {e.response.content}"
        )
        return f"I have no idea wtf ur tryna search for tbh."
    return None


def get_weather(weather_area: str) -> str:
    """
    Return temperature and weather per city/state/zip.

    :param weather_area: Weather search query
    :type weather_area: str
    :returns: str
    """
    endpoint = "http://api.weatherstack.com/current"
    params = {"access_key": WEATHERSTACK_API_KEY, "query": weather_area, "units": "f"}
    try:
        req = requests.get(endpoint, params=params)
        data = req.json()
        condition = data["current"]["weather_descriptions"][0]
        icon_name = condition.lower()
        if "lightning" in icon_name or "storm" in icon_name:
            icon = emoji.emojize(":cloud_with_lightning_and_rain:", use_aliases=True)
        elif "snow" in icon_name or "ice" in icon_name:
            icon = emoji.emojize(":snowflake:", use_aliases=True)
        elif "rain" in icon_name or "showers" in icon_name:
            icon = emoji.emojize(":cloud_with_rain:", use_aliases=True)
        elif "cloudy" in icon_name or "partly" in icon_name:
            icon = emoji.emojize(":partly_sunny:", use_aliases=True)
        elif "cloud" in icon_name or "fog" in icon_name:
            icon = emoji.emojize(":cloud_with_rain:", use_aliases=True)
        else:
            icon = emoji.emojize(":sunny:", use_aliases=True)
        return (
            f'{data["request"]["query"]}:\n'
            f'{icon}  {data["current"]["weather_descriptions"][0]}.  {data["current"]["temperature"]}°f (feels like {data["current"]["feelslike"]}°f). \
               {data["current"]["precip"]}% precipitation.'
        )
    except HTTPError as e:
        LOGGER.error(
            f"Failed to get weather for `{weather_area}`: {e.response.content}"
        )
        return f"I couldn't find shit for `{weather_area}` tf u searching for bruh."
    except Exception as e:
        LOGGER.error(
            f"Unexpected exception when fetching weather for `{weather_area}`: {e}"
        )
        return f"aw shit I just broke :("
