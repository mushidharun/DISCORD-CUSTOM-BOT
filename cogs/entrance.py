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
import time

COOLDOWN_SECONDS = 5
user_cooldowns = {}

class EntranceView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # persistent view

    @discord.ui.button(
        label="RETYPE HERE", # RETEXT ANY OF YOUR NEED
        style=discord.ButtonStyle.danger,
        custom_id="entrance_enter_button"  # REQUIRED for persistence
    )
    async def enter_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        # Anti-spam cooldown
        now = time.time()
        if interaction.user.id in user_cooldowns:
            if now - user_cooldowns[interaction.user.id] < COOLDOWN_SECONDS:
                return await interaction.followup.send("Please wait before clicking again.")

        user_cooldowns[interaction.user.id] = now

        guild = interaction.guild
        if not guild:
            return await interaction.followup.send("Guild not found.")

        role = guild.get_role(config.MEMBER_ROLE)
        if not role:
            local_log("ENTRANCE", "Role not found", extra="MEMBER_ROLE invalid")
            return await interaction.followup.send("Access role not configured.")

        # Already has role
        if role in interaction.user.roles:
            try:
                await interaction.user.send(
                    "❌ You already have access to FIVEM BOT. You cannot access again."
                )
            except discord.Forbidden:
                pass

            local_log("ENTRANCE", "Tried to re-enter", user=interaction.user)
            await discord_log(
                interaction.client,
                "🚫 ENTRANCE DENIED",
                f"{interaction.user.mention} tried to enter again.",
                color=0xFF0000
            )

            return await interaction.followup.send("You already have access.")

        # Give role
        try:
            await interaction.user.add_roles(role, reason="Entrance system")
        except discord.Forbidden:
            local_log("ENTRANCE", "Role add failed", user=interaction.user)
            return await interaction.followup.send("Failed to grant access. Contact staff.")

        # DM welcome
        try:
            await interaction.user.send(
                "🔥 Welcome to FIVEM BOT!\nYou now have server login access."
            )
        except discord.Forbidden:
            pass

        # Logs
        local_log("ENTRANCE", "User entered", user=interaction.user)
        await discord_log(
            interaction.client,
            "🔥 NEW ENTRANCE",
            f"{interaction.user.mention} entered .",
            color=0x00FF00
        )

        print(f"[ENTRANCE] {interaction.user} joined.")

        await interaction.followup.send("✅ You are now a !")


class Entrance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(EntranceView())  # register persistent view

    @commands.command()
    async def setup_entrance(self, ctx):
        if ctx.author.id != config.OWNER_ID:
            return

        embed = discord.Embed(
            title="🔥 FIVEM BOT – ",
            description=(
                "Click the button below to enter the battlefield.\n\n"
                "**THE BATTLEFIELD IS READY FOR YOU**"
            ),
            color=0x8B0000
        )
        embed.set_footer(text="FIVEM BOT GATE System")

        await ctx.send(embed=embed, view=EntranceView())


async def setup(bot):
    await bot.add_cog(Entrance(bot))
