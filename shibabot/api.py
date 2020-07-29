"""External APIs."""
from random import randint
import requests
import wikipediaapi
from imdb import IMDb, IMDbError
from .log import LOGGER
from config import (
    IEX_API_TOKEN,
    IEX_API_BASE_URL,
    GIPHY_API_KEY,
    GIPHY_API_ENDPOINT,
    ALPHA_VANTAGE_PRICE_BASE_URL
)


@LOGGER.catch
def get_giphy_image(query):
    """Search for Gif matching query."""
    image = 'No image found... lern2search smh'
    rand = randint(0, 20)
    params = {
        'api_key': GIPHY_API_KEY,
        'q': query,
        'limit': 1,
        'offset': rand,
        'rating': 'R',
        'lang': 'en'
    }
    try:
        req = requests.get(GIPHY_API_ENDPOINT, params=params)
        image = req.json()['data']
    except KeyError as e:
        LOGGER.error(e)
    return image


@LOGGER.catch
def get_stock_price(symbol):
    """Summarize 24-hour price fluctuation."""
    params = {'token': IEX_API_TOKEN}
    req = requests.get(
        f'{IEX_API_BASE_URL}{symbol}/quote',
        params=params
    )
    if req.status_code == 200:
        price = req.json().get('latestPrice', None)
        company_name = req.json().get("companyName", None)
        if price and company_name:
            message = f"{company_name}: Current price of ${price:.2f}."
            change = req.json().get("ytdChange", None)
            if change:
                message = f"{message} Change of {change:.2f}%"
            return message, company_name
    return f'There\'s no such company as {symbol}.'


@LOGGER.catch
def get_crypto_price(symbol):
    """Get crypto price for provided ticker label."""
    endpoint = f'{ALPHA_VANTAGE_PRICE_BASE_URL}{symbol.lower()}usd/summary'
    req = requests.get(url=endpoint)
    prices = req.json()["result"]["price"]
    percentage = prices["change"]['percentage'] * 100
    if prices["last"] > 1:
        response = f'{symbol.upper()}: Currently at ${prices["last"]:.2f}. ' \
                   f'HIGH today of ${prices["high"]:.2f}, LOW of ${prices["low"]:.2f} ' \
                   f'(change of {percentage:.2f}%).'
    else:
        response = f'{symbol.upper()}: Currently at ${prices["last"]}. ' \
                   f'HIGH today of ${prices["high"]} LOW of ${prices["low"]} ' \
                   f'(change of {percentage:.2f}%).'
    return response


@LOGGER.catch
def get_wiki_summary(query):
    """Fetch Wikipedia summary for a given query."""
    wiki = wikipediaapi.Wikipedia('en')
    page = wiki.page(query)
    return page.summary[0:300]


@LOGGER.catch
def get_imdb_movie(movie_title):
    """Get movie information from IMDB."""
    ia = IMDb()
    movie_id = None
    try:
        movies = ia.search_movie(movie_title)
        movie_id = movies[0].getID()
    except IMDbError as e:
        LOGGER.error(f'IMDB command threw error for command `{movie_title}`: {e}')
    if movie_id:
        movie = ia.get_movie(movie_id)
        cast = f"STARRING {', '.join([actor['name'] for actor in movie.data['cast'][:2]])}."
        art = movie.data.get('cover url', None)
        director = f"DIRECTED by {movie.data.get('director')[0].get('name')}."
        year = movie.data.get('year')
        genres = f"({', '.join(movie.data.get('genres'))}, {year})."
        title = f"{movie.data.get('title').upper()},"
        rating = f"{movie.data.get('rating')}/10"
        boxoffice = get_imdb_boxoffice_data(movie)
        synopsis = movie.data.get('synopsis')
        if synopsis:
            try:
                synopsis = synopsis[0]
                synopsis = ' '.join(synopsis[0].split('. ')[:2])
            except KeyError as e:
                LOGGER.error(f'IMDB movie `{title}` does not have a synopsis: {e}')
        response = ' '.join(filter(None, [title, rating, genres, cast, director, synopsis, boxoffice, art]))
        return response
    return None


@LOGGER.catch
def get_imdb_boxoffice_data(movie):
    """Get IMDB box office performance for a given film."""
    response = []
    if movie.data.get('box office', None):
        budget = movie.data['box office'].get('Budget', None)
        opening_week = movie.data['box office'].get('Opening Weekend United States', None)
        gross = movie.data['box office'].get('Cumulative Worldwide Gross', None)
        if budget:
            response.append(f"BUDGET {budget}.")
        if opening_week:
            response.append(f"OPENING WEEK {opening_week}.")
        if gross:
            response.append(f"CUMULATIVE WORLDWIDE GROSS {gross}.")
        return ' ' .join(response)
    return None
