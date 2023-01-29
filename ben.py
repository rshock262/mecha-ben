import os
import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import logging


# Logging rec from the docs
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

handler_console = logging.StreamHandler()
handler_console.setLevel(logging.INFO)
logger.addHandler(handler_console)

# Load all the environment variables using ".env"
load_dotenv()

# OpenAI key from dotenv
openai.api_key=os.environ.get("OPENAI_KEY")

# Intents are what all the bot is allowed to do via privileged gateway
intents = discord.Intents.default()
intents.message_content = True

#bot commands start with '!'
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def benChat(ctx):
    completion = openai.Completion.create(
            model="text-curie-001",
            max_tokens=80,
            prompt=ctx.message.content
            )
    await ctx.send(completion.choices[0].text)


@bot.command()
async def benDraw(ctx):
    image = openai.Image.create(
            size="512x512",
            prompt=ctx.message.content
            )
    await ctx.send(image.data[0].url)

# Discord bot token from dotenv
logger.info('Starting bot')
bot.run(os.environ.get("TOKEN"))
