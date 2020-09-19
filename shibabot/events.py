"""Register room actions."""
from .log import LOGGER


def bot_events(bot):
	"""Register actions to be taken upon room actions."""
	@bot.event
	async def on_ready():
		"""Confirm bot is connected."""
		for guild in bot.guilds:
			LOGGER.info(f'Connected to {guild.name}')

	@bot.event
	async def on_message(message):
		"""Log chat messages"""
		LOGGER.info(message)

	@bot.event
	async def on_error(event, *args):
		"""Log chat messages"""
		LOGGER.error(f'Unhandled error: {event} | args: {" ".join(args)}')

	return bot
