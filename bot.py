import discord
import logging


# Logging rec from the docs
logger = logging.getLogger('discord')

logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

logger.addHandler(handler)

# Connect client
client = discord.Client()



@client.event

async def on_ready():
    # Ret 2 go
    print('{0.user} is online'.format(client))



@client.event

async def on_message(message):
    # Don't respond to yourself robot
    if message.author == client.user:

        return


    if message.content.startswith('$hello'):

        await message.channel.send('Hullo?')


# Your token here!
client.run('')
