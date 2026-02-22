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
import config
from logger import local_log, discord_log

ALLOWED = [
    config.LEAD_ADMIN_ROLE,
    config.ADMIN_ROLE,
    config.MOD_ROLE,
    config.STAFF_ROLE
]

class Forward(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def allowed(self, member):
        if member.id == config.OWNER_ID:
            return True
        return any(r.id in ALLOWED for r in member.roles)

    @commands.command()
    async def forward(self, ctx):
        if not self.allowed(ctx.author):
            return

        await ctx.send("Type the message to forward:")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        # Get message to forward
        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60)
        except:
            return await ctx.send("Timed out.", delete_after=5)

        await ctx.send("Mention the channel to send:")

        # Get target channel
        try:
            ch_msg = await self.bot.wait_for("message", check=check, timeout=30)
        except:
            return await ctx.send("Timed out.", delete_after=5)

        if not ch_msg.channel_mentions:
            return await ctx.send("No channel mentioned.", delete_after=5)

        target = ch_msg.channel_mentions[0]

        # Send message
        try:
            await target.send(msg.content)
        except discord.Forbidden:
            return await ctx.send("No permission to send in that channel.", delete_after=5)

        # Logs
        local_log(
            "FORWARD",
            "Message forwarded",
            staff=ctx.author,
            extra=f"To #{target.name} | {msg.content}"
        )

        await discord_log(
            self.bot,
            "MESSAGE FORWARDED",
            f"By: {ctx.author.mention}\nTo: {target.mention}\n\n{msg.content}",
            color=0x8B0000
        )

        # Safe delete
        try:
            await msg.delete()
        except:
            pass

        try:
            await ch_msg.delete()
        except:
            pass

        await ctx.send("Message sent silently.", delete_after=5)


async def setup(bot):
    await bot.add_cog(Forward(bot))
