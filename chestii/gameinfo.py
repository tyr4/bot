import discord
from discord.ext import commands
from discord import app_commands

beta_description = "》 Information about the Beta Program"
beta_title1 = "What is Beta?"
beta_description1 = " The beta is an 'unstable' branch version of this game, meant for testing new features. " \
                    "Beta testers get updates in advance to test out their features and check for bugs but they risk" \
                    " game breaking bugs or losing progress (though both are very rare). Beta usually lasts a week or " \
                    "so, before that update gets released to everyone. There isn't always an active beta, since updates " \
                    "come out about once a month, and beta lasts only a week or two."

beta_title2 = "How do I join Beta? / Should I join Beta?"
beta_description2 = "You can join the Beta if you're on Android by going on the game's playstore page and scrolling to " \
                    "the Beta Tester section, and clicking Join. There is a chance that the Beta program is full when " \
                    "you try to join though. You should join the Beta if you want to help the developer test out new " \
                    "features and find bugs. You shouldn't join Beta expecting an advantage, because actual damage " \
                    "bonuses in Beta are usually disabled till the update gets released to everyone, and you will likely" \
                    " have to deal with bugs and possibly losing data."

beta_title3 = "I joined Beta, can I leave?"
beta_description3 = "You cannot leave while there is an active Beta, or you will be locked out of the game until the " \
                    "Beta is over. You can safely leave when there is not a Beta active. You may re-join the Beta if " \
                    "you accidentally leave, and you will be able to play it again. You can easily check if there is " \
                    "an active Beta by looking at the <#637388798396858379> channel and seeing if the channel is locked " \
                    "or unlocked."

device_description = "》 Information about Devices"
device_title1 = "Is there a possibility to play Days Bygone on PC?"
device_description1 = "Yes, you can play DBG on PC via an Emulator. You can pick which Emulator suits you the best, " \
                      "but the most common ones are Bluestacks and NOX. If the Emulator isn't working properly, " \
                      "you might have to turn on Virtualization in BIOS/UEFI."

device_title2 = "I play on multiple devices, how can I safely switch between them?"
device_description2 = "- Never have the game open on multiple devices at the same time." \
                      "- Enter Dungeon and get at least 1 Key to force a save update. This step is optional but helps " \
                      "to make sure." \
                      "- Press the back button and the Save & Exit menu will pop-up, accept it when you are done. " \
                      "For iOS, go to Settings and press the red button next to the Sign Out button." \
                      "- Open on other device."

device_title3 = "Want to play your account on both Android and iOS?"
device_description3 = "To be able to play on both Android and iOS, you need to first connect your account to a " \
                      "Facebook account. Once it's been connected, you can save and exit, go on your second device " \
                      "and connect with the Facebook account you used. Don't forget, game settings are stored on the " \
                      "device!"


class Beta(commands.GroupCog, name="beta"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="info", description="Provides general information about the Beta program")
    async def beta_info(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=beta_description, color=0x71368a)
        embed.add_field(name=beta_title1, value=beta_description1, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="join", description="Guides you to joining the Beta program")
    async def beta_join(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=beta_description, color=0x71368a)
        embed.add_field(name=beta_title2, value=beta_description2, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leave", description="Guides you to correctly leaving the Beta program")
    async def beta_leave(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=beta_description, color=0x71368a)
        embed.add_field(name=beta_title3, value=beta_description3, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)


class Devices(commands.GroupCog, name="device"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="emulator", description="Guides you to playing the game on PC via an Emulator")
    async def device_emulator(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=device_description, color=0x71368a)
        embed.add_field(name=device_title1, value=device_description1, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="switch", description="Guides you to correctly switching between your devices")
    async def device_switch(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=device_description, color=0x71368a)
        embed.add_field(name=device_title2, value=device_description2, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ios", description="Guides you to correctly switching between your devices")
    async def device_ios(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=device_description, color=0x71368a)
        embed.add_field(name=device_title3, value=device_description3, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Beta(bot))
    await bot.add_cog(Devices(bot))
