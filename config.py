"""Bot configuration via .env."""
from os import getenv, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

DISCORD_TOKEN = getenv('DISCORD_TOKEN')
GIPHY_API_KEY = getenv('GIPHY_API_KEY')
