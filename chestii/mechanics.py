import discord
from discord.ext import commands
from discord import app_commands

description = "》 Information about Gamemodes and Mechanics"
devastation_title = "How does Devastation work?"
devastation_description = "Devastation is another layer of critical damage, so it's damage is equal to: \n" \
                          "**Damage x Crit Damage x Crit Damage = Devastation Damage**.\n" \
                          "Devastation Chance is based on your Crit Chance above 100% and your Devastation stat. " \
                          "For example, if you have 150% Crit Chance and level 2.5k Devastation, you will " \
                          "devastate 12.5% of the time (50% x 0.25). You need at least 200% Crit Chance to always " \
                          "devastate if your devastate stat is maxed out at 10k."

antimacro_title = "What are these circles or weapons I have to click when I go back to the shop?"
antimacro_description = "That's the anti-macro. It verifies that you are not breaking the rules. For the circles, " \
                        "just click on the them to finish it. If you get the gear or weapons list, you have to choose " \
                        "the right weapon based on it's name. If you are unsure what to choose, you can ask in <#696035168414072913>"

walls_title = "Which wall should I equip? / Do the wall effects stack?"
walls_description = "Which wall you equip is just a cosmetic choice, because all wall effects are passive, and stack " \
                    "additively. For example, that means if you buy the two +25% elixir walls, you'll have 50% more " \
                    "elixir regardless of which wall you have equipped, even if it's a gold or damage wall. "

quickstart_title = "What is Quickstart? When should I get it?"
quickstart_description = "Quickstart is an unlockable feature that you can buy when starting any Expedition run that " \
                         "costs 600 Rubies, which allows you to start Expedition (Easy/Normal/Hard/Hell) from a later " \
                         "point than 00:00. For example, if your personal best in Hell is 16:00, Quickstart will let " \
                         "you start Hell from 10:00. This speeds up the bones/hour that you get from Expedition." \
                         "\nBecause of other priorities to spend your rubies on, we generally recommend buying " \
                         "Quickstart if you have progressed past 20:00 in Hell. You can also buy it earlier if you " \
                         "have bought rubies."

galastall_title = "What is a good Hell/Nightmare team?"
galastall_description = "Before you reach Day 3k, use your best DPS hero (which is probably Eleanor), and some " \
                        "combination of CC (crowd control) and %hp, such as Mikhail, Dewitt, Evolved Hank, Max, Elaine," \
                        " Garp, Dark Merlin and Esther.\n\n" \
                        "Once you get to 3k, and have Weighted Shots awakened, you can do **Galatine Stall**. " \
                        "This is the best strategy for Nightmare all the way to Day 12k. You'll need the legendary " \
                        "weapon Galatine, that can be of any day, and use a combination of Mikhail, Dewitt, Max, " \
                        "Esther, Elaine and DM, Luna, Hank, hopefully all at 10*. If your Galatine is too old " \
                        "(over ~1000 days) spend 25 or 50% of your gold after rewinding into the damage stat before " \
                        "doing your runs.\n" \
                        "For Hell, you want to die as soon as you can't kill mobs anymore, you can achieve that by replacing " \
                        "1-2 CC heroes for more %hp and potentially using Cain."

nmtime_title = "What is Nightmare start time based on?"
nmtime_description = "Your starting time in Nightmare is based on your max Day in Campaign. Because of this, you " \
                     "should generally do your Nightmare runs for the day before you push. This changes once you can " \
                     "reach 10 minutes in Nightmare, around Day 12k. At that point, you can do them after pushing."

idle_title = "What is Idle?"
idle_description = "Idle is a mechanic in the game where your heroes will play while the game is closed, but only to " \
                   "a certain extent.\n\n" \
                   "If you are below your Max Day (the highest day you've reached in Campaign) when you close the game," \
                   " your heroes will slowly push towards it, but won't go above it. Once they get there, or if you " \
                   "closed the game already at max Day, they will also farm Idle/Passive Rewinds and Gold, once every " \
                   "60 or 45 minutes depending on your Idle Speed skill.\n\nIdle/Passive Rewinds will increase your " \
                   "Rewind Perks (-wave, portal chance, rewind speed, gilded portal chance), but won't generate any E" \
                   "lixir or Tickets, and are much slower than rewinding actively. Because of this, Idle isn't a very " \
                   "used mechanic, especially by higher day players."

howtobeat_title = "How do I beat this mob/boss?"
howtobeat_description = "In general, the answer to this question is always deal more damage, usually by rewinding more " \
                        "and upgrading your skills. Some mobs and bosses do have certain tricks to them though.\n\n" \
                        "Some mobs have resistances, so they can't be damaged by %current hp (purple damage), such as " \
                        "Warmongers and all mobs in Cyber; or %max hp (red/black damage), such as Sentinels, Banshees " \
                        "and Manaeaters.\n\n" \
                        "Most/all Campaign bosses can be killed with just %hp damage, but that requires specific " \
                        "heroes, such as Saul, DM and Esther for dealing damage, and lots of slow and freeze."

afkassist_title = "AFK Assist"
afkassist_description = "AFK Assist is the most expensive and most impactful pack. It allows your Defender (the guy " \
                        "with the weapon) to aim by himself, without the need for you to keep your finger on the screen" \
                        " and also attack portals and mobs automatically. The pack also allows you to overnight the " \
                        "Expedition Gamemode. Overnighting is letting the game run while you are asleep and it " \
                        "automatically restarting when you die. Finally, you will also get access to Auto-Discard in " \
                        "the Hunt game mode. This addition allows you to automatically discard items, of a specific " \
                        "rarity of your choosing, whilst farming bosses. AFK Assist also has a Pivot mode, where you" \
                        " can choose a point on the screen to aim at. Just hold the AFK Assist 'A' icon and drag it," \
                        " it'll turn blue and an X marker will appear on the screen, which you can move around to " \
                        "choose where to aim. This is particularly useful for some World Tree (10k plus, check " \
                        "<#1003735352034472046>) mechanics, such as BT/Smite and Mana Siphon."

express_title = "Express Pack"
express_description = "Express Pack, the second in priority pretty much just makes the game 2.5-3x faster overall, " \
                      "giving you 2x Rewind Speed and double portal skip. "

premiumsupporter_title = "Premium Supporter"
premiumsupporter_descrition = "Premium Supporter/Ad Pack, removes ads from the game while allowing you to use all the " \
                              "ad related bonuses instantly. This one is not as important as the others, but it lets " \
                              "you get 15 rubies for free every real life (RL) day, two revives per death on push and " \
                              "double crates on every boss without having to watch an ad every time, saving you some " \
                              "time, especially since Google/Apple can't always find a suitable ad for you. This in " \
                              "particular can happen at the end of a Dungeon run for example, not allowing you to " \
                              "double your keys."

purchases_title = "What about other purchases, what should I spend money on?"
purchases_description = "Before Day ~3000, Titan and Hero Chests are very good purchases, giving you a lot of " \
                        "Catalysts that will speed up your hero progress immensely in a stage where Dungeon takes " \
                        "way too long to farm, as well as a few rubies.\n\nAt Day 6000 you unlock the Pack of Scrolls " \
                        "purchase, which is very worth it during gear farming at Day 10000, since Scrolls are hard to " \
                        "come by and the more you have, the less time you have to spend farming. You still shouldn't " \
                        "use Scrolls before T10 Gear, unless you really don't mind spending a lot of money for slightly " \
                        "quicker progress.\n\nPlain rubies are always a good purchase, as you can use it to buy Elixir " \
                        "Walls, more Cyber Capacity, Rune and Gear slots, among other things.\n\nT" \
                        "he rest of the purchases are very underwhelming and give very little value for what they cost," \
                        " so steer away, especially from 'Legendary Hero', 'Legendary Weapon', 'Legendary Hero + Weapon'," \
                        " and the Catalyst Pack you can buy for rubies."

cc_title = "What does CC stand for?"
cc_description = "This sadly depends on context, as two things are abbreviated to CC.\n\n" \
                 "Crit Chance, which is used in the context of Devastation and talking about Runes.\n\n" \
                 "Crowd Control refers to heroes and spells that can restrict/hinder enemy movement. " \
                 "This includes things like slow, freeze, knockback, and knock-up."


class Mechanics(commands.GroupCog, name="mechanics"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="devastation", description="Provides information about the Devastation mechanic")
    async def devastation(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=devastation_title, value=devastation_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="antimacro", description="Provides information about the Anti-Macro feature")
    async def antimacro(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=antimacro_title, value=antimacro_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="walls", description="Provides information about Wall effects")
    async def walls(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=walls_title, value=walls_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="quickstart", description="rovides information about the Quickstart feature")
    async def quickstart(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=quickstart_title, value=quickstart_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="galastall", description="Provides information about the Galatine Stall tea")
    async def galastall(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=galastall_title, value=galastall_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="nmtime", description="Provides information about the start time of Nightmare Expedition")
    async def nmtime(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=nmtime_title, value=nmtime_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="idle", description="Provides information about the Idle mechanic")
    async def idle(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=idle_title, value=idle_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="howtobeat", description="Provides information about different mob mechanics and how to "
                                                   "beat them")
    async def howtobeat(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=howtobeat_title, value=howtobeat_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="afkassist", description="Provides information about the premium AFK Assist pack")
    async def afkassist(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=afkassist_title, value=afkassist_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="express", description="Provides information about the premium Express pack")
    async def express(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=express_title, value=express_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="premiumsupporter", description="Provides information about the premium Ad pack")
    async def premiumsupporter(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=premiumsupporter_title, value=premiumsupporter_descrition, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="purchases", description="Provides information about the other premium purchases")
    async def purchases(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=purchases_title, value=purchases_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="cc", description="Provides information about the 'CC' abbreviation")
    async def cc(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=cc_title, value=cc_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Mechanics(bot))