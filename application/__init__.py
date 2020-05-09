"""Initialize bot."""
from discord.ext import commands
import datetime
import requests
from random import randint
from config import GIPHY_API_KEY


def create_bot():
    bot = commands.Bot(command_prefix='!')

    @bot.command(name='420')
    async def time_remaining(ctx):
        """Get remaining time until target."""
        now = datetime.datetime.now()
        am_time = now.replace(hour=4, minute=20, second=0)
        pm_time = now.replace(hour=16, minute=20, second=0)
        if am_time > now:
            diff = str(am_time - now)
        else:
            diff = str(pm_time - now)
        diff = diff.split(':')
        await ctx.send(f'{diff[0]} hours, {diff[1]} minutes, {diff[2]} seconds, until 4:20.')

    @bot.command(name='giphy')
    async def giphy_image_search(ctx):
        """Giphy image search."""
        rand = randint(0, 20)
        params = {'api_key': GIPHY_API_KEY,
                  'q': search_term,
                  'limit': 1,
                  'offset': rand,
                  'rating': 'R',
                  'lang': 'en'}
        res = requests.get('https://api.giphy.com/v1/gifs/search', params=params)
        if len(res.json()['data']):
            image = res.json()['data'][0]['images']['original']['url']
            await ctx.send(image)
        else:
            await ctx.send('image not found :(')

    return bot
