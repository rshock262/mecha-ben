import os
import discord
import logging


# Logging rec from the docs
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

handler_console = logging.StreamHandler()
handler_console.setLevel(logging.INFO)
logger.addHandler(handler_console)


# Connect client
client = discord.Client()


@client.event
async def on_ready():
    logger.info(f'{client.user} is online')


@client.event
async def on_message(message):
    # Don't respond to yourself robot
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hullo?')


if __name__ == "__main__":
    token = os.environ.get('DISCORD_TOKEN')

    logger.info('Starting bot...')
    client.run(token)
