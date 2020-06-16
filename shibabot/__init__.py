"""Initialize bot."""
from random import randint
from datetime import datetime, timezone
import pytz
import requests
from discord.ext import commands
from config import GIPHY_API_KEY, GIPHY_API_ENDPOINT, DISCORD_GUILD
from .log import LOGGER


def create_bot():
    bot = commands.Bot(command_prefix='!')

    @bot.event
    async def on_ready():
        """Confirm bot is connected."""
        for guild in bot.guilds:
            if guild.name == DISCORD_GUILD:
                break

        LOGGER.info(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    @bot.command(name='420')
    async def time_remaining(ctx):
        """Get remaining time until target time."""
        now = datetime.now(tz=pytz.timezone('America/New_York'))
        am_time = now.replace(hour=4, minute=20, second=0)
        pm_time = now.replace(hour=16, minute=20, second=0)
        if am_time > now:
            diff = f'{am_time - now}'
        elif am_time < now and now < pm_time:
            diff = f'{pm_time - now}'
        else:
            tomorrow_am_time = now.replace(day=now.day+1, hour=4, minute=20, second=0)
            diff = f'{tomorrow_am_time - now}'
        diff = diff.split(':')
        await ctx.send(f'{diff[0]} hours, {diff[1]} minutes, & {diff[2]} seconds until 4:20')

    @bot.command(name='giphy', )
    async def giphy_image_search(ctx):
        """Giphy image search."""
        rand = randint(0, 20)
        params = {
            'api_key': GIPHY_API_KEY,
            'q': search_term,
            'limit': 1,
            'offset': rand,
            'rating': 'R',
            'lang': 'en'
        }
        req = requests.get(GIPHY_API_ENDPOINT, params=params)
        if bool(req.json()['data']):
            image = req.json()['data'][0]['images']['original']['url']
            await ctx.send(image)
        else:
            await ctx.send('image not found :(')

    return bot

