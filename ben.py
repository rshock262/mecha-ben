import discord
import discord.ext
import openai
import logging
from dotenv import load_dotenv

load_dotenv()

openai.api_key=os.environ.get("OPENAI_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def benChat(ctx)
    completion = openai.Completion.create(
            model="text-ada-001",
            max_tokens=5,
            prompt=ctx.message
            )
    ctx.send(completion.choices[0].text)


@bot.command()
async def benDraw(ctx):
    image = openai.Image.create(
            size="512x512",
            prompt=ctx.message
            )
    ctx.send(image.data[0].url)

@bot.command()
async def benQuip(ctx):
    completion = openai.Completion.create(
            model="text-davinci-003",
            max_tokens=60,
            temperature=0.5,
            top_p=0.3,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            prompt=ctx.message
            )
    ctx.send(completion.choices[0].text)

bot.run(os.environ.get("TOKEN"))
