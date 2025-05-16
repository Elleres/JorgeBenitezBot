import asyncio
import os
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

import discord

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user}")

async def main():
    async with bot:
        discord.opus.load_opus('/opt/homebrew/lib/libopus.0.dylib')
        await bot.load_extension("bot.extensions.music")
        await bot.start(TOKEN)

asyncio.run(main())