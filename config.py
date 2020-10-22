"""Configuration via environment variables."""
from os import environ, getenv, path

from dotenv import load_dotenv

# Load values from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

# General config
ENVIRONMENT = environ.get("ENVIRONMENT")
BASE_DIR = environ.get("BASE_DIR")

# Discord
DISCORD_TOKEN = environ.get("DISCORD_TOKEN")
DISCORD_CHANNEL_HACKERS = environ.get("DISCORD_CHANNEL_HACKERS")
DISCORD_CHANNEL_SHIBA = environ.get("DISCORD_CHANNEL_SHIBA")
DISCORD_CHANNEL_MAX = environ.get("DISCORD_CHANNEL_MAX")
DISCORD_GUILDS = [DISCORD_CHANNEL_HACKERS, DISCORD_CHANNEL_SHIBA, DISCORD_CHANNEL_MAX]

# Database
DATABASE_URI = environ.get("DATABASE_URI")
DATABASE_COMMANDS_TABLE = environ.get("DATABASE_COMMANDS_TABLE")
DATABASE_WEATHER_TABLE = environ.get("DATABASE_WEATHER_TABLE")
DATABASE_ARGS = {"ssl": {"ca": f"{BASE_DIR}/creds/ca-certificate.crt"}}

# Giphy
GIPHY_API_KEY = environ.get("GIPHY_API_KEY")
GIPHY_API_ENDPOINT = "https://api.giphy.com/v1/gifs/search"

# Stock
IEX_API_TOKEN = environ.get("IEX_API_TOKEN")
IEX_API_BASE_URL = "https://cloud.iexapis.com/stable/stock/"

# Crypto
ALPHA_VANTAGE_API_KEY = environ.get("ALPHA_VANTAGE_API_KEY")
ALPHA_VANTAGE_PRICE_BASE_URL = "https://api.cryptowat.ch/markets/bitfinex/"
ALPHA_VANTAGE_CHART_BASE_URL = "https://www.alphavantage.co/query/"

# Plotly
PLOTLY_API_KEY = getenv("PLOTLY_API_KEY")
PLOTLY_USERNAME = getenv("PLOTLY_USERNAME")

# Weather
WEATHERSTACK_API_KEY = environ.get("WEATHERSTACK_API_KEY")
