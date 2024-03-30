import discord
from discord import app_commands
from discord.ext import commands

troubleshooting_command_list = "**/troubleshooting auth** - Provides general information about Authentication Failed errors.\n" \
                               "**/troubleshooting ads** - Provides general information about Ad errors.\n" \
                               "**/commands troubleshooting** - The command you just used!"

gameinfo_command_list = "**/beta info** - Provides general information about the Beta program.\n" \
                        "**/beta join** - Guides you to joining the Beta program.\n" \
                        "**/beta leave** - Guides you to correctly leaving the Beta program.\n" \
                        "**/device emulator** - Guides you to playing the game on PC via an Emulator.\n" \
                        "**/device switch** - Guides you to correctly switching between your devices.\n" \
                        "**/device ios** - Guides you to loading your progress from Android to iOS and vice versa.\n" \
                        "**/commands gameinfo** - The command you just used!"

mechanics_command_list1 = "**/mechanics devastation** - Provides information about the Devastation mechanic.\n" \
                          "**/mechanics antimacro** - Provides information about the Anti-Macro feature.\n" \
                          "**/mechanics walls** - Provides information about Wall effects.\n" \
                          "**/mechanics quickstart** - Provides information about the Quickstart feature.\n" \
                          "**/mechanics galastall** -Provides information about the Galatine Stall team in Expedition.\n"

mechanics_command_list2 = "**/mechanics nmtime** - Provides information about the start time of Nightmare Expedition.\n" \
                          "**/mechanics idle** - Provides information about the Idle mechanic.\n" \
                          "**/mechanics howtobeat** - Provides information about different mob mechanics and how to " \
                          "beat them.\n" \
                          "**/mechanics afkassist** - Provides information about the premium AFK Assist pack.\n" \
                          "**/mechanics express** - Provides information about the premium Express pack.\n" \
                          "**/mechanics premiumsupporter** - Provides information about the premium Ad pack.\n" \
                          "**/mechanics purchase** - Provides information about the other premium purchases.\n" \
                          "**/mechanics cc** - Provides information about the 'CC' abbreviation.\n" \
                          "**/commands mechanics** - The command you just used!"

resources_command_list = "**/resources tickets** - Provides information about Tickets.\n" \
                         "**/resources using_tickets** - Provides information about correctly using Tickets.\n" \
                         "**/resources summon** - Provides information about Summons and Mass Summon.\n" \
                         "**/resources keys** - Provides information about Keys.\n" \
                         "**/resources using_keys** - Provides information about correctly using Keys.\n" \
                         "**/resources medals** - Provides information about Guild Medals.\n" \
                         "**/resources hearts** - Provides information about Hearts (Amity).\n" \
                         "**/resources evolutions** - Provides information about Hero Evolutions.\n" \
                         "**/resources rubies** - Provides information about Rubies.\n" \
                         "**/resources using_rubies** - Provides information about correctly using Rubies.\n" \
                         "**/resources bones** - Provides information about Bones (Fossils).\n" \
                         "**/commands resources** - The command you just used!"

runes_command_list = "**/runes info** - Provides general information about Runes.\n" \
                     "**/runes fusing** - Provides information about fusing Runes.\n" \
                     "**/runes fusing_efficiently** -Provides information about efficiently fusing Runes.\n" \
                     "**/runes unleash** - Provides information about unleashing Runes.\n" \
                     "**/runes cloning** - Provides information about cloning Runes.\n" \
                     "**/commands runes** - The command you just used!"

guilds_command_list = "**/guilds info** - Provides general information about Guilds.\n" \
                      "**/guilds create** - Provides information about creating Guilds.\n" \
                      "**/guilds roles** - Provides information about member roles inside Guilds.\n" \
                      "**/guilds shop** - Provides information about the Guild Shop.\n" \
                      "**/guilds hideout** - Provides information about the Guild Hideout.\n" \
                      "**/commands guilds** - The command you just used!"

hunt_command_list = "**/hunt info** - Provides general information about Hunt.\n" \
                    "**/hunt gear** - Provides information about (Hunt) Gear.\n" \
                    "**/hunt stats** - Provides information about (Hunt) Gear Stats.\n" \
                    "**/hunt scrolls** - Provides information about (Hunt) Scrolls.\n" \
                    "**/hunt transmog** - Provides information about (Hunt) Gear Transmog (changes gear appearance).\n" \
                    "**/hunt asmodeus** - Provides information about the Hunt Boss Asmodeus.\n" \
                    "**/hunt leviathan** - Provides information about the Hunt Boss Leviathan.\n" \
                    "**/hunt belphegor** - Provides information about the Hunt Boss Belphegor.\n" \
                    "**/hunt mammon** - Provides information about the Hunt Boss Mammon.\n" \
                    "**/commands hunt** - The command you just used!"

calc_command_list = "**/calc weapondamage** - Input the old & new day of your weapon to find out how many days you gain.\n" \
                    "**/calc daytodamage** - Input a Day to receive the estimate one-shot damage required to beat it.\n" \
                    "**/calc damagetoday** - Input the damage number of your DPS Hero to get an estimate of your " \
                    "one-shot pushing range.\n" \
                    "**/calc multiplier** - Input a damage multiplier to receive a Day equivalent.\n" \
                    "**/calc rewindspots** - Input a day & the days to look ahead to receive the Rewind Scores for " \
                    "the said spots. Max 500 at a time.\n" \
                    "**/calc detailed_rewindspot** - Input a day to receive detailed info on the spot (each Mob and " \
                    "Boss for each portal)\n" \
                    "**/calc best_rewindspot** - Input a day & the days to look ahead to receive the day with the best " \
                    "Rewind Score (no details on other spots).\n" \
                    "**/calc optimal_rewind** - Input your Elixir data (Elixir, EM, Skills) to receive the minimum amount of rewinds required" \
                    " for the desired amount of skills.\n" \
                    "**/calc dungeon_gold** - Input your dungeon data to receive the best way to spend your keys, given a Day target.\n" \
                    "**/commands calc** - The command you just used!"


command_list = "**/commands troubleshooting** - Provides a list of all commands related to Troubleshooting\n" \
               "**/commands gameinfo** - Provides a list of all commands related to Game info (Beta/Multiple Devices)\n" \
               "**/commands mechanics** - Provides a list of all commands related to various Game Mechanics\n" \
               "**/commands resources** - Provides a list of all commands related to various Resources\n" \
               "**/commands runes** - Provides a list of all commands related to Runes\n" \
               "**/commands guilds** - Provides a list of all commands related to Guilds\n" \
               "**/commands calc** - Provides a list of all commands related to Calculators (sheets and such)\n" \
               "**/commands list** - The command you just used!"


class Commands(commands.GroupCog, name="commands"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="troubleshooting", description="Provides a list of all commands related to "
                                                              "Troubleshooting")
    async def troubleshooting(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="List of all available troubleshooting commands", color=0x71368a)
        embed.add_field(name="", value=troubleshooting_command_list, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="gameinfo", description="Provides a list of all commands related to Game info "
                                                       "(Beta/Multiple Devices)")
    async def gameinfo(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="List of all available Game Info commands", color=0x71368a)
        embed.add_field(name="", value=gameinfo_command_list, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="mechanics", description="Provides a list of all commands related to various Game Mechanics")
    async def mechanics(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="List of all available Mechanics commands", color=0x71368a)
        embed.add_field(name="", value=mechanics_command_list1, inline=False)
        embed.add_field(name="", value=mechanics_command_list2, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="resources", description="Provides a list of all commands related to various Resources")
    async def resources(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="List of all available Resources commands", color=0x71368a)
        embed.add_field(name="", value=resources_command_list, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="runes", description="Provides a list of all commands related to Runes")
    async def runes(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="List of all available Runes commands", color=0x71368a)
        embed.add_field(name="", value=runes_command_list, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="guilds", description="Provides a list of all commands related to Guilds")
    async def guilds(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="List of all available Runes commands", color=0x71368a)
        embed.add_field(name="", value=guilds_command_list, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="hunt", description="Provides a list of all commands related to Hunt")
    async def hunt(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="List of all available Hunt commands", color=0x71368a)
        embed.add_field(name="", value=hunt_command_list, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="calc", description="Provides a list of all commands related to Calculators (sheets and such)")
    async def calc(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="List of all available Calculator commands", color=0x71368a)
        embed.add_field(name="", value=calc_command_list, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="list",
                          description="Provides a list of all available commands")
    async def commands(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title="List of all available commands", color=0x71368a)
        embed.add_field(name="", value=command_list, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Commands(bot))
