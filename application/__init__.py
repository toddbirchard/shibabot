"""Initialize bot."""
from discord.ext import commands
import datetime

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

    return bot
