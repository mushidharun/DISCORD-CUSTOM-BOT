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
import sys
import platform
import asyncio
import config
from logger import local_log, discord_log

class OwnerView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.dm_cooldown = False

    def is_owner(self, member):
        return member.id == config.OWNER_ID

    async def deny(self, interaction):
        if interaction.response.is_done():
            await interaction.followup.send("Owner only.", ephemeral=True)
        else:
            await interaction.response.send_message("Owner only.", ephemeral=True)

    async def safe_reply(self, interaction, content=None, embed=None):
        if interaction.response.is_done():
            await interaction.followup.send(content=content, embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(content=content, embed=embed, ephemeral=True)

    # Shutdown Bot
    @discord.ui.button(
        label="Shutdown Bot",
        style=discord.ButtonStyle.danger,
        custom_id="owner_shutdown"
    )
    async def shutdown(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.is_owner(interaction.user):
            return await self.deny(interaction)

        await self.safe_reply(interaction, "Shutting down...")

        local_log("OWNER", "Shutdown Bot", staff=interaction.user)
        await discord_log(
            self.bot,
            "OWNER ACTION",
            f"Bot shutdown by {interaction.user.mention}",
            color=0xFF0000
        )

        await self.bot.close()

    # Restart Bot
    @discord.ui.button(
        label="Restart Bot",
        style=discord.ButtonStyle.secondary,
        custom_id="owner_restart"
    )
    async def restart(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.is_owner(interaction.user):
            return await self.deny(interaction)

        await self.safe_reply(interaction, "Restarting...")

        local_log("OWNER", "Restart Bot", staff=interaction.user)
        await discord_log(
            self.bot,
            "OWNER ACTION",
            f"Bot restart by {interaction.user.mention}",
            color=0xFFA500
        )

        os.execl(sys.executable, sys.executable, *sys.argv)

    # Clear Channel
    @discord.ui.button(
        label="Clear Channel",
        style=discord.ButtonStyle.primary,
        custom_id="owner_clear"
    )
    async def clear(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.is_owner(interaction.user):
            return await self.deny(interaction)

        deleted = 0
        async for msg in interaction.channel.history(limit=50):
            try:
                await msg.delete()
                deleted += 1
            except:
                pass

        local_log("OWNER", "Clear Channel", staff=interaction.user, extra=f"{deleted} messages")
        await discord_log(
            self.bot,
            "OWNER ACTION",
            f"Channel cleared by {interaction.user.mention} ({deleted} messages)",
            color=0x00BFFF
        )

        await self.safe_reply(interaction, "Channel cleared.")

    # Server Powered Up DM
    @discord.ui.button(
        label="Server Powered Up",
        style=discord.ButtonStyle.success,
        custom_id="owner_powered_up"
    )
    async def powered_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.is_owner(interaction.user):
            return await self.deny(interaction)

        if self.dm_cooldown:
            return await self.safe_reply(interaction, "DM system cooling down. Try later.")

        await self.safe_reply(interaction, "Sending power-up DM to all members...")

        self.dm_cooldown = True
        guild = interaction.guild
        sent = 0
        failed = 0

        for member in guild.members:
            if member.bot:
                continue

            try:
                await member.send(
                                    # TYPE ANY OF YOUR NEEDS
                )
                sent += 1
                await asyncio.sleep(0.8)
            except:
                failed += 1

        local_log("OWNER", "Server Powered Up DM", staff=interaction.user, extra=f"Sent: {sent}, Failed: {failed}")
        await discord_log(
            self.bot,
            "SERVER POWERED UP",
            f"DM sent to {sent} members by {interaction.user.mention}\nFailed: {failed}",
            color=0x00FF00
        )

        self.dm_cooldown = False

        await interaction.followup.send(
            f"Power-up alert sent.\nSuccess: {sent}\nFailed: {failed}",
            ephemeral=True
        )

    # System Info
    @discord.ui.button(
        label="System Info",
        style=discord.ButtonStyle.secondary,
        custom_id="owner_sysinfo"
    )
    async def info(self, interaction: discord.Interation, button: discord.ui.Button):
        if not self.is_owner(interaction.user):
            return await self.deny(interaction)

        embed = discord.Embed(title="BOT SYSTEM INFO", color=0x8B0000)
        embed.add_field(name="Platform", value=platform.system())
        embed.add_field(name="Python", value=platform.python_version())
        embed.add_field(name="Bot User", value=str(self.bot.user))

        local_log("OWNER", "Viewed System Info", staff=interaction.user)

        await self.safe_reply(interaction, embed=embed)


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.view = OwnerView(bot)

    @commands.command()
    async def setup_owner_panel(self, ctx):
        if ctx.author.id != config.OWNER_ID:
            return

        channel = self.bot.get_channel(config.OWNER_PANEL_CHANNEL)
        if not channel:
            return await ctx.send("Owner panel channel not found.")

        async for msg in channel.history(limit=10):
            try:
                await msg.delete()
            except:
                pass

        embed = discord.Embed(
            title="ZETRA'S OWNER PANEL",
            description="Absolute Control System",
            color=0x8B0000
        )
        await channel.send(embed=embed, view=self.view)


async def setup(bot):
    await bot.add_cog(Owner(bot))
