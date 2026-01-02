import discord
from discord.ext import commands
from discord import app_commands

wt_sheet_link = "https://docs.google.com/spreadsheets/d/1A-J5gifZtwgBL1_WzR9eXIM4InxccwyIc5f998ZPKXM/edit?gid=548764124#gid=548764124"
ticket_sheet_link = "https://docs.google.com/spreadsheets/d/156tZ418aGVTDE3DGZsQMdxTAhovNovknqfhtRBFAT8g/edit?gid=1084168163#gid=1084168163"
pushing_sheet_link = "https://docs.google.com/spreadsheets/d/1YHZTl2_Q7UQq31zEvjptA3eiBfhPGbGG6cQPC9CT2g8/edit#gid=1993682071"
masterlist_sheet_link = "https://docs.google.com/spreadsheets/d/1ywxGQw8yLPWrfTKK8W79Z8Na8gKuuYlnj368PNIfdKQ/edit?gid=0#gid=0"
wiki_link = "https://daysbygonewiki.miraheze.org/wiki/Main_Page"

class Sheet(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="wtcalc", description="Sends a link to the WT Planner sheet")
    async def send_wt_sheet(self, interaction: discord.Interaction):
        message = (f"<:WT_Apple:1019750592001867867> **[World Tree Calculator](<{wt_sheet_link}>)** <:WT_Apple:1019750592001867867>\n"
                   f"Use this to figure out where to invest your apples for the most optimal days of damage & Monarch's WT Planner to plan out your next World Tree Build!\n"
                   f"(short guide on how to use it here: https://discord.com/channels/570929677732937738/1191279847427817482/1191284734433706044)\n"
                   f"-# Don't forget to make a copy!")

        await interaction.response.send_message(message)

    @app_commands.command(name="ticketcalc", description="Sends a link to the Ticket sheet")
    async def send_ticket_sheet(self, interaction: discord.Interaction):
        message = (f"<:Resource_ticket:1137471573113176154> **[Hero Ticket/Catalyst Calculator](<{ticket_sheet_link}>)** <:Catalysts:1072001631941574697>\n"
                   f"Use this calculator to figure out how many hero copies/tickets it would take to get legendary heroes to x* as well as calculate catalysts needed for ascensions/nodes and the Tome in Dark\n"
                   f"-# Don't forget to make a copy!")

        await interaction.response.send_message(message)

    @app_commands.command(name="pushingcalc", description="Sends a link to N's Pushing sheet")
    async def send_pushing_sheet(self, interaction: discord.Interaction):
        message = (f"[Use this sheet to see how far in days you can push in the Campaign mode](<{pushing_sheet_link}>)\n"
                   f"*output will be a rough estimate")

        await interaction.response.send_message(message)

    @app_commands.command(name="assets", description="Information about free in-game assets")
    async def send_asset_info(self, interaction: discord.Interaction):
        message = (f"You might see sprites seen on DBG on other games as well, Idle Slayer being a common example.\n"
                   f"This is not plagiarism or anything of the sort, as many different games can purchase and use these sprites.\n"
                   f"This is the case for different mobs, heroes, as well as spell icons.")

        await interaction.response.send_message(message)

    @app_commands.command(name="masterlist", description="Sends a link to the Sheet Master List")
    async def send_masterlist_sheet(self, interaction: discord.Interaction):
        message = (f"**Master List of all community made sheets/calculators here:**\n"
                   f"<{masterlist_sheet_link}>")

        await interaction.response.send_message(message)

    @app_commands.command(name="wiki", description="Sends a link to the official DBG Wiki")
    async def send_wiki(self, interaction: discord.Interaction):
        message = (f"**Official Days Bygone Wiki**\n"
                   f"<{wiki_link}>")

        await interaction.response.send_message(message)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Sheet(bot))
