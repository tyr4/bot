import time

import discord
from discord.ext import commands
from random import randint
import asyncio
import re
import datetime
import pytz
import json

from chestii import jail

jailtime = jail.jailtime
ceva_id = jail.ceva_id


def update(user_id: str, name, mode):
    with open('data.json', 'r+') as json_file:
        data = json.load(json_file)
        if user_id not in data:
            data[user_id] = {"kurureact1": 0, "kurureact2": 0, "kuruemote": 0, "kurugif": 0, "name": name}

        if mode == 1:
            data[user_id]['kurureact1'] += 1
        elif mode == 2:
            data[user_id]['kurureact2'] += 1
        elif mode == 3:
            data[user_id]['kuruemote'] += 1
        elif mode == 4:
            data[user_id]['kurugif'] += 1

        json_file.seek(0)
        json.dump(data, json_file, indent=4)


class Funni(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ask(self, ctx):
        if ctx.guild.id == 570929677732937738 and ctx.author.id != 556836294710525952:
            return
        idk = randint(1, 2)
        if idk == 1:
            await ctx.reply("<a:yescat:1279088548162572319>", mention_author=False)
        else:
            await ctx.reply("<a:NoNoNoNoNo:1279088570350571673>", mention_author=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        print(f"{message.author} imparte intelepciune: '{message.content}', #{message.channel}")
        masaj = re.findall(r'\w+', str(message.content.lower()))
        try:
            name = str(message.author.display_name)
        except:
            name = ""

        channel = self.bot.get_channel(1150149982385606656)
        if message.author == self.bot.user:
            return

        if message.guild.id in [570929677732937738, 993818190008287283]:
            z = randint(1, 1000)
            zplus = randint(1, 10000)
            kurukuru_jackpo = randint(1, 100000)
            if "the" in masaj and "man" in masaj and message.author.id in [556836294710525952, 278798822937853953]:
                if masaj.index("the") < masaj.index("man"):
                    await message.channel.send("Dave the man <:LETSFUCKINGGOO:901184486702710804>", reference=message,
                                               mention_author=False)

            if z == 1000 or str(message.channel) == "amogus-testing":
                await message.add_reaction("<a:kurukuru:1113242215083421707>")
                update(str(message.author.id), str(message.author), 1)
                kurukuru2 = randint(1, 5)
                if kurukuru2 == 5 or str(message.channel) == "amogus-testing":
                    await message.add_reaction("<a:kurukuru2:1139252590278889529>")
                    update(str(message.author.id), str(message.author), 2)

            if kurukuru_jackpo == 100000 or str(message.channel) == "amogus":
                await message.reply("https://tenor.com/view/kuru-kuru-gif-10882574602170874277", mention_author=False)
                update(str(message.author.id), str(message.author), 4)

            if zplus == 10000 or str(message.channel) == "amogus":
                await message.reply("<a:kurukuru:1113242215083421707>", mention_author=False)
                update(str(message.author.id), str(message.author), 3)

            if "silwuf" in message.content and "prestige" in message.content:
                await message.channel.send("You might be wondering how I got WT Prestige, huh? Here's how: || |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| ||||:||||)|||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| ||",
                                           reference=message, mention_author=False)

            if zplus == 10000 or kurukuru_jackpo == 100000 or z == 1000:
                chanel = self.bot.get_channel(1224041578407002153)
                await chanel.send(file=discord.File("data.json"))

        elif message.guild.id in [993818190008287283, 748126143584141332, 1030490217855074304]:
            global jailtime
            x = randint(1, 250)

            if message.author.id in ceva_id and jailtime is True:
                a = message.content
                if a == "":
                    a = "*some random attachment*"
                await channel.send(f"**{name} in <#{message.channel.id}>**: {a}")
                await asyncio.sleep(2)
                await message.delete()

            if "the" in masaj and "man" in masaj:
                if masaj.index("the") < masaj.index("man"):
                    await message.channel.send("Dave the man <:LETSFUCKINGGOO:901184486702710804>", reference=message,
                                               mention_author=False)
            if "becky" in masaj:
                await message.delete()

            if "esketit" in masaj:
                await message.channel.send("https://tenor.com/view/lets-lets-get-it-gif-14167426", reference=message,
                                           mention_author=False)

            if "<@1135983715646976111>" in message.content.lower():
                reply = ["https://cdn.discordapp.com/emojis/1078009688366522580.gif", "I require professional help",
                         "My mental state is declining <a:kurukuru:1113242215083421707>"]
                random_reply = randint(0, (len(reply) - 1))
                await message.channel.send(reply[random_reply], reference=message, mention_author=True)


async def setup(bot):
    await bot.add_cog(Funni(bot))
