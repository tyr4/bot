import discord
from discord.ext import commands
from discord import app_commands

description = "》 Information about Guilds"
info_title1 = "Guilds"
info_description1 = "- Guilds are unlocked at Day 80. You can either join someone else's guild for free, or create your " \
                    "own for 500 Rubies."
info_description2 = "- Bulletin is place where you can chat with other guild members and also see relevant guild messages " \
              "like player joined, player left, promoted, demoted and if anything got changed in the settings."

info_title3 = "Guild Skills"
info_description3 = "They're not in the game yet! But we might get them in an upcoming update. Right now there is the " \
                    "ingame tab as a little teaser."
info_title4 = "Guild Raids"
info_description4 = "They're not in the game yet! But we might get them in an upcoming update. Right now we just have" \
                    " an NPC in the Hideout as a little teaser."


create_title = "How does creating your own guild work?"
create_description = "If you decide to create your own guild instead of joining one there are few steps to it.\n" \
                     "- Guild icon, you can choose between 28 different designs.\n" \
                     "- Color, you can choose between 6 different Colors and 4 different Accent colors, or you can tap " \
                     "on the random button and let the game select randomly.\n" \
                     "- Guild name, you can choose up to 15 characters.\n" \
                     "- Up to 20 people can join.\n" \
                     "- If you leave a guild, you will get a 24hour cooldown!" \
                     "- After creating the guild, you can still change many things except the name of your guild.\n" \
                     "- Description, where you can add any useful information about your guild, for example the" \
                     "required day for someone to join.\n" \
                     "- You can choose the Type of your guild, if its going to be an open guild or if people have to " \
                     "send a request."

roles_title = "Guild Roles"
roles_description = "There are currently 4 guild roles:\n" \
                    "- Member, a role which everyone gets when they join a guild for the first time.\n" \
                    "- Elder, can kick members out, promoted by either leader, co-leader or elder.\n" \
                    "- Co-leader, can kick both members and elders, accept requests to join their guild, can change" \
                    " the description and settings of the guild, promoted by leader.\n" \
                    "- Leader, owner of the guild, can kick anyone, can promote anyone, accept requests to join their" \
                    " guild, can change the description and settings, can pass leadership to a co-leader"

shop_title = "What is the purpose of Guilds?"
shop_description = "Guild Medals & Daily Check-ins. \n" \
                   "- Thanks to daily check-ins, you will be able to gain one <:Resource_GuildMedal:1016016279976550430>" \
                   " every day.\n" \
                   "- With guild medals, you can buy many things, but the most valuable resource in the Guild Store " \
                   "are scrolls." \
                   "- By checking in, you and all the guild members are contributing to get experience towards the next " \
                   "guild level which can be found above the guild icon."

hideout_title = "Guild Hideout"
hideout_description = "Here you can free-roam (walk around) and see other players! There is nothing to do in the " \
                      "hideout yet."


class Guilds(commands.GroupCog, name="guilds"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="info", description="Provides general information about Guilds")
    async def guilds_info(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=info_title1, value=info_description1, inline=False)
        embed.add_field(name="", value=info_description2, inline=False)
        embed.add_field(name=info_title3, value=info_description3, inline=False)
        embed.add_field(name=info_title4, value=info_description4, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="create", description="Provides information about creating Guilds")
    async def create(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=create_title, value=create_description, inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1102311924735168517/1170020063995240488/image.png")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="roles", description="Provides information about member roles inside Guilds")
    async def roles(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=roles_title, value=roles_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="shop", description="Provides information about the Guild Shop")
    async def shop(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=shop_title, value=shop_description, inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1102311924735168517/1170026587954090095/image.png?"
                            "ex=65578b2c&is=6545162c&hm=1de65091b7b69368bd848e569f30d1df3f6f4920c06f4bcc0d75263338aefc04&")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="hideout", description="Provides information about the Guild Hideout")
    async def hideout(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=hideout_title, value=hideout_description, inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1102311924735168517/1170026587601784912/image.png?e"
                            "x=65578b2c&is=6545162c&hm=2a1271e23894d6d839029cb5bd7a84401111dbffca23667f8a86dfbd6931bd60&")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Guilds(bot))

