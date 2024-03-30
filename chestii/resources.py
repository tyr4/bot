import discord
from discord.ext import commands
from discord import app_commands

description = "》 Information about Resources"
tickets_title = "How to get Tickets?"
tickets_description = "- You can get Tickets from rewinding, bone/amity/key Shop (+their weekly deals), check-ins, " \
                      "Ticket Usher and Vermilion (<#1055815369866088529>).\n" \
                      "- The main source of gaining Tickets is rewinding.\n" \
                      "- You have a 4% base chance to get a Ticket from a boss.\n" \
                      "- Each time you skip a Boss day with Portal, you get a chance to get a Ticket from the portal " \
                      "as well.\n" \
                      "- First 10 <:Resource_ticket:1137471573113176154> of the day - 4% stated grows by another 4% per ticket not dropped," \
                      " to the max of 10%. After 10 <:Resource_ticket:1137471573113176154>  dropped, it's just 4% base again."

summon_title = "Should I do 1 or 10 Summons?/What is Mass Summon?"
summon_description = "You should always do 10x summons only as it guarantees an Epic Hero.\n" \
                     "The option to use Mass Summon is unlocked and visible as long as you have 1000+ " \
                     "<:Resource_ticket:1137471573113176154>. 1000 Tickets is the minimum amount you can spend and " \
                     "you can choose to increase the amount in increments of 100 Tickets."

using_tickets_title = "How to use Tickets responsibly/When should I save Tickets?"
using_tickets_description = "Firstly, you should switch from Classic Heroes to New Age Heroes and get a single copy " \
                            "of <:Hero_mikhail:703033570402238495>. Once you get him, you can switch back to Classic Heroes.\n" \
                            "You should get <:Hero_eleanor:703019878453346374> to 10:React_red_star: as soon as possible.\n" \
                            "After you get <:Hero_eleanor:703019878453346374>  to 10 <a:React_red_star:622060909312868352>, " \
                            "you can start saving up for ONE of the TOP 3 DPS Heroes. Your choice is either " \
                            "<:Hero_nero:763654327465934868>, <:Hero_lilith:703020228984045618> or <:Hero_kingarthur:703033728061931600>.\n" \
                            "These heroes become the most useful once they get to 10 <a:React_red_star:62206090931286" \
                            "8352> as this unlocks the ability to purchase one of their end nodes. To achieve this, a " \
                            "hero requires approximately 2000 <:Resource_ticket:1137471573113176154> due to a 2%, " \
                            "during their rate up."

keys_title1 = "How to get Keys?"
keys_description1 = "You can only get Keys from the Dungeon game mode which unlocks at Day 15. The amount of Keys you " \
                    "can get depends on what Floor you choose. Floor = Keys per minute (Assuming you use the Ad to " \
                    "double the outcome). For example, floor 8000 = 8000 keys per minute (if doubled)."

keys_title2 = "What Floor should I pick? Does it matter?"
keys_description2 = "No, it does not matter if floor 166 has Caps in it, and floor 137 has Rexes in it, you will get " \
                    "the same result.\n" \
                    "BUT, you want to get on a Floor where <:Hero_eleanor:703019878453346374>  one shots everything, " \
                    "it's completely normal to drop even 100s of days down. DO NOT use any other heroes with her. " \
                    "The reason for that is because you can experience lag and the game can even crash, which means " \
                    "you could lose an overnight worth of Keys. You wont see it, but you will notice it once you for " \
                    "example, sleep for 6 hours, and the game gives you a outcome of 5 hours."

using_keys_title = "I got X amount of Keys, now what?"
using_keys_description = "The main reason to farm keys overnight is to afford a decent amount of Catalysts... You will need " \
                    "a quite a lot. Each Catalyst costs 10,000 <:Resource_key:1052006772291936329>.\n" \
                    "Once you make a purchase, you will randomly receive 1 of the 8 types of Catalyst. If you are early " \
                    "in the game, you should only be farming for heroes that you actively use. In most cases, this " \
                    "will be <:Hero_eleanor:703019878453346374>.\n\n" \
                    "You can also spend your Keys on the weekly deals. You can spend as many Keys as you are " \
                    "comfortable with on <:Resource_crate:1167984753513873428> and <:Resource_ticket:1137471573113176154>.\n" \
                    "Most people stop buying these deals once they cost 10/50k keys each."

medals_title = "How to get Guild Medals?"
medals_description = "You can claim one every day by checking in, in your guild - Unlocks at Day 80.\n" \
                     "With Guild Medals, you can buy many things. The most valuable resource in the guild store are scrolls.\n" \
                     "Scrolls are used for rerolling sub stats on your gear (<#1063909425624125501>)\n" \
                     "Early, it is completely fine to buy couple Catalysts for Heroes that you actively use."

hearts_title1 = "How to get Hearts?"
hearts_description1 = "Hearts can be obtained from from Social -> Friends.\n" \
                     "In the beginning of the game, you will be able to add 5 players. Do that as soon as you can, " \
                     "so you can start gathering hearts! You can have a maximum of 30 friends. Each upgrade gives you " \
                     "5 additional slots and costs 50 rubies.\n If your friend isn't active for 30 or more days, " \
                     "you won't get any Hearts from them anymore. To easily check who is active, you can sort your " \
                     "friend list by activity."
hearts_title2 = "What should I buy with them?"
hearts_description2 = "There are weekly deals which should be purchased whenever you can. You have a whole week to " \
                      "obtain then so there is plenty of time.\n" \
                      "Do not buy tickets with Hearts! It's not worth it early in the game, the ratio is changing with " \
                      "your max day. \n" \
                      "Prioritise evolutions first, once all evolutions have been purchased then save them up for " \
                      "tickets, even then, only spend on tickets if you can't get your desired ascension in time."

evolutions_title = "What are Hero Evolutions?"
evolutions_description = "Hero Evolutions can be bought for 300 Hearts <:Resource_heart:896833387787083837> + Hero " \
                         "needs to meet the correct ascension. You should buy the Evolutions in this order - <:Hero_sa" \
                         "ul:977594194988236861> > <:Hero_soulbringer_hank:1070462845218738236> > <:Hero_siegfried:1122" \
                         "901975269376050> > <:Hero_cherryblossom:931654404074008616> > <:Hero_auto_kek:1019254136086204477>.\n" \
                         "After day 1000, every 4000 days will give an additional +1 to the Hero Ticket purchase. " \
                         "For example, at day 5000, you will be able to gain 2 hero Tickets for 5 Hearts."
rubies_title1 = "How to get Rubies?"
rubies_description1 = "You can get Rubies from Achievements, watching ads, Daily quests, Referrals, using Gold " \
                     "Spin/selling a weapon and by buying them for real money.  You can get a minimum of 45 Rubies per " \
                     "day.  (15 from watching the Ads and 30 from daily quests)."
rubies_title2 = "What should I buy with them?"
rubies_description2 = "You should start with buying all of the Hero slots. After that, you should buy all of the Elixir" \
                      " Walls, starting with the 1000 Ruby ones. After you discover all 28 skills, you will be able to " \
                      "start discovering Awakenings. Rerolling bad awakenings will cost 200 Rubies and Recalling a " \
                      "discovered Awakening will cost 250 Rubies.\n" \
                      "- Rerolling -> When you get to choose an Awakening every 365 days, thats when you can Reroll.\n" \
                      "- Recalling -> When you already picked an Awakening but you want to Recall it. " \
                      "Its always good to have a good amount (200-400) of Rubies saved for rerolling."

using_rubies_title = "I got all Hero slots and the Elixir walls, what should I buy now?"
using_rubies_description1 = "Buying all the Friend slots so you can speed up the Heart <:Resource_heart:896833387787083837> gain.\n" \
                           "Once you get past day 3000, buy the Gold walls; they are relatively cheap and useful.\n" \
                           "As a short example, at day 5000 you will unlock <#1055150620044177499>, where you can buy " \
                           "some capacity for both the Elixir Generator and the Ticket Usher or finishing the timer when forging a rune.\n"

using_rubies_description2 = "- Elixir Generator - increase the amount by 1 hours for every 400 rubies <:Resource_ruby:1038573545518813245>\n" \
                           "- Ticket Usher - increase the amount by 4 hours for every 200 rubies <:Resource_ruby:1038573545518813245>\n" \
                           "- Forger - When your Rune reached 75% completion, you can spend rubies " \
                           "<:Resource_ruby:1038573545518813245> to skip the remaining progress, the cost of skipping " \
                           "is 1 ruby <:Resource_ruby:1038573545518813245>  per 10 minutes.\n" \
                           "Upgrading both Elixir Generator and Ticket Usher enough that you don't let it idle at full " \
                           "capacity. So that you can sleep a full night without missing out on elixir or tickets." \
                           "In conclusion, be careful with your rubies!"

bones_title1 = "Where should I farm Bones?"
bones_description1 = "You should farm Bones at the highest difficulty where you can kill mobs for at least 1 minute. " \
                     "Time to unlock each difficulty: For Normal you need to reach 5:00 on Easy For Hard it's 5:00 on " \
                     "Normal And to unlock Hell you need to survive 4:00 on Hard The Bone drop is RNG, but higher you " \
                     "get better the odds."
bones_title2 = "How should I farm Bones?"
bones_description2 = "For that part, you need to experiment yourself. You can either try your regular pushing team, " \
                     "Galatine stall team, full DPS team, pushing team + Cain.\n" \
                     "Find the best team that gives the most Bones per Minute. Team can change after every push."
bones_title3 = "What should I buy with Bones?"
bones_description3 = "Caladbolg is one of the early weapons that you should consider buying. \n" \
                     "It costs only 200 Bones so buying it every 200 days should not be a problem, it is worth buying " \
                     "until you reach day 1500. You also got a week to buy all Hero Tickets, Rubies and Weapon Crates, " \
                     "buy everything, it's worth it."


class Resources(commands.GroupCog, name="resources"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="tickets", description="Provides information about Tickets")
    async def tickets(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=tickets_title, value=tickets_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="summon", description="Provides information about Summons and Mass Summon")
    async def summon(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=summon_title, value=summon_description, inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1102311924735168517/1168915209549783100/image.png")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="using_tickets", description="Provides information about correctly using Tickets")
    async def using_tickets(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=using_tickets_title, value=using_tickets_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="keys", description="Provides information about Keys")
    async def keys(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=keys_title1, value=keys_description1, inline=False)
        embed.add_field(name=keys_title2, value=keys_description2, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="using_keys", description="Provides information about correctly using Keys")
    async def using_keys(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=using_keys_title, value=using_keys_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="medals", description="Provides information about Guild Medals")
    async def medals(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=medals_title, value=medals_description, inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1102311924735168517/1168919238480777316/image.png")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="hearts", description="Provides information about Hearts (Amity)")
    async def hearts(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=hearts_title1, value=hearts_description1, inline=False)
        embed.add_field(name=hearts_title2, value=hearts_description2, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="evolutions", description="Provides information about Hero Evolutions")
    async def evolutions(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=evolutions_title, value=evolutions_description, inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1102311924735168517/1168922000413184043/image.png")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rubies", description="Provides information about Rubies")
    async def rubies(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=rubies_title1, value=rubies_description1, inline=False)
        embed.add_field(name=rubies_title2, value=rubies_description2, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="using_rubies", description="Provides information about correctly using Rubies")
    async def using_rubies(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=using_rubies_title, value=using_rubies_description1, inline=False)
        embed.add_field(name="", value=using_rubies_description2, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="bones", description="Provides information about Bones (Fossils)")
    async def bones(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=bones_title1, value=bones_description1, inline=False)
        embed.add_field(name=bones_title2, value=bones_description2, inline=False)
        embed.add_field(name=bones_title3, value=bones_description3, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Resources(bot))