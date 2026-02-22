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

STATUS_MEDIA = {
    "restart": "https://media.discordapp.net/attachments/1419739427961573397/1419740661149597808/standard4-ezgif.com-optimize.gif?ex=6977a787&is=69765607&hm=60b0eb51f31cd22225828e1fb2a06d2ff243af92363a67b78eeef4288c36d57e&=",
    "dev": "https://cdn.discordapp.com/attachments/1419739427961573397/1465070874754416812/DEV_MODE.png?ex=6977c514&is=69767394&hm=6b392e4846a28cc88b845376a91cf359ff843554b5afdf239373da80b30691c3&",
    "shutdown": "https://media.discordapp.net/attachments/1419739427961573397/1465071709156802859/OFFLINE.png?ex=6977c5db&is=6976745b&hm=83e6be23ab87f2e423a7924e74590291a688c54f275f3bd18c1ea3a683678767&=&format=webp&quality=lossless",
    "back": "https://cdn.discordapp.com/attachments/1419739427961573397/1465072628040597614/ONLINE.png?ex=6977c6b6&is=69767536&hm=cb1f230824f8610c26d136d0bfc4829da438afb6e18c0d9c99c5af4172624340&",
    "online": "https://cdn.discordapp.com/attachments/1419739427961573397/1465092996998369384/Untitled_design.png?ex=6977d9ae&is=6976882e&hm=15124111b1e706cc91498edf41eb126c3fb06bb5d1157bcfbc8992521b714adf&",
}

ALLOWED_ROLE_IDS = [
    config.LEAD_ADMIN_ROLE,
    config.ADMIN_ROLE,
    config.MOD_ROLE,
    config.STAFF_ROLE
]

class StatusView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    def has_permission(self, member):
        if member.id == config.OWNER_ID:
            return True
        return any(r.id in ALLOWED_ROLE_IDS for r in member.roles)

    async def send_status(self, interaction, title, media_url):
        await interaction.response.defer(ephemeral=True)

        channel = self.bot.get_channel(config.STATUS_CHANNEL)
        if channel is None:
            try:
                channel = await self.bot.fetch_channel(config.STATUS_CHANNEL)
            except:
                return await interaction.followup.send("Status channel not found.")

        try:
            async for msg in channel.history(limit=15):
                await msg.delete()
        except:
            pass

        embed = discord.Embed(title=title, color=0xFF0000)
        embed.set_image(url=media_url)
        embed.set_footer(text="ZETRA'S Server Status")
        embed.timestamp = discord.utils.utcnow()

        await channel.send(content="@everyone", embed=embed)
        await interaction.followup.send("Status updated.")

        local_log("STATUS", title, staff=interaction.user)
        await discord_log(
            self.bot,
            "SERVER STATUS UPDATE",
            f"{title}\nBy: {interaction.user.mention}",
            color=0xFF0000
        )

    @discord.ui.button(label="Restart", style=discord.ButtonStyle.secondary, custom_id="status_restart")
    async def restart(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.has_permission(interaction.user):
            return await interaction.response.send_message("No permission.", ephemeral=True)
        await self.send_status(interaction, "SERVER RESTARTING", STATUS_MEDIA["restart"])

    @discord.ui.button(label="Dev Mode", style=discord.ButtonStyle.primary, custom_id="status_dev")
    async def dev(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.has_permission(interaction.user):
            return await interaction.response.send_message("No permission.", ephemeral=True)
        await self.send_status(interaction, "SERVER IN DEV MODE", STATUS_MEDIA["dev"])

    @discord.ui.button(label="Shutdown", style=discord.ButtonStyle.danger, custom_id="status_shutdown")
    async def shutdown(self, interaction: discord.Interation, button: discord.ui.Button):
        if not self.has_permission(interaction.user):
            return await interaction.response.send_message("No permission.", ephemeral=True)
        await self.send_status(interaction, "SERVER SHUTDOWN", STATUS_MEDIA["shutdown"])

    @discord.ui.button(label="Server Back", style=discord.ButtonStyle.success, custom_id="status_back")
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.has_permission(interaction.user):
            return await interaction.response.send_message("No permission.", ephemeral=True)
        await self.send_status(interaction, "SERVER BACK ONLINE", STATUS_MEDIA["back"])


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setup_status_panel(self, ctx):
        if ctx.author.id != config.OWNER_ID:
            return

        embed = discord.Embed(
            title="ZETRA'S Status Control Panel",
            description="Management Team can update server status using buttons.",
            color=0x8B0000
        )
        await ctx.send(embed=embed, view=StatusView(self.bot))

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(config.BOT_STATUS_CHANNEL)
        if channel is None:
            try:
                channel = await self.bot.fetch_channel(config.BOT_STATUS_CHANNEL)
            except:
                return

        embed = discord.Embed(title="BOT IS NOW ONLINE", color=0x00FF00)
        embed.set_image(url=STATUS_MEDIA["online"])
        await channel.send(content="@everyone", embed=embed)

        local_log("BOT", "Bot Online")
        await discord_log(self.bot, "BOT ONLINE", "ZETRA'S DISCORD BOT is now online.", color=0x00FF00)

    def cog_unload(self):
        channel = self.bot.get_channel(config.BOT_STATUS_CHANNEL)
        if channel:
            embed = discord.Embed(title="BOT IS GOING OFFLINE", color=0xFF0000)
            embed.set_image(url=STATUS_MEDIA["shutdown"])
            self.bot.loop.create_task(channel.send(content="@everyone", embed=embed))
            local_log("BOT", "Bot Offline")


async def setup(bot):
    await bot.add_cog(Status(bot))
