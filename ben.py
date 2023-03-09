import os
import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import logging
import json
from duckduckgo_search import ddg
from PIL import Image
import requests
from io import BytesIO

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

@bot.command(aliases=["test"],
             help="I say Pong")
async def ping(ctx):
    await ctx.send("Pong")

@bot.command(aliases=["g"],
             help="Get the first search result")
async def search(ctx, *, arg):
    result = ddg(arg)[0]
    # I think there's a more pythonic way to do this,
    # but I also want it to not embed using the chevrons... TOO BAD!
    output = result["title"] + "\n" + result["body"] + "\n<" + result["href"] + ">"
    await ctx.send(output)

@bot.command(aliases=["c"],
             help="I talk back to you when you say things")
async def benchat(ctx, *, arg):
    completion = openai.Completion.create(
            model="text-davinci-003",
            max_tokens=4000,
            prompt=arg
            )
    await ctx.send(completion.choices[0].text)

@bot.command(aliases=["d"],
             help="I draw you a nice picture")
async def bendraw(ctx, *, arg):
    image = openai.Image.create(
            size="512x512",
            prompt=arg
            )
    await ctx.send(image.data[0].url)

@bot.command(aliases=["rd"],
             help="I redraw an image")
async def benredraw(ctx, *, arg):
    imgUrl = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    image = Image.open(BytesIO(requests.get(imgUrl.content))) # this is getting the image file the wrong way. Needs a 'bytes like file'
    edit = openai.Image.create_edit(
            image=image,
            size="512x512",
            prompt=arg
            )
    await ctx.send(edit.data[0].url)

@bot.command(aliases=["v"],
             help="I check if what you reply to is based or cringe")
async def benverify(ctx):
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    moderate = openai.Moderation.create(
        input=message.content
        )
    await ctx.send("Toxic" if moderate.results[0].flagged else "Safe")
    if moderate.results[0].flagged:
        await ctx.send(json.dumps(moderate.results[0].categories, indent=2))

@bot.command(aliases=["e"],
             help="I do what you tell me to do to a message you reply to")
async def benedit(ctx, *, arg):
    change = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    edit = openai.Edit.create(
        model="text-davinci-edit-001",
        input=change.content,
        instruction=arg
        )
    await ctx.send(edit.choices[0].text)

# Discord bot token from dotenv
logger.info('Starting bot')
bot.run(os.environ.get("TOKEN"))
