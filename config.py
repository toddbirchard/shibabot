"""Bot configuration via environment variables."""
from os import getenv, environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

ENVIRONMENT = environ.get('ENVIRONMENT')
DISCORD_TOKEN = environ.get('DISCORD_TOKEN')
DISCORD_GUILD = environ.get('DISCORD_GUILD')
GIPHY_API_KEY = environ.get('GIPHY_API_KEY')
GIPHY_API_ENDPOINT = 'https://api.giphy.com/v1/gifs/search'
