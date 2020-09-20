"""Register bot commands."""
from datetime import datetime
import pytz
from discord.ext.commands import Bot
from handlers import crypto_chart_handler, stock_chart_handler
from .api import (
    get_giphy_image,
    get_wiki_summary,
    get_imdb_movie,
    get_urban_definition,
    get_weather
)


def bot_commands(bot) -> Bot:
    """Register user-triggered commands to chat bot."""

    @bot.command(name='420', help='Get time remaining until that time of day.')
    async def time_remaining(ctx):
        """Get remaining time until target time."""
        now = datetime.now(tz=pytz.timezone('America/New_York'))
        am_time = now.replace(hour=4, minute=20, second=0)
        pm_time = now.replace(hour=16, minute=20, second=0)
        if am_time > now:
            remaining = f'{am_time - now}'
        elif am_time < now < pm_time:
            remaining = f'{pm_time - now}'
        else:
            tomorrow_am_time = now.replace(
                day=now.day + 1,
                hour=4,
                minute=20,
                second=0
            )
            remaining = f'{tomorrow_am_time - now}'
        remaining = remaining.split(':')
        await ctx.send(
            f'{remaining[0]} hours, {remaining[1]} minutes, & {remaining[2]} seconds until 4:20'
        )

    @bot.command(name='giphy', help='Search for a Giphy image.', aliases=["!"])
    async def giphy_search(ctx, *args):
        """Giphy image search."""
        query = " ".join(args[:])
        search_results = get_giphy_image(query)
        if bool(search_results):
            image = search_results[0]['images']['original']['url']
            await ctx.send(image)
        else:
            await ctx.send('image not found :(')

    @bot.command(name='stock', help='Get 30-day stock performance.')
    async def stock(ctx, symbol: str):
        """Fetch stock price and generate 30-day performance chart."""
        chart = stock_chart_handler.get_chart(symbol)
        await ctx.send(chart)

    @bot.command(name='crypto', help='Get 60-day crypto performance.')
    async def crypto(ctx, symbol: str):
        """Fetch crypto price and generate 60-day performance chart."""
        chart = crypto_chart_handler.get_chart(symbol)
        await ctx.send(chart)

    @bot.command(name='wiki', help='Get Wikipedia page summary.')
    async def wiki(ctx, *args):
        """Get summary of Wikipedia entry."""
        query = " ".join(args[:])
        response = get_wiki_summary(query)
        await ctx.send(response)

    @bot.command(name='imdb', help='Get IMDB summary and box office performance for a movie title.')
    async def imdb(ctx, *args):
        """Movie summaries from IMDB."""
        movie_title = " ".join(args[:])
        response = get_imdb_movie(movie_title)
        await ctx.send(response)

    @bot.command(name='urban', help='Get a definition from UrbanDictionary.', alias='define')
    async def urban(ctx, *args):
        word = " ".join(args[:])
        response = get_urban_definition(word)
        await ctx.send(response)

    @bot.command(name='weather', help='Get weather conditions for a given city, area, or zip code.')
    async def weather(ctx, area: str):
        response = get_weather(area)
        await ctx.send(response)

    return bot
