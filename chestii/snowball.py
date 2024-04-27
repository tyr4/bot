import discord
from discord import app_commands
from discord.ext import commands
from random import randint
import asyncio
import json
import time
import datetime
from discord.ext.commands import cooldown, BucketType

lista = []
leaderboard_spots = [":first_place:", ":second_place:", ":third_place:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:"]


def convert_to_unix_time(date: datetime.datetime, days: int, hours: int, minutes: int, seconds: int) -> str:
    # Get the end date
    end_date = date + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

    # Get a tuple of the date attributes
    date_tuple = (end_date.year, end_date.month, end_date.day, end_date.hour, end_date.minute, end_date.second)

    # Convert to unix time
    return f'<t:{int(time.mktime(datetime.datetime(*date_tuple).timetuple()))}:R>'


async def cd(user_id, snowballed_id, result):
    with open('cd.json', 'r+') as json_file:
        data = json.load(json_file)
        if str(user_id) not in data or str(snowballed_id) not in data:
            data[str(user_id)] = {"cd": 0, "timestamp": ""}
            data[str(snowballed_id)] = {"cd": 0, "timestamp": ""}

        data[str(user_id)]["cd"] = 1
        data[str(user_id)]["timestamp"] = convert_to_unix_time(datetime.datetime.now(), 0, 0, 1, 0)

        json_file.seek(0)
        json.dump(data, json_file, indent=4)
        if result == 1:
            data[str(snowballed_id)]["cd"] = 2
            data[str(snowballed_id)]["timestamp"] = convert_to_unix_time(datetime.datetime.now(), 0, 0, 0, 20)
            print("inainte de update")
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            print("dupa de update (romana 100)")
            await asyncio.sleep(20)
            data[str(snowballed_id)]["cd"] = 0
            data[str(snowballed_id)]["timestamp"] = ""

            json_file.seek(0)
            json.dump(data, json_file, indent=4)

        await asyncio.sleep(40 if result == 1 else 60)
        data[str(user_id)]["cd"] = 0
        data[str(user_id)]["timestamp"] = ""

        json_file.seek(0)
        json.dump(data, json_file, indent=4)


def update(user_id, name, result):
    with open('snowbol.json', 'r+') as json_file:
        data = json.load(json_file)
        if str(user_id) not in data:
            data[str(user_id)] = {"won": 0, "lost": 0, "name": name}
        if result == 1:
            data[str(user_id)]["won"] += 1
        elif result == 2:
            data[str(user_id)]["lost"] += 1

        json_file.seek(0)
        json.dump(data, json_file, indent=4)

        return data[str(user_id)]["won"], data[str(user_id)]["lost"]


class Snowball(commands.GroupCog, name="snowball"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="hit", description="Hit someone idk")
    @app_commands.describe(user="The snowballed")
    @app_commands.checks.cooldown(1, 60, key=lambda i: (i.guild_id, i.user.id))
    async def hit(self, interaction: discord.Interaction, user: discord.User) -> None:

        if user.id == interaction.user.id:
            embed = discord.Embed(title=f"Snowball haha idk", color=0x1abc9c)
            embed.add_field(name="Are you dumb?", value=f"Hmm imo yes you deserve the 60s cooldown now", inline=False)
            embed.set_footer(text="Ahmet was here",
                             icon_url="https://cdn.discordapp.com/emojis/1106570654544830474.png")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            result = randint(1, 2)
            embed = discord.Embed(title=f"{'Your throw was disappointing...' if result == 2 else 'Good throw!'}", color=0x1abc9c)
            won, lost = update(interaction.user.id, interaction.user.name, result)

            embed.add_field(name=f"", value=f"**{interaction.user.display_name}'s** attempt at "
                           f"snowballing **{user.display_name}** "
                           f"__{'succeeded__! <a:mashpapartier:1141451859878494208>' if result == 1 else 'failed__! <:peperose:911014215639240764>'}\n\n"
                           f"You now have **{won} wins** and **{lost} losses**!", inline=False)
            embed.set_footer(text="the snowballmaster69 is snowballing ඞ",
                             icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
            await interaction.response.send_message(embed=embed)

            if result == 1 and user.id not in lista:
                lista.append(user.id)
                await asyncio.sleep(20)
                lista.remove(user.id)

    @hit.error
    async def hit_error(self, interaction: discord.Interaction, error):
        embed = discord.Embed(title="Snowball haha idk", color=0x1abc9c)
        embed.add_field(name="", value=f"Wait **{error.retry_after:.2f}s** idiot", inline=False)
        embed.set_footer(text="Haha I mean be patient",
                         icon_url="https://cdn.discordapp.com/emojis/901873383212462091.png")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="leaderboard", description="Snowball leaderboard idk")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        idk = ""
        with open('snowbol.json', 'r') as json_file:
            data = json.load(json_file)
            embed = discord.Embed(title=f"Snowbol Leaderboard <a:silwufkurukuru:1147620600584613928>", color=0x1abc9c)
            sorted_data = sorted(data.items(), key=lambda x: x[1]["won"], reverse=True)
            for i, (key, value) in enumerate(sorted_data):
                spot = f"#{i + 1}" if i >= 10 else leaderboard_spots[i]
                if key == str(interaction.user.id):
                    ceva = f"{spot} <@{key}> (`{value['name']}`) - {value['won']}/{value['lost']}" \
                           f" ({format((value['won'] / (value['won'] + value['lost'])) * 100, '.2f')}%) W/L"
                    if i >= 10:
                        break
                if i < 10 and value["won"] != 0:
                    idk += f"{spot} <@{key}> (`{value['name']}`) - {value['won']}/{value['lost']}" \
                           f" ({format((value['won'] / (value['won'] + value['lost'])) * 100, '.2f')}%) W/L\n"
            embed.add_field(name="**TOP 10**", value=idk, inline=False)
            if ceva:
                embed.add_field(name="You", value=ceva, inline=False)
            else:
                embed.add_field(name="You", value="Nothing here :(", inline=False)
            embed.set_footer(text="the snowballmaster69 is snowballing ඞ",
                             icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")
            await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Snowball(bot), guild=discord.Object(id=993818190008287283))
