"""Register room actions."""
from .log import LOGGER


def bot_events(bot):
	"""Register actions to be taken upon room actions."""
	@bot.event
	async def on_ready():
		"""Confirm bot is connected."""
		for guild in bot.guilds:
			LOGGER.info(f'Connected to {guild.name}')

	return bot
