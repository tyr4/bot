import discord
from discord.ext import commands
from discord import app_commands
import datetime
import time

from chestii.wrapped import update_wrapped_data

wt_sheet_link = "https://docs.google.com/spreadsheets/d/1A-J5gifZtwgBL1_WzR9eXIM4InxccwyIc5f998ZPKXM/edit?gid=548764124#gid=548764124"
ticket_sheet_link = "https://docs.google.com/spreadsheets/d/156tZ418aGVTDE3DGZsQMdxTAhovNovknqfhtRBFAT8g/edit?gid=1084168163#gid=1084168163"
pushing_sheet_link = "https://docs.google.com/spreadsheets/d/1YHZTl2_Q7UQq31zEvjptA3eiBfhPGbGG6cQPC9CT2g8/edit#gid=1993682071"
masterlist_sheet_link = "https://docs.google.com/spreadsheets/d/1ywxGQw8yLPWrfTKK8W79Z8Na8gKuuYlnj368PNIfdKQ/edit?gid=0#gid=0"
wiki_link = "https://daysbygonewiki.miraheze.org/wiki/Main_Page"
cybers_site_link_wt = "https://dbg-calculator.vercel.app/pages/worldtree.html"
cybers_site_link = "https://dbg-calculator.vercel.app"
dark_sheet_link = "https://docs.google.com/spreadsheets/d/1Q1c3qUT74m3kT6ePJOm-Nib05v7I1Ua5AB9XdKn6HME/edit?gid=0#gid=0"

def get_event_week_data():
    start_date = datetime.datetime(2026, 3, 29, 12, 0, tzinfo=datetime.timezone.utc)
    end_date = datetime.datetime(2100, 12, 31, 12, 0, tzinfo=datetime.timezone.utc)

    current_event = 1
    zile_luni = []
    
    while start_date <= end_date:
        if start_date.weekday() == 0:
            current_event += 1
            temp = [start_date, current_event]
            zile_luni.append(temp)

        start_date += datetime.timedelta(days=1)

    next_event = datetime.datetime.now(tz=datetime.timezone.utc)
    for monday in zile_luni:
        if next_event > monday[0]:
            current_event = monday[1]
        else:
            next_event_timestamp = monday[0].timestamp()
            break

    embed = discord.Embed(title="Event rotation <a:kafkakurukuru:1118233531110412461>", color=0x71368a)
    current_week = " <--- we are here"

    embed.add_field(name="", value=f"Next event is <t:{next_event_timestamp:.0f}:R>", inline=False)


    embed.add_field(name="Week 1" + (current_week if current_event == 0 else ""), value="<:Resource_Elixir:1155243501181730817> Elixir Rush", inline=False)

    embed.add_field(name="Week 2" + (current_week if current_event == 1 else ""), value="<:Resource_cyberCore:1052007235217268777> Elixir Overdrive\n "
                                            "<:NightmareFuel:894994680570335252> Nightmare Rush\n"
                                            "<:Resource_TimeStone:1169945471003938858> Time Rush", inline=False)

    embed.add_field(name="Week 3" + (current_week if current_event == 2 else ""), value="<:Resource_Elixir:1155243501181730817> Elixir Rush\n"
                                            "<:Resource_ticket:1137471573113176154> Ticket Rush", inline=False)

    embed.add_field(name="Week 4" + (current_week if current_event == 3 else ""), value="<:Resource_cyberCore:1052007235217268777> Ticket Overdrive\n"
                                            "<:Resource_TimeStone:1169945471003938858> Time Rush", inline=False)

    embed.add_field(name="Every Wednesday", value="<a:Gilded_portal:774161972240711680> Gilded Rush", inline=False)
    
    embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                    icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
    
    return embed

class Sheet(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="wtcalc", description="Sends a link to the WT Planner sheet")
    async def send_wt_sheet(self, interaction: discord.Interaction):
        message = (f"<:WT_Apple:1019750592001867867> **[World Tree Calculator](<{wt_sheet_link}>)** <:WT_Apple:1019750592001867867>\n"
                   f"Use this to figure out where to invest your apples for the most optimal days of damage & Monarch's WT Planner to plan out your next World Tree Build!\n"
                   f"(short guide on how to use it here: https://discord.com/channels/570929677732937738/1191279847427817482/1191284734433706044 - don't forget to make a copy!)\n"
                   f"\nYou can also try out **[Cyber's site](<{cybers_site_link_wt}>)** for a better experience")

        if interaction.guild.id == 570929677732937738 and interaction.user.id == 1123936489303195660 and interaction.channel.id != 699337693238263900:
            await interaction.response.send_message("<#699337693238263900> exists bro", ephemeral=True)
        else:
            await interaction.response.send_message(message)

        await update_wrapped_data("wtcalc", username=interaction.user.name, user_id=interaction.user.id)

    @app_commands.command(name="ticketcalc", description="Sends a link to the Ticket sheet")
    async def send_ticket_sheet(self, interaction: discord.Interaction):
        message = (f"<:Resource_ticket:1137471573113176154> **[Hero Ticket/Catalyst Calculator](<{ticket_sheet_link}>)** <:Catalysts:1072001631941574697>\n"
                   f"Use this calculator to figure out how many hero copies/tickets it would take to get legendary heroes to x* as well as calculate catalysts needed for ascensions/nodes and the Tome in Dark\n"
                   f"-# Don't forget to make a copy!")

        if interaction.guild.id == 570929677732937738 and interaction.user.id == 1123936489303195660 and interaction.channel.id != 699337693238263900:
            await interaction.response.send_message("<#699337693238263900> exists bro", ephemeral=True)
        else:
            await interaction.response.send_message(message)
        await update_wrapped_data("ticketcalc", username=interaction.user.name, user_id=interaction.user.id)

    @app_commands.command(name="pushingcalc", description="Sends a link to N's Pushing sheet")
    async def send_pushing_sheet(self, interaction: discord.Interaction):
        message = (f"[Use this sheet to see how far in days you can push in the Campaign mode](<{pushing_sheet_link}>)\n"
                   f"*output will be a rough estimate")

        if interaction.guild.id == 570929677732937738 and interaction.user.id == 1123936489303195660 and interaction.channel.id != 699337693238263900:
            await interaction.response.send_message("<#699337693238263900> exists bro", ephemeral=True)
        else:
            await interaction.response.send_message(message)
        await update_wrapped_data("pushingcalc", username=interaction.user.name, user_id=interaction.user.id)

    @app_commands.command(name="assets", description="Information about free in-game assets")
    async def send_asset_info(self, interaction: discord.Interaction):
        message = (f"You might see sprites seen on DBG on other games as well, Idle Slayer being a common example.\n"
                   f"This is not plagiarism or anything of the sort, as many different games can purchase and use these sprites.\n"
                   f"This is the case for different mobs, heroes, as well as spell icons.")

        if interaction.guild.id == 570929677732937738 and interaction.user.id == 1123936489303195660 and interaction.channel.id != 699337693238263900:
            await interaction.response.send_message("<#699337693238263900> exists bro", ephemeral=True)
        else:
            await interaction.response.send_message(message)
        await update_wrapped_data("assets", username=interaction.user.name, user_id=interaction.user.id)

    @app_commands.command(name="masterlist", description="Sends a link to the Sheet Master List")
    async def send_masterlist_sheet(self, interaction: discord.Interaction):
        message = (f"**Master List of all community made sheets/calculators here:**\n"
                   f"<{masterlist_sheet_link}>")

        if interaction.guild.id == 570929677732937738 and interaction.user.id == 1123936489303195660 and interaction.channel.id != 699337693238263900:
            await interaction.response.send_message("<#699337693238263900> exists bro", ephemeral=True)
        else:
            await interaction.response.send_message(message)
        await update_wrapped_data("masterlist", username=interaction.user.name, user_id=interaction.user.id)

    @app_commands.command(name="wiki", description="Sends a link to the official DBG Wiki")
    async def send_wiki(self, interaction: discord.Interaction):
        message = (f"**Official Days Bygone Wiki**\n"
                   f"<{wiki_link}>")

        if interaction.guild.id == 570929677732937738 and interaction.user.id == 1123936489303195660 and interaction.channel.id != 699337693238263900:
            await interaction.response.send_message("<#699337693238263900> exists bro", ephemeral=True)
        else:
            await interaction.response.send_message(message)
        await update_wrapped_data("wiki", username=interaction.user.name, user_id=interaction.user.id)

    @app_commands.command(name="dancy", description="Sends a dancy")
    async def send_dancy(self, interaction: discord.Interaction):
        message = "<a:dancy:1461348000977653760>"
        
        if interaction.guild.id == 570929677732937738 and interaction.user.id == 1123936489303195660 and interaction.channel.id != 699337693238263900:
            await interaction.response.send_message("<#699337693238263900> exists bro", ephemeral=True)
        else:
            await interaction.response.send_message(message)
        await update_wrapped_data("dancy", username=interaction.user.name, user_id=interaction.user.id)
    
    @app_commands.command(name="website", description="Sends a link to Cyber's website")
    async def send_website(self, interaction: discord.Interaction):
        message = f"DBG Site with most sheets/formulas: {cybers_site_link}"

        if interaction.guild.id == 570929677732937738 and interaction.user.id == 1123936489303195660 and interaction.channel.id != 699337693238263900:
            await interaction.response.send_message("<#699337693238263900> exists bro", ephemeral=True)
        else:
            await interaction.response.send_message(message)
        await update_wrapped_data("website", username=interaction.user.name, user_id=interaction.user.id)

    @app_commands.command(name="darksheet", description="Sends a link to the Lost Chapter Costs sheet")
    async def send_dark_sheet(self, interaction: discord.Interaction):
        message = f"You can find all Dark Tome buff values and costs here: <{dark_sheet_link}>"

        if interaction.guild.id == 570929677732937738 and interaction.user.id == 1123936489303195660 and interaction.channel.id != 699337693238263900:
            await interaction.response.send_message("<#699337693238263900> exists bro", ephemeral=True)
        else:
            await interaction.response.send_message(message)
        await update_wrapped_data("darksheet", username=interaction.user.name, user_id=interaction.user.id)
    
    @app_commands.command(name="events", description="Sends the event schedule")
    async def send_events(self, interaction: discord.Interaction):
        embed = get_event_week_data()

        if interaction.guild.id == 570929677732937738 and interaction.user.id == 1123936489303195660 and interaction.channel.id != 699337693238263900:
            await interaction.response.send_message("<#699337693238263900> exists bro", ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed)
        await update_wrapped_data("events", username=interaction.user.name, user_id=interaction.user.id)

    @app_commands.command(name="worldtreeactivity", description="Launch the World Tree Discord Activity")
    async def worldtreeactivity(self, interaction: discord.Interaction):
        try:
            await interaction.response.launch_activity()
        except Exception as error:
            debug_log(f"/worldtreeactivity failed for user {interaction.user.id}: {type(error).__name__}: {error}")
            if interaction.response.is_done():
                await interaction.followup.send(
                    "Couldn't launch the World Tree Activity.",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    "Couldn't launch the World Tree Activity.",
                    ephemeral=True,
                )

        await update_wrapped_data("worldtreeactivity", username=interaction.user.name, user_id=interaction.user.id)
        


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Sheet(bot))
