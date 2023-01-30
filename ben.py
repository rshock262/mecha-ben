import os
import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import logging
import json

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

@bot.command(aliases=["c"])
async def benchat(ctx, *, arg):
    completion = openai.Completion.create(
            model="text-curie-001",
            max_tokens=80,
            prompt=arg
            )
    await ctx.send(completion.choices[0].text)


@bot.command(aliases=["d"])
async def bendraw(ctx, *, arg):
    image = openai.Image.create(
            size="512x512",
            prompt=arg
            )
    await ctx.send(image.data[0].url)

@bot.command(aliases=["v"])
async def benverify(ctx):
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    moderate = openai.Moderation.create(
        input=message.content
        )
    await ctx.send("Flagged" if moderate.results[0].flagged else "Safe")
    await ctx.send(json.dumps(moderate.results[0].category_scores, indent=2))

# Discord bot token from dotenv
logger.info('Starting bot')
bot.run(os.environ.get("TOKEN"))
