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

class AnnounceView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)  # persistent view
        self.bot = bot

    def allowed(self, member):
        return member.id == config.OWNER_ID or any(
            r.id == config.LEAD_ADMIN_ROLE for r in member.roles
        )

    @discord.ui.button(
        label="📣 Server Announcement",
        style=discord.ButtonStyle.danger,
        custom_id="announce_server"  # required for persistent view
    )
    async def server_announce(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.allowed(interaction.user):
            return await interaction.response.send_message(
                "Only Owner & Lead Admin can use.", ephemeral=True
            )

        await interaction.response.send_message(
            "Type the server announcement:", ephemeral=True
        )

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60)
        except:
            return await interaction.followup.send("Timed out.", ephemeral=True)

        channel = self.bot.get_channel(config.SERVER_ANNOUNCE_CHANNEL)
        if channel is None:
            try:
                channel = await self.bot.fetch_channel(config.SERVER_ANNOUNCE_CHANNEL)
            except:
                return await interaction.followup.send("Announcement channel not found.", ephemeral=True)

        embed = discord.Embed(
            title="SERVER ANNOUNCEMENT",
            description=msg.content,
            color=0xFF0000,
            timestamp=discord.utils.utcnow()
        )

        await channel.send(content="@everyone", embed=embed)

        # logging
        local_log("ANNOUNCE", "Server announcement", staff=interaction.user, extra=msg.content)
        await discord_log(
            self.bot,
            "SERVER ANNOUNCEMENT",
            f"By: {interaction.user.mention}\n\n{msg.content}",
            color=0xFF0000
        )

        await msg.delete()
        await interaction.followup.send("Announcement sent.", ephemeral=True)

    @discord.ui.button(
        label="🧩 Patch Update",
        style=discord.ButtonStyle.primary,
        custom_id="announce_patch"  # required
    )
    async def patch(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.allowed(interaction.user):
            return await interaction.response.send_message(
                "Only Owner & Lead Admin can use.", ephemeral=True
            )

        await interaction.response.send_message(
            "Type the patch update:", ephemeral=True
        )

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60)
        except:
            return await interaction.followup.send("Timed out.", ephemeral=True)

        channel = self.bot.get_channel(config.PATCH_UPDATE_CHANNEL)
        if channel is None:
            try:
                channel = await self.bot.fetch_channel(config.PATCH_UPDATE_CHANNEL)
            except:
                return await interaction.followup.send("Patch channel not found.", ephemeral=True)

        embed = discord.Embed(
            title="PATCH UPDATE",
            description=msg.content,
            color=0x00BFFF,
            timestamp=discord.utils.utcnow()
        )

        await channel.send(embed=embed)

        # logging
        local_log("PATCH", "Patch update", staff=interaction.user, extra=msg.content)
        await discord_log(
            self.bot,
            "PATCH UPDATE",
            f"By: {interaction.user.mention}\n\n{msg.content}",
            color=0x00BFFF
        )

        await msg.delete()
        await interaction.followup.send("Patch update sent.", ephemeral=True)


class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.view = AnnounceView(bot)

    @commands.command()
    async def setup_announce_panel(self, ctx):
        if ctx.author.id != config.OWNER_ID:
            return

        channel = self.bot.get_channel(config.ANNOUNCE_PANEL_CHANNEL)
        if channel is None:
            try:
                channel = await self.bot.fetch_channel(config.ANNOUNCE_PANEL_CHANNEL)
            except:
                return await ctx.send("Panel channel not found.")

        try:
            async for msg in channel.history(limit=10):
                await msg.delete()
        except:
            pass

        embed = discord.Embed(
            title="ZETRA Announcement Panel",
            description="Owner & Lead Admin only",
            color=0x8B0000
        )

        await channel.send(embed=embed, view=self.view)

        # logging
        local_log("SYSTEM", "Announcement panel created", staff=ctx.author)
        await discord_log(
            self.bot,
            "ANNOUNCE PANEL",
            f"Panel created by {ctx.author.mention}",
            color=0x8B0000
        )


async def setup(bot):
    await bot.add_cog(Announce(bot))
