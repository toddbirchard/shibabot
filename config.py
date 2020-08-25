"""Configuration via environment variables."""
from os import getenv, environ, path
from dotenv import load_dotenv


# Load values from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

ENVIRONMENT = environ.get('ENVIRONMENT')
BASE_DIR = environ.get('BASE_DIR')

# Discord
DISCORD_TOKEN = environ.get('DISCORD_TOKEN')
DISCORD_GUILD = environ.get('DISCORD_GUILD')

# Database
DATABASE_URI = getenv('DATABASE_URI')
DATABASE_COMMANDS_TABLE = getenv('DATABASE_COMMANDS_TABLE')
DATABASE_WEATHER_TABLE = getenv('DATABASE_WEATHER_TABLE')
DATABASE_ARGS = {'ssl': {'ca': f'{BASE_DIR}/creds/ca-certificate.crt'}}

# Giphy
GIPHY_API_KEY = environ.get('GIPHY_API_KEY')
GIPHY_API_ENDPOINT = 'https://api.giphy.com/v1/gifs/search'

# Gifs
GIPHY_API_KEY = getenv('GIPHY_API_KEY')
GFYCAT_CLIENT_ID = getenv('GFYCAT_CLIENT_ID')
GFYCAT_CLIENT_SECRET = getenv('GFYCAT_CLIENT_SECRET')
REDGIFS_ACCESS_KEY = getenv('REDGIFS_ACCESS_KEY')

# Stock
IEX_API_TOKEN = getenv('IEX_API_TOKEN')
ALPHA_VANTAGE_API_KEY = getenv('ALPHA_VANTAGE_API_KEY')

# Plotly
PLOTLY_API_KEY = getenv('PLOTLY_API_KEY')
PLOTLY_USERNAME = getenv('PLOTLY_USERNAME')
