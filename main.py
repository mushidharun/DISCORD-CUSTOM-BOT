# =========================================================
#  ZETRA DISCORD FIVEM BOT – COMMERCIAL EDITION
#
#  COPYRIGHT OWNER : MUSHI DHARUN (ZETRA)
#  PRICE : DM ME DIRECTLY OR CONTACT IN MY SERVER
#  SERVER : https://discord.gg/uxMjPz749k
#
#  This software is proprietary and confidential.
#  Unauthorized copying, modification, resale,
#  redistribution, or sharing is strictly prohibited.
#
#  Legal action may be taken for violations.
# =========================================================




import discord
from discord.ext import commands
import os
import config
import asyncio
import traceback
import logging
from datetime import datetime

# BASIC SECURITY CHECK

if not hasattr(config, "TOKEN") or not config.TOKEN:
    raise RuntimeError("TOKEN missing in config.py")

# CONSOLE LOG SYSTEM

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# INTENTS

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# READY EVENT

@bot.event
async def on_ready():
    logging.info(f"ZETRA DISCORD FIVEM BOT Logged in as {bot.user} (ID: {bot.user.id})")
    logging.info(f"Connected to {len(bot.guilds)} guild(s)")

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game("ZETRA DISCORD FIVEM BOT")
    )

    # Re-register persistent views (fix buttons not working after restart)
    for cog in bot.cogs.values():
        if hasattr(cog, "view"):
            try:
                bot.add_view(cog.view)
            except Exception as e:
                logging.warning(f"View load failed: {e}")


# GLOBAL ERROR HANDLER

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  

    logging.error(f"Command Error: {error}")
    traceback.print_exc()

    try:
        await ctx.send("An error occurred. Check console.", delete_after=5)
    except:
        pass


# INTERACTION ERROR FIX

@bot.event
async def on_error(event, *args, **kwargs):
    logging.error(f"Unhandled Event Error: {event}")
    traceback.print_exc()


# LOAD COGS

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logging.info(f"Loaded: {filename}")
            except Exception as e:
                logging.error(f"Failed to load {filename}: {e}")


# SAFE START

async def main():
    try:
        async with bot:
            await load_cogs()
            await bot.start(config.TOKEN)
    except Exception as e:
        logging.critical(f"Bot crashed: {e}")
        traceback.print_exc()

# RUN LOOP

if __name__ == "__main__":
    asyncio.run(main())
