"""External APIs."""
from random import randint
import requests
import wikipediaapi
from config import IEX_API_TOKEN, GIPHY_API_KEY, GIPHY_API_ENDPOINT
from .log import LOGGER


@LOGGER.catch
def get_giphy_image(query):
    """Search for Gif matching query."""
    rand = randint(0, 20)
    params = {
        'api_key': GIPHY_API_KEY,
        'q': query,
        'limit': 1,
        'offset': rand,
        'rating': 'R',
        'lang': 'en'
    }
    req = requests.get(GIPHY_API_ENDPOINT, params=params)
    return req.json()['data']


@LOGGER.catch
def get_stock_price(symbol):
    """Summarize 24-hour price fluctuation."""
    params = {'token': IEX_API_TOKEN}
    req = requests.get(
        f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote',
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
    endpoint = f'https://api.cryptowat.ch/markets/bitfinex/{symbol.lower()}usd/summary'
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
