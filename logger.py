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





import os
import datetime
import discord
import config

LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)


def local_log(category, action, user=None, staff=None, extra=None):
    """Save logs locally + print to console"""

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    file_path = os.path.join(LOG_FOLDER, f"{date}.log")
    line = f"[{time}] [{category}] {action}"

    if user:
        line += f" | User: {user}"
    if staff:
        line += f" | By: {staff}"
    if extra:
        line += f" | Info: {extra}"

    line += "\n"

    # write file
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as e:
        print(f"[LOGGER ERROR] Failed to write log file: {e}")

    # console output (IMPORTANT for debugging)
    print(line.strip())


async def discord_log(bot, title, description, color=0x8B0000):
    """Send logs to Discord channel safely"""

    try:
        # try cache first
        channel = bot.get_channel(config.LOG_CHANNEL)

        # fallback to fetch
        if channel is None:
            channel = await bot.fetch_channel(config.LOG_CHANNEL)

        if channel is None:
            local_log("LOGGER", "Channel not found", extra=str(config.LOG_CHANNEL))
            return

        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_footer(text="DEMON V Log System")

        await channel.send(embed=embed)

    except discord.Forbidden:
        local_log("LOGGER", "No permission to send log")
    except discord.HTTPException as e:
        local_log("LOGGER", "HTTP error", extra=str(e))
    except Exception as e:
        local_log("LOGGER", "Discord log failed", extra=str(e))
