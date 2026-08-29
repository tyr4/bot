import pathlib

import discord
from discord.ext import commands, tasks
from random import randint
import asyncio
import re
import datetime
import json

from chestii.wrapped import update_wrapped_data
from chestii.sheet import get_event_week_data
from chestii.void_deals import build_embed_today_deals

log_ok = 0
kuru_lock = asyncio.Lock()

with open('raids_list.json', 'r+') as json_file:
    raids_list = json.load(json_file)

with open('update_list.json', 'r+') as json_file:
    update_list = json.load(json_file)

async def update_update_list(user_id: int, update_list):
    with open('update_list.json', 'r+') as json_file:
        data = json.load(json_file)
        data['list'] = update_list['list']
        json_file.seek(0)
        json.dump(data, json_file, indent=4)


async def update_raids_list(user_id: int, raids_list):
    with open('raids_list.json', 'r+') as json_file:
        data = json.load(json_file)
        data['list'] = raids_list['list']
        json_file.seek(0)
        json.dump(data, json_file, indent=4)


def rateup_embed():
    # NU SETA ASTA IN ACEEASI SAPTAMANA CA ZIUA DE AZI
    start_date = datetime.datetime(2025, 12, 15, 12, 0, tzinfo=datetime.timezone.utc)
    end_date = datetime.datetime(2100, 12, 31, 12, 0, tzinfo=datetime.timezone.utc)

    normal_rateup_emotes = [
        "<:Hero_Nero:1216982822665977946>",
        "<:Hero_Merlin:703020597755510824>",
        "<:Hero_Lilith:1487965100043403374>",
        "<:Hero_Dewitt:703020422005915658>",
        "<:Hero_Dash:703020475647000708>",
        "<:Hero_DarkMerlin:703020537089097789>",
        "<:Hero_Cain:711652423172882442>",
        "<:Hero_Elden:703020676323475536>",
        "<:Hero_KingArthur:1470568923073351914>",
        "<:Hero_Luna:703033646172602508>",
        "<:Hero_Mikhail:703033570402238495>",
        "<:Hero_Lilibeth:1487965050680512562>",
        "<:Hero_Clarissa:1487965135858569256>",
        "<:Hero_Roland:742795363739762778>"
    ]
    normal_rateup_names = ['Nero', 'Merlin', 'Lilith', 'Dewitt', 'Dash', 'Dark Merlin', 'Cain', 'Elden', 'King Arthur',
                           'Luna', 'Mikhail', 'Lilibeth', 'Clarissa', 'Roland']

    fates_rateup_emotes = [
        "<:Hero_Joan:1247636855877406771>",
        "<:Hero_Iseria:1247636854816243822>",
        "<:Hero_Zeus:1247637113521049630>",
        "<:Hero_Boreas:1452633290019442863>"
    ]
    fates_rateup_names = ['Joan of Arc', 'Iseria', 'Zeus', 'Boreas']

    dark_rateup_emotes = [
        "<:Hero_Abel:1205212780769185792>",
        "<:Hero_Bellona:1367087087609839677>",
        "<:Hero_DaryonDevilkin:1487823751423725721>"
    ]
    dark_rateup_names = ["Abel", "Bellona", "Daryon Devilkin"]

    zile_luni, curr_rateup = [], 0
    # DOAR ASTEA 3 CONTEAZA, NU CORESPUND CU INDICII DIN LISTE (DECAT CU -2 SAU CEVA)
    curr_normal_rateup = 7
    curr_clairvoyance_rateup = 0
    curr_fates_rateup = 3
    curr_dark_rateup = 0

    # ASTEA NU CONTEAZA
    next_normal_rateup = 0
    next_clairvoyance_rateup = 0
    next_fates_rateup = 0

    while start_date <= end_date:
        if start_date.weekday() == 0:
            curr_normal_rateup = (curr_normal_rateup + 1) % len(normal_rateup_emotes)
            curr_clairvoyance_rateup = (curr_clairvoyance_rateup + 1) % len(normal_rateup_emotes)
            curr_fates_rateup = (curr_fates_rateup + 1) % len(fates_rateup_emotes)
            curr_dark_rateup = (curr_dark_rateup + 1) % len(dark_rateup_emotes)
            
            temp = [start_date, curr_normal_rateup, curr_clairvoyance_rateup, curr_fates_rateup, curr_dark_rateup]
            zile_luni.append(temp)
        start_date += datetime.timedelta(days=1)

    # NU ATINGE
    next_rateup = datetime.datetime.now(tz=datetime.timezone.utc)
    for monday in zile_luni:
        if next_rateup > monday[0]:
            # curr_rateup = monday[0]
            curr_normal_rateup = monday[1]
            curr_clairvoyance_rateup = monday[2]
            curr_fates_rateup = monday[3]
            curr_dark_rateup = monday[4]
        else:
            next_rateup = monday[0].timestamp()
            next_normal_rateup = monday[1]
            next_clairvoyance_rateup = monday[2]
            next_fates_rateup = monday[3]
            next_dark_rateup = monday[4]
            break
    
    
    embed = discord.Embed(title='Hero Rate-up Rotation', color=0x71368a)
    embed.add_field(name='Tickets Rate-up',
                    value=f'{normal_rateup_emotes[curr_normal_rateup]} {normal_rateup_names[curr_normal_rateup]}'
                          f' (next {normal_rateup_emotes[next_normal_rateup]} {normal_rateup_names[next_normal_rateup]})',
                    inline=False)

    embed.add_field(name='Fates/Totem of Clairvoyance Rate-ups',
                    value=f'{fates_rateup_emotes[curr_fates_rateup]} {fates_rateup_names[curr_fates_rateup]}'
                          f' (next {fates_rateup_emotes[next_fates_rateup]} {fates_rateup_names[next_fates_rateup]})\n'
                          f'{normal_rateup_emotes[curr_clairvoyance_rateup]} {normal_rateup_names[curr_clairvoyance_rateup]}'
                          f' (next {normal_rateup_emotes[next_clairvoyance_rateup]} {normal_rateup_names[next_clairvoyance_rateup]})',
                    inline=False)

    embed.add_field(name='Dark Rate-up',
                value=f'{dark_rateup_emotes[curr_dark_rateup]} {dark_rateup_names[curr_dark_rateup]}'
                        f' (next {dark_rateup_emotes[next_dark_rateup]} {dark_rateup_names[next_dark_rateup]})',
                inline=False)

    embed.add_field(name='', value=f'Next rate-up is <t:{next_rateup:.0f}:R>', inline=False)

    embed.set_image(
        url='https://media.discordapp.net/attachments/1141499425722740756/1488176510618702074/image.png?ex=69cbd3e1&is=69ca8261&hm=db600143eb390d80a41dae252158b4980b0540d36b6ccb9466fbd4c4851c8fe1&=&quality=lossless')

    print("embed fraere")
    return embed


# def init_sheet():
#     # Path to your service account key file
#     SERVICE_ACCOUNT_FILE = 'google_sheets_api_key.json'
#
#     # Define the scope
#     SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
#
#     # Authenticate using the service account key
#     creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#
#     # Use gspread to access the Google Sheets API
#     gc = gspread.authorize(creds)
#
#     # Open the Google Sheet by its title or URL
#     sheet = gc.open_by_key("1cq3kCdWNpyiOA_XKiUPi62XyspexsgyIP48yMkGmEqM")
#     worksheet = sheet.worksheet('Sheet1')
#
#     return sheet, worksheet


def filter_application_text(text_input):
    text_input = text_input.replace("**", "")
    text_input = text_input.split("\n")

    for i in range(0, len(text_input)):
        index = text_input[i].find(":")
        text_input[i] = text_input[i][(index + 1 if index != -1 else 0):].lstrip()

    return text_input

def load_kuru_data():
    kuru_data = {}

    with open('data.json', 'r') as json_file:
        kuru_data = json.load(json_file)

    return kuru_data

def save_kuru_data(kuru_data):
    path = pathlib.Path("data.json")
    tmp = path.with_suffix(".tmp")

    with tmp.open("w") as f:
        f.seek(0)
        json.dump(kuru_data, f, indent=4)

    tmp.replace(path)

async def update(user_id: str, name, mode):
    async with kuru_lock:
        data = load_kuru_data()

        if user_id not in data:
            data[user_id] = {"kurureact1": 0, "kurureact2": 0, "kuruemote": 0, "kurugif": 0, "dancyreply": 0, "dancygif": 0, "dancyspam": 0, "dancybread": 0, "name": name}
        
        if "dancyreply" not in data[user_id]:
                data[user_id]['dancyreply'] = 0
        
        if "dancygif" not in data[user_id]:
                data[user_id]['dancygif'] = 0

        if "dancyspam" not in data[user_id]:
                data[user_id]['dancyspam'] = 0

        if "dancybread" not in data[user_id]:
                data[user_id]['dancybread'] = 0

        if mode == 1:
            data[user_id]['kurureact1'] += 1
        elif mode == 2:
            data[user_id]['kurureact2'] += 1
        elif mode == 3:
            data[user_id]['kuruemote'] += 1
        elif mode == 4:
            data[user_id]['kurugif'] += 1

        elif mode == 5:
            data[user_id]['dancyreply'] += 1
        elif mode == 6:
            data[user_id]['dancygif'] += 1
        elif mode == 7:
            data[user_id]['dancyspam'] += 1
        elif mode == 8:
            data[user_id]['dancybread'] += 1

        data[user_id]["name"] = name
        
        save_kuru_data(data)


embed_message_general = None
general_channel = None
help_channel = None
embed_message_help = None

class Funni(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_embed.start()

    @commands.command()
    # @commands.has_permissions(manage_messages=True)
    async def embed(self, ctx, *, args):
        if ctx.author.id == 556836294710525952:
            embed = discord.Embed(title='hello zero', color=0x71368a)
            embed.add_field(name='', value=args, inline=False)

            await ctx.channel.send(embed=embed)

    @tasks.loop(seconds=60)
    async def check_embed(self):
        global log_ok
        global general_channel
        global embed_message_general
        global embed_message_help
        global help_channel

        embed = rateup_embed()
        await embed_message_general.edit(embed=embed)
        await embed_message_help.edit(embed=embed)

        # log_channel = self.bot.get_channel(1319074955492589649)
        # if not log_ok and datetime.datetime.now(tz=pytz.utc).hour == 14:
        #     log_ok = 1
        #     async for message in log_channel.history(limit=None):
        #         await message.delete()
        #         await asyncio.sleep(1)

    @check_embed.before_loop
    async def before_check_embed(self):
        global general_channel
        global embed_message_general
        global embed_message_help
        global help_channel

        print("se asteapta")
        await self.bot.wait_until_ready()
        general_channel = await self.bot.fetch_channel(570929677732937740)
        help_channel = await self.bot.fetch_channel(696035168414072913)

        embed_message_general = await general_channel.fetch_message(1369768813272371210)
        embed_message_help = await help_channel.fetch_message(1453161876375601196)

    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def angel(self, ctx, *, arg):
    #     print(arg)
    #     channel = self.bot.get_channel(1240742251420712990)
    #     if ctx.author.id != 839495136500514886:
    #         await channel.send(f"**{ctx.author}** ({ctx.author.id}): **{arg}**")
    #         await ctx.channel.send(arg)

    #     await ctx.message.delete()

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if "whar" in message_after.content.lower() or "whatr" in message_after.content.lower():
            await message_after.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id == 570929677732937738:
            guild = await self.bot.fetch_guild(payload.guild_id)
            channel = await guild.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)

            hasCrocodile, hasSaxophone = False, False
            hasEagle, hasAmerica = False, False

            for reaction in message.reactions:
                emoji = str(reaction.emoji)        # str or Emoji
                count = reaction.count
                me = reaction.me              # did the bot react?

                if "🐊" in emoji or "crocodile" in emoji:
                    hasCrocodile = True
                
                if "🎷" in emoji or "saxophone" in emoji:
                    hasSaxophone = True

                if "🦅" in emoji:
                    hasEagle = True
                
                if "🇺🇸" in emoji:
                    hasAmerica = True

                print(f"Emoji: {emoji} | Count: {count} | Bot reacted: {me}")
            
            if hasCrocodile and hasSaxophone:
                print(payload.user_id)
                user = await self.bot.fetch_user(payload.user_id)
                await user.send("🇫🇷")
                print(f"sent french to {user.display_name}")
            
            if hasAmerica and hasEagle:
                user = await self.bot.fetch_user(payload.user_id)
                await user.send("🍔")

        if payload.guild_id == 570929677732937738 and payload.user_id in [1174101270471114864, 685600652633964603,
                                                                          1381989758418419805]:
            await asyncio.sleep(5)
            user, user_id = payload.member.name, payload.user_id
            channel = self.bot.get_channel(payload.channel_id)
            log_channel = self.bot.get_channel(1352323971860795393)
            message = await channel.fetch_message(payload.message_id)

            string = (f'# {user} {user_id} #{channel.name}\n'
                      f'**Reacted "{payload.emoji.name}" to the message:** \n"`{message.content}`"')
            # if payload.emoji.name.lower() in emoji_list:
            #     string += " <@556836294710525952>"

            string += '\n~~                                        ~~'

            await log_channel.send(string)
            await asyncio.sleep(5)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kuro(self, ctx, *, arg):
        user = self.bot.get_user(556836294710525952)
        await user.send(arg)
        print('am primit')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def gala(self, ctx):
        user = await self.bot.fetch_user(313692765429170177)
        dm = await user.create_dm()

        async for message in dm.history(limit=9999):
            print(
                message.author.id,
                message.content,
                message.created_at
            )
            if message.attachments:
                for attachment in message.attachments:
                    print(attachment.url)

    @commands.command()
    async def ask(self, ctx):
        # if ctx.guild.id == 570929677732937738 and ctx.author.id != 556836294710525952:
        # return
        try:
            if ctx.guild.id == 570929677732937738 and ctx.author.id != 556836294710525952:
                return
            idk = randint(1, 2)
            if idk == 1:
                await ctx.reply("<a:yescat:1422854452947189811>", mention_author=False)
            else:
                await ctx.reply("<a:NoNoNoNoNoNo:1422854397066608672>", mention_author=False)
        except:
            idk = randint(1, 2)
            if idk == 1:
                await ctx.reply("<a:yescat:1279088548162572319>", mention_author=False)
            else:
                await ctx.reply("<a:NoNoNoNoNo:1279088570350571673>", mention_author=False)

    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def alpha_history(self, ctx, channel_id):
    #     data = datetime.datetime(2025, 8, 20, tzinfo=pytz.utc)
    #     channel = self.bot.get_channel(int(channel_id))
    #     counter = 0
    #     start = time.time()
    #     matrix = []
    #
    #     async for message in channel.history(limit=None, after=data):
    #         if message.author.id == 151495292418654210:
    #             continue
    #
    #         counter += 1
    #         filtered_text = [message.author.display_name, message.author.name, message.created_at.strftime("%Y-%m-%d %H:%M:%S"), str(message.author.id), str(message.content)]
    #         matrix.append(filtered_text)
    #         print(filtered_text)
    #
    #     dump_all_info_alpha_sheet(matrix)
    #
    #     end = time.time()
    #     await ctx.reply(f"{counter} messages found in <#{1102311924735168517}> in {format(end - start, '.2f')}s!")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or message.guild.id != 570929677732937738:
            return

        canal = self.bot.get_channel(1352323971860795393)
        await canal.send(f'# {message.author} {message.author.id} #{message.channel} (deleted)\n'
                         f'"`{message.content[:1900]}`"')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 1135983715646976111:
            return

        try:
            if message.guild.id in [1030490217855074304, 570929677732937738, 748126143584141332, 1134464290477330432, 1412320952678613043]:
                print(f"{message.author} imparte intelepciune: '{message.content}', #{message.channel}")
        except Exception as e:
            print(f"{message.author} imparte intelepciune: '{message.content}' DM")

        masaj = re.findall(r'\w+', str(message.content.lower()))
        try:
            name = str(message.author.display_name)
        except:
            name = ""

        if message.guild.id in [570929677732937738, 993818190008287283, 1507129472682426459]:
            if message.attachments and not message.author.bot and message.guild.id == 570929677732937738:
                canal = self.bot.get_channel(1352323971860795393)
                await canal.send(f'# {message.author} {message.author.id} #{message.channel}\n'
                                 f'"`{message.content}`"')
                # await asyncio.sleep(20)
                for attachment in message.attachments:
                    get_file_format = lambda url: f".{url.split('/')[-1].split('?')[0].split('.')[-1]}" if '.' in url.split('/')[-1] else None

                    print(get_file_format(attachment.url))
                    path = f"image{get_file_format(attachment.url)}"
                    await attachment.save(path)

                    # send the void deals if its a valid image
                    # try:
                    #     if ".png" in path or ".jpg" in path: 
                    #         void_data = await run_void_deals_ocr(path)
                    #         if void_data is not None:
                    #             await message.reply(embed=void_data, mention_author=False)
                    # except:
                    #     print("nu se poate")

                    await canal.send(f"Sent by {message.author} {message.author.id}",
                                     file=discord.File(f'image{get_file_format(attachment.url)}'))
                    print(attachment.url)
                    await asyncio.sleep(30)

            z = randint(1, 1000)
            zplus = randint(1, 10000)
            kurukuru_jackpo = randint(1, 100_000)
            kurukuru2 = 0
            dancyreply = randint(1, 5000)
            dancygif = randint(1, 50_000)
            dancyspam = randint(1, 500_000)
            dancybread = randint(1, 1_000_000)

            if (message.author.id == 556836294710525952 and str(message.content).lower() == "hmm i think im gonna get a bread now."):
                kurukuru_jackpo = 100000

            if message.author.id == 977660878080057344:
                dancyspam = 0
                dancybread = 0

            if "the" in masaj and "man" in masaj and message.author.id in [556836294710525952, 278798822937853953]:
                if masaj.index("the") < masaj.index("man"):
                    await message.channel.send("Dave the man <:LETSFUCKINGGOO:1286739473085759519>", reference=message,
                                               mention_author=False)

            if message.channel.id not in [1367130635801722972]:
                if z == 1000 or str(message.channel) == "amogus-testing" and message.channel.id:
                    await message.add_reaction("<a:kurukuru:1113242215083421707>")
                    await update(str(message.author.id), str(message.author), 1)
                    kurukuru2 = randint(1, 5)
                    if kurukuru2 == 5 or str(message.channel) == "amogus-testing":
                        await message.add_reaction("<a:kurukuru2:1139252590278889529>")
                        update(str(message.author.id), str(message.author), 2)

                if message.channel.id not in [696035168414072913, 1069249122428780636, 1367130635801722972]:
                    if kurukuru_jackpo == 100000:
                        if message.author.id == 977660878080057344:
                            kurukuru_jackpo = 0
                        else:
                            await message.reply("https://tenor.com/view/kuru-kuru-gif-10882574602170874277",
                                                mention_author=False)
                            
                            await update(str(message.author.id), str(message.author), 4)

                    if zplus == 10000 or str(message.channel) == "amogus":
                        await message.reply("<a:kurukuru:1113242215083421707>", mention_author=False)
                        await update(str(message.author.id), str(message.author), 3)

                    if dancyreply == 5000 or str(message.channel) == "amogus":
                        await message.reply("<a:dancy:1461348000977653760>", mention_author=False)
                        await update(str(message.author.id), str(message.author), 5)
                    
                    if dancygif == 50_000 or str(message.channel) == "amogus":
                        await message.reply("https://cdn.discordapp.com/emojis/1458461038889664523.gif?size=1024", mention_author=False)
                        await update(str(message.author.id), str(message.author), 6)

                    if dancyspam == 500_000 or str(message.channel) == "amogus":
                        await message.reply(f"{'<a:dancy:1461348000977653760>' * 10}", mention_author=False)
                        await update(str(message.author.id), str(message.author), 7)

                    if dancybread == 1_000_000 or str(message.channel) == "amogus":
                        await message.reply(f"{'<a:dancy:1461348000977653760>' * 10}", file=discord.File("kuru-kuru.gif"), mention_author=False)
                        await update(str(message.author.id), str(message.author), 8)


                if zplus == 10000 or kurukuru_jackpo == 100000 or z == 1000 or dancyreply == 5000 or dancygif == 50_000 or dancyspam == 500_000 or dancybread == 1_000_000:
                    chanel = self.bot.get_channel(1224041578407002153)
                    await chanel.send(file=discord.File("data.json"))

                    await update_wrapped_data("kurukuru", z == 1000, kurukuru2 == 5, zplus == 10000, kurukuru_jackpo == 100000, username=str(message.author), user_id=message.author.id)
                    chanel = self.bot.get_channel(1456699085422727402)
                    await chanel.send(file=discord.File("wrapped.json"))

            if "silwuf" in message.content and "prestige" in message.content:
                await message.channel.send(
                    "You might be wondering how I got WT Prestige, huh? Here's how: || |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| ||||:||||)|||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| |||| ||",
                    reference=message, mention_author=False)

            if message.author.id == 599358572002017281:
                t = message.content.lower()
                if "uwu" in t or "pwease" in t or "owo" in t or "sowwy" in t or "hewo" in t or "hewwo" in t:
                    # ["uwu", "pwease", "owo", "sowwy", "hewo", "hewwo"]:
                    await message.add_reaction("<a:ayakabonk:1237138645970849812>")

            if "furismug" in message.content.lower():
                if randint(1, 10) == 10:
                    await message.add_reaction("<:furismug:1272514766757433374>")
            
            if "dancy" in message.content.lower() and message.author.id != 954082451762847746:
                if randint(1, 10) == 10:
                    await message.add_reaction("<:dancy:1461348000977653760>")

            if "pettheevl" in message.content.lower():
                if randint(1, 10) == 10:
                    await message.add_reaction("<a:pettheevl:1331245568940314658>")

            if "#dark glarissa" in message.content.lower():
                await message.reply(
                    "<:Hero_Clarissa:703021406270783573> <#1169777605143166976> <:Hero_Clarissa:703021406270783573>",
                    mention_author=False)

            if "?gala" in message.content.lower():
                await message.reply(
                    f"An updated gala for players at 0-36k like <@977660878080057344> and me: [THE NEW GALA](<https://docs.google.com/document/d/1ZBD3OQuU0kuBt3L-s7zq__QWxjnge1meVs5B_nke9nM/edit?tab=t.0>)\n\n"
                    "If you only want to use the command for yourself, you can use it in <#699337693238263900> or find the link in <#637933543699513367>",
                    mention_author=False)
                await update_wrapped_data("?gala", username=message.author.name, user_id=message.author.id)

            if "?evl" in message.content.lower():
                await message.reply(
                    f"An updated evl for players at 0-36k like <@553194887701331969> and me: [THE NEW EVL](<https://docs.google.com/document/d/1ZBD3OQuU0kuBt3L-s7zq__QWxjnge1meVs5B_nke9nM/edit?tab=t.0>)\n\n"
                    "If you only want to use the command for yourself, you can use it in <#699337693238263900> or find the link in <#637933543699513367>")
                await update_wrapped_data("?evl", username=message.author.name, user_id=message.author.id)
            
            if "?cyber" in message.content.lower():
                await message.reply(f"DBG Site with most sheets/formulas: https://dbg-calculator.vercel.app", mention_author=False)
                await update_wrapped_data("?cyber", username=message.author.name, user_id=message.author.id)

            if "?tyr" in message.content.lower():
                await message.reply(
                    "Updated Optimal Rewind Calculator with stats calculations: <https://docs.google.com/spreadsheets/d/1ChZHbUy914-4r9vvcjviKCUfBqnJKiUvpnsG321XoWM/edit?gid=0#gid=0>",
                    mention_author=False)
                await update_wrapped_data("?tyr", username=message.author.name, user_id=message.author.id)

            if "?death" in message.content.lower():
                await message.channel.send("<@674287880981708821> Hi hi hello")

                await asyncio.sleep(6)

                await message.channel.send("<@674287880981708821> Once more for good measure")

                await update_wrapped_data("?death", username=message.author.name, user_id=message.author.id)

            if "?rateup" in message.content.lower():
                print("am intrat")
                embed = rateup_embed()
                print("am embed fraere", embed)

                embed.set_image(url=None)

                await message.reply(
                    f"Weekly Hero Rate-up: https://discord.com/channels/570929677732937738/570929677732937740/1369768813272371210",
                    mention_author=False, embed=embed)

                await update_wrapped_data("?rateup", username=message.author.name, user_id=message.author.id)

            if "?darksheet" in message.content.lower():
                await message.reply(
                    "You can find all Dark Tome buff values and costs here: <https://docs.google.com/spreadsheets/d/1Q1c3qUT74m3kT6ePJOm-Nib05v7I1Ua5AB9XdKn6HME/edit?gid=0#gid=0>", mention_author=False)
                await update_wrapped_data("?darksheet", username=message.author.name, user_id=message.author.id)
            
            if "?events" in message.content.lower():
                embed = get_event_week_data()
                
                await message.reply(mention_author=False, embed=embed)
                await update_wrapped_data("?events", username=message.author.name, user_id=message.author.id)

            if "?wtcalc" in message.content.lower():
                text = "<:WT_Apple:1019750592001867867> **[World Tree Calculator](<https://docs.google.com/spreadsheets/d/1A-J5gifZtwgBL1_WzR9eXIM4InxccwyIc5f998ZPKXM/edit?gid=548764124#gid=548764124>)** <:WT_Apple:1019750592001867867>  /  *[[Alternative Calc in Browser]](https://dbg-calculator.vercel.app/pages/worldtree.html)*\n" \
                "Use this to figure out where to invest your apples for the most optimal days of damage & Monarch's WT Planner to plan out your next World Tree Build! \n" \
                "(short guide on how to use it here: https://discord.com/channels/570929677732937738/1191279847427817482/1458890737193193688) \n" \
                "-# Don't forget you have to make a copy! If you're on phone, you have to download the Google Sheets app"

                await message.reply(text, mention_author=False)
                await update_wrapped_data("?wtcalc", username=message.author.name, user_id=message.author.id)

            if "?halloween" in message.content.lower():
                await message.reply(
                    "Halloween Event Boss Team: <:Hero_DarkMerlin:703020537089097789> <:Hero_Mikhail:703033570402238495> <:Hero_Max:703017718835838997> <:Hero_Dewitt:703020422005915658> <:Hero_Saul:977594194988236861> <:Hero_Garp:729434017296023675> (decent for all difficulties)\n" \
                    "For Insane, 15* <:Hero_DarkMerlin:703020537089097789> is required", mention_author=False)
                await update_wrapped_data("?halloween", username=message.author.name, user_id=message.author.id)
            
            if "?mammoths" in message.content.lower():
                if message.author.id != 954082451762847746:
                    await message.reply("https://tenor.com/view/woolly-mammoth-aio-ai-vi!deo-gif-2546557529878141509", mention_author=False)
                    await update_wrapped_data("?mammoths", username=message.author.name, user_id=message.author.id)
            
            if ("🐊" in message.content.lower() and "🎷" in message.content.lower()) or ("crocodile" in message.content.lower() and "saxophone" in message.content.lower()):
                user = await self.bot.fetch_user(message.author.id)
                print(f"sent french to {user.display_name}")
                await user.send("🇫🇷")
            
            if "🦅" in message.content.lower() and "🇺🇸" in message.content.lower():
                user = await self.bot.fetch_user(message.author.id)
                await user.send("🍔")

            if "?deals" in message.content.lower():
                embed = build_embed_today_deals()
                await message.reply(embed=embed, mention_author=False)

                await update_wrapped_data("?deals", username=message.author.name, user_id=message.author.id)

            # numar = randint(1, 50)
            # numar2 = randint(1, 5)
            # user = await self.bot.fetch_user(977660878080057344)

            # if numar2 == 1:
            #     await user.send(f"{'🇫🇷' * numar}")
            # elif numar2 == 2:
            #     await user.send(f"{'🇷🇴' * numar}")
            # elif numar2 == 3:
            #     await user.send(f"{'<a:dancy:1461348000977653760>' * numar}")
            # elif numar2 == 4:
            #     await user.send(f"{'<a:kurukuru:1113242215083421707>' * numar}")
            # elif numar2 == 5:
            #     await user.send(f"{'https://media.discordapp.net/attachments/728112209972166718/998669686554251394/image0-1.gif ' * max(1, numar // 5)}")

                
            exclusion_list = [696035168414072913, 1069249122428780636, 637388798396858379]
            parent_id = None
            try:
                parent_id = message.channel.parent.id
            except:
                pass

            if message.channel.id not in exclusion_list or parent_id not in exclusion_list:
                if message.author.id not in raids_list['list'] and 'raids' in message.content.lower():
                    raids_list['list'].append(message.author.id)
                    base_date = datetime.datetime(2022, 8, 22)
                    base_date += datetime.timedelta(weeks=675 + len(raids_list['list']))
                    unix = int(base_date.timestamp())

                    await message.reply(
                        f"Did someone mention Guild Raids? Well, they got delayed by another week, well done <@{message.author.id}>!\n"
                        f"(They are **not** developed yet!)\n**Current deadline: <t:{unix}:D>**", mention_author=False)
                    await update_raids_list(message.author.id, raids_list)
                    chanel = self.bot.get_channel(1224041578407002153)
                    await chanel.send(file=discord.File('raids_list.json'))

                    await update_wrapped_data("raids", username=message.author.name, user_id=message.author.id)

            a = message.content.lower()

            # if message.channel.id not in exclusion_list or message.channel.parent.id not in exclusion_list:
            #     if message.author.id not in update_list['list'] and ('new update' in a or "when update" in a or "update?" in a or "next update" in a or ("when" in a and "update" in a) or ("update" in a and "?" in a)):
            #         update_list['list'].append(message.author.id)
            #         base_date = datetime.datetime(2025, 3, 1)
            #         base_date += datetime.timedelta(weeks=len(update_list['list']) * 2)
            #         unix = int(base_date.timestamp())

            #         await message.reply(f"Did someone mention the new update? Well, it got delayed by two weeks, well done <@{message.author.id}>!\n"
            #                             f"(It is **not** developed yet!)\n**Current deadline: <t:{unix}:D>**", mention_author=False)
            #         await update_update_list(message.author.id, update_list)
            #         chanel = self.bot.get_channel(1224041578407002153)
            #         await chanel.send(file=discord.File('update_list.json'))

        elif message.guild.id in [993818190008287283, 1134464290477330432, 1030490217855074304, 1412320952678613043]:
            global jailtime
            x = randint(1, 500)
            #
            # if message.author.id == 352815253828141056 or "whar" in message.content.lower() or "whatr" in message.content.lower():
            #     await message.delete()
            # elif message.author.id in jail.ceva_id and jail.jailtime is True:
            #     a = message.content
            #     if a == "":
            #         a = "*some random attachment*"
            #     await channel.send(f"**{name} in <#{message.channel.id}>**: {a}")
            #     await asyncio.sleep(2)
            #     await message.delete()
            #
            # if message.author.id == 692045914436796436 and message.channel.id != 1136284162832224276:
            #     await message.delete()
            #     await message.channel.send("<#1136284162832224276> idiot")

            if str(message.channel) == "administratum" or str(message.channel) == "teme":
                x = 0
            elif str(message.channel) == "amogus-testing":
                x = 500
            if x == 501:
                funni = [f"Haha how funny of you {name} <:keek:806077897584410685>", "Ong fr fr", "*silence*",
                         "<:pogFrog:802088916244234261>", "Just no <:pepe_flower:901873383212462091>", "YES", "ඞ",
                         f"{name} stinks", "Based", "Why?", "Are you sure?", "💀", "Please don't", "Please do",
                         "Not based",
                         "Great idea!", "Bad idea!", "*claps*", "*throws up*", "🤝", "<a:kurukuru:1113242215083421707>",
                         "Who asked?", "And?", "Ok buddy", f"This is why {name} shouldn't run for president",
                         "Thanks for the idea",
                         "Why does that matter?", "My reaction to that information: 💀",
                         "Do you know what you're talking about?",
                         f"This is not proper etiquette, {name}", "Do NOT say this again", "You can say that again!",
                         "Fr?",
                         "🧢",
                         "I was today years old when I realized I didn’t like you.",
                         "Someday you’ll go far. And I really hope you stay there.",
                         "Oops, my bad. I could’ve sworn I was dealing with an adult.",
                         "I love what you’ve done with your hair. How do you get it to come out of your nostrils like that?",
                         "Remember that time you were saying that thing I didn’t care about? Yeah, that is now.",
                         "You’re the reason God created the middle finger.",
                         "I’m busy right now, can I ignore you another time?",
                         "Oh, you don’t like being treated the way you treat me? That must suck.",
                         "I wish I had a flip phone, so I could slam it shut on this conversation.",
                         "N’Sync said it best, “BYE, BYE, BYE!”",
                         "I’ve been called worse things by better men.",
                         "You’re a gray sprinkle on a rainbow cupcake.",
                         "Your secrets are always safe with me. I never even listen when you tell me them.",
                         "You bring everyone so much joy! You know, when you leave the room. But, still.",
                         "How many licks until I get to the interesting part of this conversation?",
                         "Keep rolling your eyes, you might eventually find a brain.",
                         "Your face makes onions cry.",
                         "Did I invite you to the barbecue? Then why are you all up in my grill?",
                         "Our kid must have gotten his brain from you! I still have mine.",
                         "You have so many gaps in your teeth it looks like your tongue is in jail.",
                         "If your brain was dynamite, there wouldn’t be enough to blow your hat off.",
                         "You are more disappointing than an unsalted pretzel.",
                         "It’s impossible to underestimate you.",
                         "Wow, your maker really didn’t waste time giving you a personality, huh?",
                         "Her teeth were so bad she could eat an apple through a fence.",
                         "I’ll never forget the first time we met. But I’ll keep trying.",
                         "Oh, I’m sorry. Did the middle of my sentence interrupt the beginning of yours?",
                         "Hold still. I’m trying to imagine you with personality.",
                         "I’m not insulting you, I’m describing you.",
                         "You are the human version of period cramps.",
                         "You’re cute. Like my dog. He also chases his tail for entertainment.",
                         "You are like a cloud. When you disappear, it’s a beautiful day.",
                         "You have an entire life to be an idiot. Why not take today off?",
                         "Your kid is so annoying, he makes his Happy Meal cry.",
                         "Your face is just fine, but we’ll have to put a bag over that personality.",
                         "I’m not a nerd. I’m just smarter than you.",
                         "I may love to shop but I will never buy your bull.",
                         "Child, I’ve forgotten more than you ever knew.",
                         "I’m an acquired taste. If you don’t like me, acquire some taste.",
                         "Bye. Hope to see you never.",
                         "Don’t worry, the first 40 years of childhood are always the hardest.",
                         "If you’re going to be two-faced, at least make one of them pretty.",
                         "The only way my husband would ever get hurt during an activity is if the TV exploded.",
                         "If you have a problem with me, write the problem on a piece of paper, fold it, and shove it up your ass.",
                         "Complete this sentence for me: 'I never want to see you ————!'",
                         "I thought of you today. It reminded me to take out the trash.",
                         "You bring everyone so much joy when you leave the room.",
                         "Did the mental hospital test too many drugs on you today?",
                         "OH MY GOD! IT SPEAKS!",
                         "Beauty is only skin deep, but ugly goes clean to the bone.",
                         "I’d like to help you out. Which way did you come in?",
                         "I forgot the world revolves around you. My apologies, how silly of me.",
                         "Light travels faster than sound which is why you seemed bright until you spoke.",
                         "I’d rather treat my baby’s diaper rash than have lunch with you.",
                         "You look so pretty. Not at all gross, today.",
                         "I only take you everywhere I go, so I don’t have to kiss you goodbye.",
                         "We were happily married for one month, but unfortunately, we’ve been married for 10 years.",
                         "When you look in the mirror, say hi to the clown you see in there for me, would you?",
                         "Somewhere out there is a tree tirelessly producing oxygen for you. You owe it an apology.",
                         "That sounds like a you problem.",
                         "You have miles to go before you reach mediocre."]
                if message.guild.id == 1412320952678613043:
                    Dave_quotes = ["Dave can divide by zero.",
                                   "Dave counted to infinity. Twice.",
                                   "When Dave enters a room, he doesn't turn the lights on; he turns the dark off.",
                                   "Dave can slam a revolving door.",
                                   "Dave can unscramble an egg.",
                                   "Dave can hear sign language.",
                                   "Dave can find the needle in the haystack and the haystack in the needle.",
                                   "Dave can speak Braille.",
                                   "Dave can win a game of Connect Four in three moves.",
                                   "When Dave does push-ups, he doesn't push himself up; he pushes the Earth down.",
                                   "Dave can make a happy meal cry.",
                                   "Dave doesn't wear a watch; he decides what time it is.",
                                   "Dave can build a snowman out of rain.",
                                   "Dave doesn't need GPS; he is the direction.",
                                   "Dave can unbreak broken glass.",
                                   "Dave can hear your thoughts, but he's not interested.",
                                   "When Dave does a push-up, he's not lifting himself up; he's pushing the Earth down.",
                                   "Dave can delete the Recycling Bin.",
                                   "Dave can un-invent the wheel.",
                                   "Dave can divide by zero and get a valid answer.",
                                   "Dave can pick oranges from an apple tree and make the best lemonade you've ever tasted.",
                                   "Dave's tears can cure cancer. Too bad he has never cried.",
                                   "Dave can win a game of chess with just one move: a roundhouse kick to the opponent's king.",
                                   "Dave can hear a pin drop in a thunderstorm.",
                                   "Dave can hear the sound of one hand clapping.",
                                   "Dave can taste the rainbow.",
                                   "Dave can hear silence.",
                                   "Dave can turn water into wine, but he prefers beer.",
                                   "Dave can hear you blinking.",
                                   "Dave can slam a revolving door.",
                                   "Dave can make a fire by rubbing two ice cubes together.",
                                   "Dave can drown a fish.",
                                   "Dave can breathe underwater, but he chooses not to, to give other fish a chance.",
                                   "Dave doesn't do push-ups; he pushes the Earth down.",
                                   "Dave can divide by zero.",
                                   "Dave can build a snowman out of rain.",
                                   "Dave can find the remote control without looking.",
                                   "Dave can win a game of hide and seek in the dark.",
                                   "Dave can slam a revolving door.",
                                   "Dave can write a novel with a single letter.",
                                   "Dave can make a snow angel in the desert.",
                                   "Dave can grill a popsicle.",
                                   "Dave can tie his shoes with his feet.",
                                   "Dave can cut through a hot knife with butter.",
                                   "Dave can uncook a scrambled egg.",
                                   "Dave can speak braille.",
                                   "Dave can unscramble scrambled eggs.",
                                   "Dave can break the sound barrier with his silence.",
                                   "Dave can make a volcano erupt by staring at it.",
                                   "Dave can make onions cry.",
                                   "Dave can slam a revolving door.",
                                   "Dave can eat just one Lay's potato chip.",
                                   "Dave can win a staring contest against the sun.",
                                   "Dave can talk in Morse code.",
                                   "Dave can play the violin with a piano.",
                                   "Dave can fold a piece of paper more than seven times.",
                                   "Dave can alphabetize a dictionary.",
                                   "Dave can make a circle with a square.",
                                   "Dave can cut a knife with butter.",
                                   "Dave can make a snake laugh.",
                                   "Dave can make a triangle with two sides.",
                                   "Dave can unscramble a jigsaw puzzle in one second.",
                                   "Dave can make a square dance in a round room.",
                                   "Dave can jump off the ground and miss.",
                                   "Dave can draw a perfect circle without a compass.",
                                   "Dave can write a book without words.",
                                   "Dave can color a rainbow with just one crayon.",
                                   "Dave can solve a Rubik's Cube blindfolded... with his feet.",
                                   "Dave can speak every language, including sign language.",
                                   "Dave can ride a unicycle... with training wheels.",
                                   "Dave can make a snowman out of sand.",
                                   "Dave can eat soup with a fork.",
                                   "Dave can make a cat bark.",
                                   "Dave can make a pineapple pizza taste good.",
                                   "Dave can walk on sunshine.",
                                   "Dave can make a black hole blink.",
                                   "Dave can make a tree fall in a forest and everyone will hear it.",
                                   "Dave can make a mirror reflect on its life choices.",
                                   "Dave can make a rock sweat.",
                                   "Dave can make a triangle have four sides.",
                                   "Dave can hear a pin drop in a thunderstorm.",
                                   "Dave can hear the sound of one hand clapping.",
                                   "Dave can taste the rainbow.",
                                   "Dave can hear silence.",
                                   "Dave can turn water into wine, but he prefers beer.",
                                   "Dave can hear you blinking.",
                                   "Dave can slam a revolving door.",
                                   "Dave can make a fire by rubbing two ice cubes together.",
                                   "Dave can drown a fish.",
                                   "Dave can breathe underwater, but he chooses not to, to give other fish a chance.",
                                   "Dave doesn't do push-ups; he pushes the Earth down.",
                                   "Dave can divide by zero.",
                                   "Dave can build a snowman out of rain.",
                                   "Dave can find the remote control without looking.",
                                   "Dave can win a game of hide and seek in the dark.",
                                   "Dave can slam a revolving door.",
                                   "Dave can write a novel with a single letter.",
                                   "Dave can make a snow angel in the desert.",
                                   "Dave can grill a popsicle.",
                                   "Dave can tie his shoes with his feet.",
                                   "Dave can cut through a hot knife with butter.",
                                   "Dave can uncook a scrambled egg.",
                                   "Dave can speak braille.",
                                   "Dave can unscramble scrambled eggs.",
                                   "Dave can break the sound barrier with his silence.",
                                   "Dave can make a volcano erupt by staring at it.",
                                   "Dave can make onions cry.",
                                   "Dave can slam a revolving door.",
                                   "Dave can eat just one Lay's potato chip."]
                    funni += Dave_quotes

                random = randint(0, (len(funni) - 1))
                chestie = funni[random]
                user_id = [556836294710525952, 1012877247956402257, 555455936760905780]
                if chestie == f"{name} stinks" and message.author.id in user_id:
                    await message.channel.send(f"{name} smells good. <:pepeloon:910540003828985926>", reference=message,
                                               mention_author=False)
                elif chestie == "ඞ":
                    random_amogus = randint(0, 100)
                    chestie *= random_amogus
                    await message.channel.send(f"{chestie}, *Amogus rolled: {random_amogus}*", reference=message,
                                               mention_author=False)
                else:
                    await message.channel.send(chestie, reference=message, mention_author=False)

            if "the" in masaj and "man" in masaj:
                if masaj.index("the") < masaj.index("man"):
                    await message.channel.send("Dave the man <:LETSFUCKINGGOO:1286739473085759519>", reference=message,
                                               mention_author=False)

            a = message.content.lower()
            if "beck" in a or 'bekc' in a:
                await message.delete()

            # if message.author.id != 556836294710525952:
            #     if "https" in a:
            #         print('fmm ralf')
            #         if "zzz" in a or 'burnice' in a or 'jane' in a or 'doe' in a or 'zenless' in a or 'zone' in a or 'mp4' in a or 'gif' in a or 'tenor' in a:
            #             await message.delete()

            #     if message.attachments:
            #         for attachment in message.attachments:
            #             if 'gif' in attachment.url or 'mp4' in attachment.url:
            #                 await message.delete()
            #                 break

            if "esketit" in masaj:
                await message.channel.send("https://tenor.com/view/lets-lets-get-it-gif-14167426", reference=message,
                                           mention_author=False)

            if "<@1135983715646976111>" in message.content.lower():
                reply = ["https://cdn.discordapp.com/emojis/1078009688366522580.gif", "I require professional help",
                         "My mental state is declining <a:kurukuru:1113242215083421707>"]
                random_reply = randint(0, (len(reply) - 1))
                await message.channel.send(reply[random_reply], reference=message, mention_author=True)

            if message.author.id == 763698307276079155 and "badescu" in message.content.lower():
                await message.channel.send("I love you too, cocalarule", reference=message, mention_author=False)

            if "Did you ever heard about our god and savior" in message.content:
                await message.channel.send("No I haven't, and leave me the fuck alone", reference=message,
                                           mention_author=False)


async def setup(bot):
    await bot.add_cog(Funni(bot))