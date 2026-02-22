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
from logger import local_log

ALLOWED = [
    config.LEAD_ADMIN_ROLE,
    config.ADMIN_ROLE,
    config.MOD_ROLE
]

class AdminView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    def allowed(self, member):
        if member.id == config.OWNER_ID:
            return True
        return any(r.id in ALLOWED for r in member.roles)

    async def log(self, guild, msg):
        channel = self.bot.get_channel(config.ADMIN_LOG_CHANNEL)
        if channel:
            try:
                await channel.send(msg)
            except:
                pass

    async def safe_delete(self, message):
        try:
            await message.delete()
        except:
            pass

    async def ask_for_member(self, interaction):
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=30)
            if not msg.mentions:
                await interaction.followup.send("No user mentioned.", ephemeral=True)
                return None, msg
            return msg.mentions[0], msg
        except:
            await interaction.followup.send("Timed out. Try again.", ephemeral=True)
            return None, None

    @discord.ui.button(label="Kick", style=discord.ButtonStyle.danger, custom_id="admin_kick")
    async def kick(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.allowed(interaction.user):
            return await interaction.response.send_message("No permission.", ephemeral=True)

        await interaction.response.send_message("Mention user to kick:", ephemeral=True)
        member, msg = await self.ask_for_member(interaction)
        if not member:
            return

        try:
            await member.kick(reason="Kicked by admin panel")
        except:
            await interaction.followup.send("Failed to kick user.", ephemeral=True)
            return

        await self.log(interaction.guild, f"{member} kicked by {interaction.user}")
        local_log("ADMIN", "Kick", user=member, staff=interaction.user)

        await self.safe_delete(msg)

    @discord.ui.button(label="Mute", style=discord.ButtonStyle.secondary, custom_id="admin_mute")
    async def mute(self, interaction: discord.Interation, button: discord.ui.Button):
        if not self.allowed(interaction.user):
            return await interaction.response.send_message("No permission.", ephemeral=True)

        await interaction.response.send_message("Mention user to mute:", ephemeral=True)
        member, msg = await self.ask_for_member(interaction)
        if not member:
            return

        role = interaction.guild.get_role(config.MUTED_ROLE)
        if role:
            try:
                await member.add_roles(role)
            except:
                await interaction.followup.send("Failed to mute user.", ephemeral=True)
                return

            await self.log(interaction.guild, f"{member} muted by {interaction.user}")
            local_log("ADMIN", "Mute", user=member, staff=interaction.user)

        await self.safe_delete(msg)

    @discord.ui.button(label="Unmute", style=discord.ButtonStyle.success, custom_id="admin_unmute")
    async def unmute(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.allowed(interaction.user):
            return await interaction.response.send_message("No permission.", ephemeral=True)

        await interaction.response.send_message("Mention user to unmute:", ephemeral=True)
        member, msg = await self.ask_for_member(interaction)
        if not member:
            return

        role = interaction.guild.get_role(config.MUTED_ROLE)
        if role:
            try:
                await member.remove_roles(role)
            except:
                await interaction.followup.send("Failed to unmute user.", ephemeral=True)
                return

            await self.log(interaction.guild, f"{member} unmuted by {interaction.user}")
            local_log("ADMIN", "Unmute", user=member, staff=interaction.user)

        await self.safe_delete(msg)

    @discord.ui.button(label="Clear", style=discord.ButtonStyle.primary, custom_id="admin_clear")
    async def clear(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.allowed(interaction.user):
            return await interaction.response.send_message("No permission.", ephemeral=True)

        try:
            await interaction.channel.purge(limit=20)
        except:
            await interaction.followup.send("Failed to clear messages.", ephemeral=True)
            return

        await self.log(interaction.guild, f"Messages cleared by {interaction.user}")
        local_log("ADMIN", "Clear messages", staff=interaction.user, extra="20 messages")

        await interaction.response.send_message("Cleared.", ephemeral=True)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.view = AdminView(bot)

    @commands.command()
    async def setup_admin_panel(self, ctx):
        if ctx.author.id != config.OWNER_ID:
            return

        channel = self.bot.get_channel(config.ADMIN_PANEL_CHANNEL)
        if channel:
            async for msg in channel.history(limit=10):
                try:
                    await msg.delete()
                except:
                    pass

            embed = discord.Embed(
                title="DEMON V Admin Panel",
                description="Admin / Mod Controls",
                color=0x8B0000
            )
            await channel.send(embed=embed, view=self.view)


async def setup(bot):
    await bot.add_cog(Admin(bot))
