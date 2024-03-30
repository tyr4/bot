import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta

description = "》 Information about Hunt"
info_title = "Hunt"
info_description = "Hunt is unlocked at **Day 1000**. \n" \
                   "Hunt is used to obtaining Gear.\n" \
                   "You will be introduced to 4 new Bosses\n" \
                   "Asmodeus  <:Boss_Asmodeus:1150185250174021683>  every X000\n" \
                   "Leviathan   <:Boss_Leviathan:1150185254498357321> every X250\n" \
                   "Belphegor  <:Boss_Belphegor:1150185251503611915> every X500\n" \
                   "Mammon    <:Boss_Mammon:1150185255974748390> every X750"

gear_title1 = "Gear"
gear_description1 = "There are 10 Tiers, 4 types of Gear and 4 types of Rarity you can obtain.\n" \
                   "Each Tier and Rarity provides different amount of damage / Quality of Life stats."

gear_title2 = "Types & Rarity"
gear_description2 = "There are 4 types of Gear for now, Headgear, Armor, Boots and Ring.\n" \
                    "And 4 types of Rarity, Legendary with 2% drop chance, Epic with 6% drop chance, Rare 26% and " \
                    "Common with 66%."

stats_title = "Main stats and Sub stats on Gear"
stats_description = "+Damage = Useless.\n" \
                    "+Crit damage% = Only useful for T1 and T2.\n" \
                    "xCrit damage/Damage/Hero damage/Spell damage = Used for T3+ (Spell damage useable at <#1003735352034472046> " \
                    "if you decide to go with the Conjurer path)\n" \
                    "xProjectile Damage = Only gives damage to your defender.\n" \
                    "+Health and Mana points.\n" \
                    "+Mana and Health Regen = Makes your Mana / Health regen faster.\n" \
                    "+Dodge = Max Dodge % you can have is 75% (Dodge gives your wall % to block / negate damage from " \
                    "enemies).\n" \
                    "+Crit chance = More critical chance, good use of this Sub stat is for T1 and T2, for better " \
                    "chance to devastate early on. \n" \
                    "+Agility =  If your Agility is past 10. Excess Agility is converted into X projectile damage " \
                    "(Only useful for <:Hero_kingarthur:703033728061931600> )."

scrolls_title1 = "Sub stats on Gear"
scrolls_description1 = "Sub stats can be rerolled with scrolls and Rubies.\n " \
                       "After a reroll, you will be given a **random** stat."

scrolls_title2 = "Cost of rerolling"
scrolls_description2 = "<:Resource_scroll:1149150845938708572>  - always 1 scroll per reroll.\n" \
                       "<:Resource_ruby:1038573545518813245> - Tier*20 = Ruby cost for the first reroll, then it " \
                       "scales additively. For example for T10 it would cost 200 Rubies for the first reroll, then +" \
                       "200 each reroll.\n\n" \
                       "**DO NOT SPEND SCROLLS, SAVE THEM FOR TIER 10 GEAR!**"

transmog_title = "How do I change a gear's Appearance?"
transmog_description = "NOT REC. BEFORE DAY 10,000/T10 GEAR BECAUSE OF RUBY COST"

asmodeus_title = "Asmodeus <:Boss_Asmodeus:1150185250174021683> "
asmodeus_description = "How to early AFK?\n" \
                       "Asmodeus can be killed with pure Max % HP and Curr % HP heroes.\n" \
                       "Such as <:Hero_nero:763654327465934868><:Hero_saul:977594194988236861><:Hero_merlin:703020" \
                       "597755510824><:Hero_darkmerlin:703020537089097789> for Max % HP.\n" \
                       "And <:Hero_esther:703019847768080444><:Hero_elden:703020676323475536><:Hero_auto_kek:101925" \
                       "4136086204477> for Curr % HP.\n" \
                       "Support: <:Hero_lilibeth:703020163158769785><:Hero_mikhail:703033570402238495><:Hero_luna:70" \
                       "3033646172602508><:Hero_max:703017718835838997><:Hero_dewitt:703020422005915658>\n" \
                       "If <:Hero_lilibeth:703020163158769785>  is 10* you can include her in the team setup to reduce" \
                       " Asmo's minion health regen.\n" \
                       "This strategy takes 6-8 minutes to kill him.\n" \
                       "Allows early farming for T10 helmet and getting faster to World Tree."

leviathan_title = "Leviathan <:Boss_Leviathan:1150185254498357321>"
leviathan_description = "Additionally, Leviathan is immune to all CC including Dewitt's uncleansable freeze and Mikhail's slow."

belphegor_title = "Belphegor <:Boss_Belphegor:1150185251503611915>"
belphegor_description = "Like Leviathan, Belphegor is also immune to Dewitt's and Mikhail's CC."

mammon_title = "Mammon <:Boss_Mammon:1150185255974748390>"
mammon_description = "Possibly AFK-able.\n" \
                     "Despite being immune to being frozen, with <:Hero_dewitt:703020422005915658> Uncleansable node, " \
                     "Mammon can be frozen + the freezing can be extended with <:Hero_cusack:703019574983000085>  and " \
                     "<:Hero_chandler:703019653064294470>.\n" \
                     "You can also achieve better time per kill. (assuming you are not already at the lowest possible)."


class Hunt(commands.GroupCog, name="hunt"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="info", description="Provides general information about Hunt")
    async def hunt_info(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=info_title, value=info_description, inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1102311924735168517/1170030002071425054/Untitled_08-21-2023_02-07-17.png")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="gear", description="Provides information about (Hunt) Gear")
    async def gear(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=gear_title1, value=gear_description1, inline=False)
        embed.add_field(name=gear_title2, value=gear_description2, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='timeouttt', description='timeouts a user for a specific time')
    async def timeouttt(self, interaction: discord.Interaction, member: discord.Member) -> None:
        duration = datetime.timedelta(minutes=1)
        await member.timeout_for(duration)
        await interaction.response.send_message(f'{member.mention} was timeouted until for {duration}', ephemeral=True)

    @app_commands.command(name="stats", description="Provides information about (Hunt) Gear Stats")
    async def stats(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=stats_title, value=stats_description, inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1102311924735168517/1170030812478046309/gearstats.png")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="scrolls", description="Provides information about (Hunt) Scrolls")
    async def scrolls(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=scrolls_title1, value=scrolls_description1, inline=False)
        embed.add_field(name=scrolls_title2, value=scrolls_description2, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="transmog", description="Provides information about (Hunt) Gear Transmog (changes gear apperrance)")
    async def transmog(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=transmog_title, value=transmog_description, inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1152329047431454780/1152329575049728160/stitchgif.gif")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="asmodeus", description="Provides information about the Hunt Boss Asmodeus")
    async def asmodeus(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=asmodeus_title, value=asmodeus_description, inline=False)
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1102311924735168517/1170034466341789716/image.png")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leviathan", description="Provides information about the Hunt Boss Leviathan")
    async def leviathan(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=leviathan_title, value=leviathan_description, inline=False)
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1102311924735168517/1170034466719273031/image2.png")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="belphegor", description="Provides information about the Hunt Boss Belphegor")
    async def belphegor(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=belphegor_title, value=belphegor_description, inline=False)
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1102311924735168517/1170034466987724840/image3.png")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="mammon", description="Provides information about the Hunt Boss Mammon")
    async def mammon(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=mammon_title, value=mammon_description, inline=False)
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1102311924735168517/1170034467377782874/image4.png")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Hunt(bot))