"""Bot configuration via environment variables."""
from os import getenv, environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# General
ENVIRONMENT = environ.get('ENVIRONMENT')
BASE_DIR = environ.get('BASE_DIR')

# Discord
DISCORD_TOKEN = environ.get('DISCORD_TOKEN')
DISCORD_CHANNEL_HACKERS = environ.get('DISCORD_CHANNEL_HACKERS')
DISCORD_CHANNEL_SHIBA = environ.get('DISCORD_CHANNEL_SHIBA')
DISCORD_GUILDS = [DISCORD_CHANNEL_HACKERS, DISCORD_CHANNEL_SHIBA]

# Database
DATABASE_URI = environ.get('DATABASE_URI')
DATABASE_COMMANDS_TABLE = environ.get('DATABASE_COMMANDS_TABLE')
DATABASE_WEATHER_TABLE = environ.get('DATABASE_WEATHER_TABLE')
DATABASE_ARGS = {'ssl': {'ca': f'{BASE_DIR}/creds/ca-certificate.crt'}}

# Giphy
GIPHY_API_KEY = environ.get('GIPHY_API_KEY')
GIPHY_API_ENDPOINT = 'https://api.giphy.com/v1/gifs/search'

# Gifs
GIPHY_API_KEY = environ.get('GIPHY_API_KEY')
GFYCAT_CLIENT_ID = environ.get('GFYCAT_CLIENT_ID')
GFYCAT_CLIENT_SECRET = environ.get('GFYCAT_CLIENT_SECRET')
REDGIFS_ACCESS_KEY = environ.get('REDGIFS_ACCESS_KEY')

# Stock
IEX_API_TOKEN = environ.get('IEX_API_TOKEN')
ALPHA_VANTAGE_API_KEY = environ.get('ALPHA_VANTAGE_API_KEY')

# Plotly
PLOTLY_API_KEY = getenv('PLOTLY_API_KEY')
PLOTLY_USERNAME = getenv('PLOTLY_USERNAME')
