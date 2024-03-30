import discord
from discord.ext import commands
from discord import app_commands

description = "》 Information about Runes"
info_title = "Runes"
info_description = "Runes can be bought in the Bones Shop with Bones <:Resource_bone:710610656864370728>\n" \
                   "When you buy any kind of Rune, you will be given a random type. There are currently 8 different " \
                   "types of Runes.\n" \
                   "<:Rune_CriticalDamage:1056355565523177553> CDMG - Critical Damage\n" \
                   "<:Rune_Damage:1056355597630570496> DMG - Damage \n" \
                   "<:Rune_HeroDamage:1056355549786161172> HDMG - Hero Damage \n" \
                   "<:Rune_Arcana:1056355514965053490> SDMG - Spell Damage \n" \
                   "<:Rune_CriticalChance:1056583354654396436> CC - Critical Chance\n" \
                   "<:Rune_Health:1056355533055082506> HP - Hit Points\n" \
                   "<:Rune_Mana:1056355504613490749> MP - Mana Points\n" \
                   "<:Rune_Blank:1056355490424160327> Blank - Blank Rune\n\n" \
                   "The recommended go-to Runes:\n" \
                   "Critical Damage, Damage, Hero Damage, Critical Chance and Health."

fusing_title1 = "Fusion"
fusing_description1 = "Used for upgrading the tier of your Rune. If you fuse two of the same type of runes you will " \
                     "get the same type 1 tier higher (CDMG + CDMG = CDMG).\n" \
                     "But if you pick two different types, you will get a random one (CDMG + DMG = random). " \
                     "Greater Rune T13+ can't be used for random fusing."

fusing_title2 = "Fusing and Dust"
fusing_description2 = "Fusing 2x Lesser Rune T1 now fuses into Rune T1.\n" \
                      "2x Rune T1 fuses into Greater Rune T1.\n" \
                      "If you only have Greater Runes T1 in the shop (before Fusing TX), focus on getting 2 types of " \
                      "Runes up to the next tier at the same time and sell the rest. " \
                      "After unlocking Greater Runes T2, focus on 4 different sets of Runes at the same time and sell" \
                      " the rest. \nUsing T3/T4 Greater Runes for Fusing isnt worth the bone cost. Blank Runes sell " \
                      "for more Dust than other Runes of the same tier. It's not worth to use them for fusing, always " \
                      "sell them. If you find yourself running out of Dust while Fusing, it's ok to sell an entire" \
                      " batch of any tier just to have some spare Fusing Dust on the side."

fusing_efficiently_title = "Fusing efficiently"
fusing_efficiently_description = "For Greater Runes T1 to Fuse Runes efficiently, buy a bunch of them, keep the two " \
                                 "types that you are currently focusing and sell the rest. When they go up a tier, " \
                                 "move to the next two different types.\n"
fusing_efficiently_title2 = "QoL Feature"

higher_tiers_title = "Unlocking higher tiers of Greater Runes in the Bone Shop"
higher_tiers_description = "You will be able to unlock higher tier Runes in the Shop by first fusing a specific Rune tier.\n" \
                           "To unlock Greater Rune T2 in the shop, you need to fuse a T10 Rune.\n" \
                           "For Greater Rune T3, you need to fuse a T11 Rune and for T4, you need to fuse a T12 Rune."

unleash_title1 = "Unleash"
unleash_description1 = "The Unleash tab is unlocked when you reach Tier X Greater Rune, but its usable when you get a " \
                      "Tier XI Greater Rune.\n" \
                      "All tiers after X are unleashable up to V7. (You can find more about that in <#1123984392046518272>).\n" \
                      "You will never lose the Unleash power by fusing it with non unleashed Rune. \n" \
                      "Keep in mind that only Runes with some sort of damage can be unleashed!"

unleash_title2 = "How many days is an Unleash worth?"
unleash_description2 = "Every Unleash is worth 146.2 days."

unleash_title3 = "When should I unleash?"
unleash_description3 = "If the amount of rewinds needed for the Unleash exceeds the amount of rewinds needed to get 146 " \
                       "days of pushing power with skills, it's usually not time to Unleash yet."

cloning_title = "Cloning"
cloning_description = "The Cloning tab is unlocked when you reach Tier XII Greater Rune, but you will be able to clone " \
                      "a Tier XIII Greater rune and higher.\n" \
                      "Cloning is the fastest way to get higher Tier Runes. It costs more bones than fusing the rune " \
                      "normally (around 5% more), but it is well worth it, since you save precious time."
cloning_description2 = "**Clone Costs per Tier**\n" \
                       "```>  V6:    -> 7.43b\n"\
                       ">  V5:    -> 3.71b\n" \
                       ">  V4:    -> 1.86b\n" \
                       ">  V3:    -> 928.74m\n" \
                       ">  V2:    -> 464.37m\n" \
                       ">  V1:    -> 232.18m\n" \
                       ">  XX:    -> 116.09m\n" \
                       ">  XIX:   -> 58.04m\n" \
                       ">  XVIII: -> 29.02m\n" \
                       ">  XVII:  -> 14.51m\n" \
                       ">  XVI:   -> 7.25m\n" \
                       ">  XV:    -> 3.63m\n" \
                       ">  XIV:   -> 1.81m\n" \
                       ">  XIII:  -> 905.77k\n```"


class Runes(commands.GroupCog, name="runes"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="info", description="Provides general information about Runes")
    async def runes_info(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=info_title, value=info_description, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="fusing", description="Provides information about fusing Runes")
    async def fusing(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=fusing_title1, value=fusing_description1, inline=False)
        embed.add_field(name=fusing_title2, value=fusing_description2, inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1102311924735168517/1170007138039517192/image.png")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="fusing_efficiently", description="Provides information about efficiently"
                                                                 " fusing Runes")
    async def fusing_efficiently(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=fusing_efficiently_title, value=fusing_efficiently_description, inline=False)
        embed.add_field(name=fusing_efficiently_title2, value='', inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1102311924735168517/1170007138303754360/image.png")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unleash", description="Provides information about unleashing Runes")
    async def unleash(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=unleash_title1, value=unleash_description1, inline=False)
        embed.add_field(name=unleash_title2, value=unleash_description2, inline=False)
        embed.add_field(name=unleash_title3, value=unleash_description3, inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1102311924735168517/1170007464880656384/image.png")
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="cloning", description="Provides information about cloning Runes")
    async def cloning(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=description, color=0x71368a)
        embed.add_field(name=cloning_title, value=cloning_description, inline=False)
        embed.add_field(name='', value=cloning_description2, inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Runes(bot))
