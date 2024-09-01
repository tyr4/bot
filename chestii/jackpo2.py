import discord
from random import randint
from discord.ext import commands
from discord import app_commands

import asyncio
import json

letters = ['j', 'a', 'c', 'k', 'p', 'o', 't']
funni_list = []
leaderboard_spots = [":first_place:", ":second_place:", ":third_place:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:"]
has_talked = []

async def cd(user):
    global funni_list
    if user not in funni_list:
        funni_list.append(user)

        for i in range(0, 2):
            await asyncio.sleep(1)

        funni_list.remove(user)


def leaderboard(user: int):
    with open('jackpo.json', 'r') as json_file:
        data = json.load(json_file)
        embed = discord.Embed(title=f"Jackpo Leaderboard <a:kafkakurukuru:1118233531110412461>", color=0x71368a)
        embed.add_field(name="__Jackpo chances__", value=f"On any message, you have:\nAny letter of JACKPOT - 1/1000 Chance\n"
                                                       f"JACKPO - 1/100000 Chance\n", inline=False)
        idk = ""
        sorted_data = sorted(data.items(), key=lambda x: x[1]['sum'], reverse=True)
        for i, (key, value) in enumerate(sorted_data):
            spot = f"#{i + 1}" if i >= 10 else leaderboard_spots[i]
            letters = f"x{value['j']} **J** / x{value['a']} **A** / x{value['c']} **C** / x{value['k']} **K** / x{value['p']} **P** / x{value['o']} **O** / x{value['t']} **T**"
            if key == str(user):
                ceva = f"{spot} <@{key}> ({value['name']}) - {letters}"
                if i >= 10:
                    break
            if i < 10 and value['sum'] != 0:
                idk += f"{spot} <@{key}> ({value['name']}) - {letters}\n"
        embed.add_field(name="**TOP 10**", value=idk, inline=False)
        if ceva:
            embed.add_field(name="You", value=ceva, inline=False)
        else:
            embed.add_field(name="You", value="Nothing here :(", inline=False)
        embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                         icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
        # print(idk)
        # print(ceva)
        return embed


# def trade(id1, id2, letter1, letter2):
#     with open('jackpo.json', 'r+') as json_file:
#         data = json.load(json_file)
#         if id1 in data and id2 in data:
#             if data[id1][letter1] != 0 and data[id2][letter2] != 0:
#                 if data[id1]['trade_state'] is True and data[id2]['trade_state'] is True:
#                     data[id1]['trade_state'] = True
#                     data[id2]['trade_state'] = True
#
#
#                 else:
#                     return 0


def update(user_id: str, name, letter, mode):
    with open('jackpo.json', 'r+') as json_file:
        data = json.load(json_file)
        if user_id not in data:
            data[user_id] = {"name": name, "trade_state": False, "j": 0, "a": 0, "c": 0, "k": 0, "p": 0, "o": 0, "t": 0, "sum": 0}

        if mode == 1:
            data[user_id][letter] += 1
            data[user_id]['sum'] += 1

        elif mode == 2:
            data[user_id]['j'] += 1
            data[user_id]['a'] += 1
            data[user_id]['c'] += 1
            data[user_id]['k'] += 1
            data[user_id]['p'] += 1
            data[user_id]['o'] += 1
            data[user_id]['sum'] += 6

        elif mode == 3:
            #trade
            pass

        json_file.seek(0)
        json.dump(data, json_file, indent=4)


class Jackpo(commands.GroupCog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_message(self, message):
        global funni_list
        global has_talked
        letter_chance = randint(1, 1_000)
        jackpo_chance = randint(1, 100_000)

        if message.author == self.bot.user:
            return

        has_talked.append(message.author.id)
        if has_talked[-1] != has_talked[0]:
            has_talked = []
        if len(has_talked) >= 3 and has_talked[0] == has_talked[1] == has_talked[2]:
            letter_chance = 0
            jackpo_chance = 0

        print(has_talked)
        # if message.author.id not in funni_list:
        #     funni_list.append(message.author.id)
        #     await asyncio.sleep(5)
        #     funni_list.remove(message.author.id)

        if letter_chance == 1_000:
            letter_won = letters[randint(0, len(letters) - 1)]
            if len(str(message.content)) < 5:
                await message.reply(f'You would\'ve won the letter **{letter_won.upper()}**, but your message was below 5 letters!', mention_author=True)
            elif message.author.id in funni_list:
                await message.reply(f'You would\'ve won the letter **{letter_won.upper()}**, but you were still in cooldown!', mention_author=True)
            else:
                await message.reply(f'WE HAVE A WINNER!!!!!\n'
                                    f'You won the letter **{letter_won.upper()}**!\nCongrats my friend {message.author.display_name}! <:pepeflower:901873383212462091>', mention_author=True)
                update(str(message.author.id), str(message.author), letter_won, 1)

        if jackpo_chance == 100_000:
            if len(str(message.content)) < 5:
                await message.reply(f'You would\'ve won the **JACKPO**, but your message was below 5 letters!', mention_author=True)
            elif message.author.id in funni_list:
                await message.reply(f'You would\'ve won the **JACKPO**, but you were still in cooldown!', mention_author=True)
            else:
                await message.reply(f'WE HAVE A JACKPO WINNER!!!!!!!!!!!!!!!!\n'
                                    f'{message.author.display_name} WON JACKPO!!!!!!!!!!!!!!\nCONGRATS {message.author.display_name}! {"<:LETSFUCKINGGOO:901184486702710804>" * 20}', mention_author=True)
                update(str(message.author.id), str(message.author), 0, 2)

        await cd(message.author.id)

    @app_commands.command(name="leaderboard", description="Show the jackpo leaderboard or something idk")
    async def jackpo_leaderboard(self, interaction: discord.Interaction):
        embed = leaderboard(interaction.user.id)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Jackpo(bot), guild=discord.Object(id=748126143584141332))