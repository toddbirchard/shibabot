"""Register bot commands."""
from datetime import datetime
import pytz
from .charts import stock_price_chart, crypto_plotly_chart
from .api import (
    get_stock_price,
    get_giphy_image,
    get_wiki_summary,
    get_crypto_price,
    get_imdb_movie
)


def bot_commands(bot):
    """Register user-triggered commands to chatbot."""

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
            tomorrow_am_time = now.replace(day=now.day + 1, hour=4, minute=20, second=0)
            remaining = f'{tomorrow_am_time - now}'
        remaining = remaining.split(':')
        await ctx.send(f'{remaining[0]} hours, {remaining[1]} minutes, & {remaining[2]} seconds until 4:20')

    @bot.command(name='giphy', help='Search for a Giphy image.')
    async def giphy_search(ctx, query: str):
        """Giphy image search."""
        search_results = get_giphy_image(query)
        if bool(search_results):
            image = search_results[0]['images']['original']['url']
            await ctx.send(image)
        else:
            await ctx.send('image not found :(')

    @bot.command(name='stock', help='Get 30-day stock performance.')
    async def stock(ctx, symbol: str):
        """Fetch stock price and generate 30-day performance chart."""
        message, company = get_stock_price(symbol)
        chart = stock_price_chart(symbol, company)
        await ctx.send(f'{message} {chart}')

    @bot.command(name='crypto', help='Get 30-day crypto performance.')
    async def crypto(ctx, symbol: str):
        """Fetch crypto price and generate 30-day performance chart."""
        message = get_crypto_price(symbol)
        chart = crypto_plotly_chart(symbol)
        await ctx.send(f'{message} {chart}')

    @bot.command(name='wiki', help='Get Wikipedia page summary.')
    async def wiki(ctx, query: str):
        """Get summary of Wikipedia entry."""
        response = get_wiki_summary(query)
        await ctx.send(response)

    @bot.command(name='imdb', help='Get IMDB summary and boxoffice performance for a movie title.')
    async def imdb(ctx, query: str):
        """Movie summaries from IMDB."""
        response = get_imdb_movie(query)
        await ctx.send(response)

    return bot

