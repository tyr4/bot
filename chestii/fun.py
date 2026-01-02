import datetime
import pytz

import discord
import random
from discord.ext import commands
from discord import app_commands

from PIL import Image, ImageSequence
from io import BytesIO
import asyncio
import json
import re
import os
import gspread
from google.oauth2.service_account import Credentials
import csv


cooldown = False
leaderboard_spots = [":first_place:", ":second_place:", ":third_place:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:"]

def init_sheet():
    # Path to your service account key file
    SERVICE_ACCOUNT_FILE = 'google_sheets_api_key.json'

    # Define the scope
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # Authenticate using the service account key
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Use gspread to access the Google Sheets API
    gc = gspread.authorize(creds)

    # Open the Google Sheet by its title or URL
    sheet = gc.open_by_key("1v52n_je0xtmGRkokTA-oYEPd-0FGmDazVddayyKEv7Y")
    worksheet = sheet.worksheet('dbg-ct')


    return sheet, worksheet


def leaderboard(user: int, mode: int, lb_name):
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        kuru = "kurureact1" if mode == 1 else ("kurureact2" if mode == 2 else ("kuruemote" if mode == 3 else ("kurugif" if mode == 4 else None)))
        react = "Reactions" if mode == 1 or mode == 2 else ("Replies" if mode == 3 or mode == 4 else None)
        ceva = ""
        if kuru is None:
            return 0
        print(mode, kuru)
        embed = discord.Embed(title=f"{lb_name} Leaderboard <a:kafkakurukuru:1118233531110412461>", color=0x71368a)
        embed.add_field(name="__Kurukuru chances__", value=f"On any message, you have:\n<a:kurukuru:1113242215083421707> Reaction - 1/1000 Chance\n"
                                                       f"<a:kurukuru2:1139252590278889529> Reaction - 1/5 Chance (if you get the first one)\n"
                                                       f"<a:kurukuru:1113242215083421707> Reply - 1/10000 Chance\n"
                                                       f"<a:kurukurubread:1196187723967516904> GIF Reply - 1/100000 Chance", inline=False)
        idk = ""
        sorted_data = sorted(data.items(), key=lambda x: x[1][kuru], reverse=True)
        for i, (key, value) in enumerate(sorted_data):
            spot = f"#{i + 1}" if i >= 10 else leaderboard_spots[i]
            if mode == 1 or mode == 2:
                if value[kuru] == 1:
                    react = "Reaction"
                else:
                    react = "Reactions"
            elif mode == 3 or mode == 4:
                if value[kuru] == 1:
                    react = "Reply"
                else:
                    react = "Replies"

            if key == str(user):
                ceva = f"{spot} <@{key}> ({value['name']}) - {value[kuru]} {react}"
                if i >= 10:
                    break
            if i < 10 and value[kuru] != 0:
                idk += f"{spot} <@{key}> ({value['name']}) - {value[kuru]} {react}\n"
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


def funni_gif(input):
    gif_path = "stab_empty.gif"
    gif = Image.open(gif_path)

    input_image = Image.open(input)
    input_image = input_image.convert("RGBA")

    new_size = (140, 140)
    input_image = input_image.resize(new_size)
    input_image = input_image.rotate(-25, expand=True)

    frames = []
    for frame_number, frame in enumerate(ImageSequence.Iterator(gif)):
        new_frame = frame.copy()
        stab_frame = Image.open(f'frames/frame_{frame_number}.png').convert("RGBA")
        middle_x = new_frame.width // 6
        middle_y = new_frame.height // 6

        if frame_number == 0:
            position = (middle_x - 12, middle_y - input_image.height // 6)
        elif frame_number == 2:
            position = (middle_x + 3, middle_y - input_image.height // 6)
        elif frame_number == 3:
            position = (middle_x + 13, middle_y - input_image.height // 6)
        elif frame_number in range(4, 10):
            position = (middle_x - 12, middle_y - input_image.height // 6)
        elif frame_number == 10:
            position = (middle_x + 12, middle_y - input_image.height // 6)
        elif frame_number == 11:
            position = (middle_x + 32, middle_y - input_image.height // 6)
        elif frame_number == 12:
            input_image = input_image.rotate(-10, expand=True)
            position = (middle_x, middle_y + (input_image.height // 6) - 20)
        elif frame_number == 43:
            input_image = input_image.rotate(20, expand=True)
            position = (middle_x - 15, middle_y + (input_image.height // 6) - 7)
        elif frame_number == 44:
            position = (middle_x - 35, middle_y + (input_image.height // 6) - 55)
        elif frame_number == 45:
            position = (middle_x - 45, middle_y + (input_image.height // 6) - 65)
        elif frame_number == 46:
            input_image.rotate(-5, expand=True)
            position = (middle_x - 52, middle_y - input_image.height // 6 - 22)
        elif frame_number == 47:
            input_image.rotate(5, expand=True)
            position = (middle_x - 62, middle_y - input_image.height // 6 - 32)
        elif frame_number in (48, 53):
            position = (middle_x - 62, middle_y - input_image.height // 6 - 32)

        new_frame.paste(input_image, position, input_image) if frame_number not in range(13, 43) else None
        new_frame.paste(stab_frame, (0, 0), stab_frame)
        frames.append(new_frame)

    for frame in frames:
        frame = frame.convert('P', palette=Image.ADAPTIVE)
    frames[1].save("output.gif", save_all=True, append_images=frames[1:], loop=gif.info['loop'], disposal=2)


def funni_pet(input):
    gif_path = "pet_template.gif"
    gif = Image.open(gif_path)

    input_image = Image.open(input)
    input_image = input_image.convert("RGBA")

    new_size = (128, 128)
    input_image = input_image.resize(new_size)
    original_width, original_height = input_image.size

    frames = []
    i = 1.1
    j = 1
    idk = 6
    for frame_number, frame in enumerate(ImageSequence.Iterator(gif)):
        new_frame = frame.copy()
        pet_frame = Image.open(f'pet_frames/frame_{frame_number + 1}.png').convert("RGBA")
        if frame_number <= 5:
            input_image = input_image.resize((int(original_width * i), int(original_height * j)))
            i += 0.03
            j -= 0.05
        else:
            i -= 0.05
            j += 0.05
            input_image = input_image.resize((int(original_width * (i * 0.96)), int(original_height * j)))
        idk += 1

        new_frame.paste(input_image, (20 + idk, 75 - idk), input_image)
        new_frame.paste(pet_frame, (0, 0), pet_frame)

        frames.append(new_frame)

    frames[1].save("output.gif", save_all=True, append_images=frames[1:], loop=gif.info['loop'], disposal=2, duration=30)


def outfit(helmet_rando, armor_rando, boots_rando, guild):
    player = Image.open("player default stance.png")
    background = Image.open("spring bg.png")
    # helmet_rando = randint(0, 32)
    # helmet_rando += 1 if helmet_rando == 14 else 0
    # armor_rando = randint(0, 21)
    # boots_rando = randint(0, 20)
    #
    helmet = Image.open(f"gear big/helmet_{helmet_rando}.png").convert("RGBA")
    armor = Image.open(f"gear big/armor_{armor_rando}.png").convert("RGBA")
    boots = Image.open(f"gear big/boots_{boots_rando}.png").convert("RGBA")
    za_hando = Image.open("player hand lol.png")
    za_legs = Image.open("za legs.png")

    if boots_rando or not boots_rando:
        if boots_rando in [11, 12, 14, 15]:
            player.paste(boots, (81, 181), boots)
            player.paste(boots, (126, 181), boots)
        elif boots_rando == 18:
            player.paste(boots, (78, 181), boots)
            player.paste(boots, (120, 181), boots)
        elif boots_rando == 19:
            player.paste(boots, (80, 171), boots)
            player.paste(boots, (128, 171), boots)
        elif boots_rando < 6:
            player.paste(boots, (83, 171), boots)
            player.paste(boots, (126, 171), boots)
        else:
            player.paste(boots, (78, 171), boots)
            player.paste(boots, (123, 171), boots)

    if armor_rando or not armor_rando:
        if armor_rando == 4:
            player.paste(armor, (40, 86), armor)
        elif armor_rando == 6:
            player.paste(armor, (80, 90), armor)
        elif armor_rando == 7:
            player.paste(armor, (86, 93), armor)
        elif armor_rando == 8:
            player.paste(armor, (77, 93), armor)
        elif armor_rando == 9:
            player.paste(armor, (58, 90), armor)
        elif armor_rando == 10:
            player.paste(armor, (78, 92), armor)
        elif armor_rando == 11:
            player.paste(armor, (80, 92), armor)
        elif armor_rando == 12:
            player.paste(armor, (43, 90), armor)
        elif armor_rando == 13:
            player.paste(armor, (57, 95), armor)
        elif armor_rando == 14:
            player.paste(armor, (46, 85), armor)
        elif armor_rando == 15:
            player.paste(armor, (82, 94), armor)
        elif armor_rando == 16:
            player.paste(armor, (78, 95), armor)
        elif armor_rando == 17:
            player.paste(armor, (64, 95), armor)
        elif armor_rando == 18:
            player.paste(armor, (63, 80), armor)
        elif armor_rando == 19:
            player.paste(armor, (82, 130), armor)
        elif armor_rando == 20:
            player.paste(armor, (10, 13), armor)
        elif armor_rando == 21:
            player.paste(armor, (78, 95), armor)
        else:
            player.paste(armor, (63, 90), armor)

    if helmet_rando or not helmet_rando:
        if helmet_rando == 0:
            player.paste(helmet, (77, 20), helmet)
        elif helmet_rando == 1:
            player.paste(helmet, (65, 3), helmet)
        elif helmet_rando == 2:
            player.paste(helmet, (65, 8), helmet)
        elif helmet_rando == 3:
            player.paste(helmet, (66, 3), helmet)
        elif helmet_rando == 4:
            player.paste(helmet, (76, 3), helmet)
        elif helmet_rando == 5:
            player.paste(helmet, (68, 40), helmet)
        elif helmet_rando == 6:
            player.paste(helmet, (73, 5), helmet)
        elif helmet_rando == 7:
            player.paste(helmet, (78, 70), helmet)
        elif helmet_rando == 8:
            player.paste(helmet, (58, 5), helmet)
        elif helmet_rando == 9:
            player.paste(helmet, (73, 13), helmet)
        elif helmet_rando == 10:
            player.paste(helmet, (68, 20), helmet)
        elif helmet_rando == 11:
            player.paste(helmet, (78, 55), helmet)
        elif helmet_rando == 12:
            player.paste(helmet, (72, -6), helmet)
        elif helmet_rando == 13:
            player.paste(helmet, (72, 18), helmet)
        elif helmet_rando == 15:
            player.paste(helmet, (115, 18), helmet)
        elif helmet_rando == 16:
            player.paste(helmet, (59, 13), helmet)
        elif helmet_rando == 17:
            player.paste(helmet, (55, 13), helmet)
        elif helmet_rando == 18:
            player.paste(helmet, (66, 18), helmet)
        elif helmet_rando == 19:
            player.paste(helmet, (74, 10), helmet)
        elif helmet_rando == 20:
            player.paste(helmet, (74, 10), helmet)
        elif helmet_rando == 21:
            player.paste(helmet, (74, 22), helmet)
        elif helmet_rando == 22:
            player.paste(helmet, (74, 17), helmet)
        elif helmet_rando == 23:
            player.paste(helmet, (63, 8), helmet)
        elif helmet_rando == 24:
            player.paste(helmet, (65, 22), helmet)
        elif helmet_rando == 25:
            player.paste(helmet, (67, 25), helmet)
        elif helmet_rando == 26:
            player.paste(helmet, (77, 6), helmet)
        elif helmet_rando == 27:
            player.paste(helmet, (81, 70), helmet)
        elif helmet_rando == 28:
            player.paste(helmet, (58, 18), helmet)
        elif helmet_rando == 29:
            player.paste(helmet, (94, 58), helmet)
        elif helmet_rando == 30:
            player.paste(helmet, (81, 50), helmet)
        elif helmet_rando == 31:
            player.paste(helmet, (81, 50), helmet)
        elif helmet_rando == 32:
            player.paste(helmet, (75, 10), helmet)

    if boots_rando == 100:
        player.paste(za_legs, (0, 0), za_legs)
    player.paste(za_hando, (0, 0), za_hando)
    if guild not in [897064561113456681, 993818190008287283]:
        background.paste(player, (-3, 10), player)
        background.resize((183, 170))
        background.save("defender drip.png")
    else:
        player.save("defender drip.png")    
    print('Done!')


def update_counting_sheet(number, user, user_id, timestamp, message):
    timestamp_str = timestamp.strftime("%d/%m/%Y %I:%M:%S %p")
    data = [number, user, str(user_id), timestamp_str, message]

    # Read column A once (single API call)
    col_a = worksheet.col_values(1)
    first_empty_row = len(col_a) + 1

    # Write the row directly
    worksheet.update(f"A{first_empty_row}:E{first_empty_row}", [data])
    print(f"Appended to row {first_empty_row}")


def update_with_matrix(matrice):
    matrix_len = 1
    for i in matrice:
        matrix_len += 1
    
    worksheet.update(f"A2:E{matrix_len}", matrice)

sheet, worksheet = init_sheet()

class Fun(commands.GroupCog, name="fun"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="stab", description="Stab someone idk")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: i.guild_id)
    @app_commands.describe(invisible="Enabling this will only make the command visible for you (automatically off for #bot-commands")
    async def stab(self, interaction: discord.Interaction, user: discord.Member, invisible: bool = False) -> None:
        global cooldown
        global counter

        if user.id in [556836294710525952]:
            await interaction.response.send_message("Nice try", ephemeral=True)
            return
        elif user.id == 151495292418654210 and interaction.user.id not in [556836294710525952]:
            await interaction.response.send_message("<a:muffinlick2:1283857270995812454>")
            return
        elif user.id == 230678674435735552:
            await interaction.response.send_message("<a:vertgun:1201573150132019321>")
            return

        if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
            await interaction.response.defer()
        elif invisible is True:
            await interaction.response.defer(ephemeral=True)
        else:
            await interaction.response.defer()

        stab_chance = random.randint(1, 4)
        print("hah")
        if user.id == 1135983715646976111:
            await user.avatar.save('avatar.png')
            print("idk")
            print(stab_chance)
            if stab_chance == 4:
                funni_gif('avatar.png')
            else:
                funni_pet('avatar.png')
        else:
            await user.avatar.save('avatar.png')
            funni_gif('avatar.png')

        guild = self.bot.get_guild(993818190008287283)
        for emoji in guild.emojis:
            if emoji.name == "output":
                await emoji.delete()
                break

        with open("output.gif", "rb") as img:
            img_byte = img.read()
            await guild.create_custom_emoji(name="output", image=img_byte)
            await asyncio.sleep(2)

        for emoji in guild.emojis:
            if emoji.name == "output":
                emote = emoji
                break

        await interaction.followup.send(emote)

    @app_commands.command(name="pet", description="Pet someone idk")
    @app_commands.checks.cooldown(1, 10.0, key=lambda i: i.guild_id)
    @app_commands.describe(invisible="Enabling this will only make the command visible for you (automatically off for #bot-commands")
    async def pet(self, interaction: discord.Interaction, user: discord.Member, invisible: bool = False) -> None:
        if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
            await interaction.response.defer()
        elif invisible is True:
            await interaction.response.defer(ephemeral=True)
        else:
            await interaction.response.defer()
        await user.avatar.save('avatar.png')
        funni_pet('avatar.png')

        guild = self.bot.get_guild(993818190008287283)
        for emoji in guild.emojis:
            if emoji.name == "output":
                await emoji.delete()
                break

        with open("output.gif", "rb") as img:
            img_byte = img.read()
            await guild.create_custom_emoji(name="output", image=img_byte)
            await asyncio.sleep(2)

        for emoji in guild.emojis:
            if emoji.name == "output":
                emote = emoji
                break

        await interaction.followup.send(emote)

    @app_commands.command(name="defender_outfit", description="Visual representation of gear on Defender")
    @app_commands.describe(helmet="Pick the first option if the helmet you want is in the 2nd list, else pick one from here")
    @app_commands.describe(rest_of_the_helmets="Pick the first option if the helmet you want is in the first list, else pick one from here")
    @app_commands.describe(invisible="Enabling this will only make the command visible for you (automatically off for #bot-commands")
    @app_commands.choices(helmet=[
        discord.app_commands.Choice(name='Pick this if you already made your choice', value=69),
        discord.app_commands.Choice(name='3D Glasses', value=30),
        discord.app_commands.Choice(name='Brown Fedora', value=18),
        discord.app_commands.Choice(name='Bucket Helm', value=20),
        discord.app_commands.Choice(name='Cheap Headphones', value=5),
        discord.app_commands.Choice(name='Cozy Hat', value=8),
        discord.app_commands.Choice(name='Cowboy Hat', value=25),
        discord.app_commands.Choice(name='Crimson Beak', value=27),
        discord.app_commands.Choice(name='Crown', value=9),
        discord.app_commands.Choice(name='Cute Headphones', value=10),
        discord.app_commands.Choice(name='Fez', value=26),
        discord.app_commands.Choice(name='Graduation Cap', value=23),
        discord.app_commands.Choice(name='Great Helm', value=21),
        discord.app_commands.Choice(name='Hard Hat', value=19),
        discord.app_commands.Choice(name='Kingsguard Helm', value=22),
        discord.app_commands.Choice(name='Midas Helm', value=1),
        discord.app_commands.Choice(name='Mushroom Cap', value=16),
        discord.app_commands.Choice(name='Oni Mask', value=3),
        discord.app_commands.Choice(name='Panama Hat', value=24),
        discord.app_commands.Choice(name='Peaked Cap', value=13),
        discord.app_commands.Choice(name='Pointy Hat', value=12),
        discord.app_commands.Choice(name='Propeller Cap', value=4),
        discord.app_commands.Choice(name='Reading Glasses', value=11),
        discord.app_commands.Choice(name='Santa Hat', value=28),
        discord.app_commands.Choice(name='Steampunk Goggles', value=31),

    ], rest_of_the_helmets=[
        discord.app_commands.Choice(name='Pick this if you already made your choice', value=69),
        discord.app_commands.Choice(name='Steel Helm', value=0),
        discord.app_commands.Choice(name='Straw Hat', value=17),
        discord.app_commands.Choice(name='Strawberry Cone', value=15),
        discord.app_commands.Choice(name='Bucket Helm', value=20),
        discord.app_commands.Choice(name='Surgical Mask', value=7),
        discord.app_commands.Choice(name='Suspicious Goggles', value=29),
        discord.app_commands.Choice(name='Top Hat', value=6),
        discord.app_commands.Choice(name='Transparent Cap', value=100),
        discord.app_commands.Choice(name='Voidmask', value=2),
    ], chestplate=[
        discord.app_commands.Choice(name='Abyssal Armor', value=14),
        discord.app_commands.Choice(name='Apron', value=7),
        discord.app_commands.Choice(name='Away Jersey', value=16),
        discord.app_commands.Choice(name='Belt', value=19),
        discord.app_commands.Choice(name='Bronze Armor', value=1),
        discord.app_commands.Choice(name='Chainmail', value=15),
        discord.app_commands.Choice(name='Copper Armor', value=3),
        discord.app_commands.Choice(name='Emerald Armor', value=12),
        discord.app_commands.Choice(name='Forsaken Wings', value=20),
        discord.app_commands.Choice(name='Galaxy Armor', value=17),
        discord.app_commands.Choice(name='Home Jersey', value=21),
        discord.app_commands.Choice(name='Life Vest', value=8),
        discord.app_commands.Choice(name='Majestic Armor', value=4),
        discord.app_commands.Choice(name='Mithril Armor', value=0),
        discord.app_commands.Choice(name='Native Armor', value=5),
        discord.app_commands.Choice(name='Oriental Armor', value=2),
        discord.app_commands.Choice(name='Oxygen Tank', value=18),
        discord.app_commands.Choice(name='Red Scarf', value=10),
        discord.app_commands.Choice(name='Satchel', value=11),
        discord.app_commands.Choice(name='School Backpack', value=9),
        discord.app_commands.Choice(name='Shaolin Armor', value=6),
        discord.app_commands.Choice(name='Transparent Armor', value=100),
        discord.app_commands.Choice(name='Vestige Armor', value=13),
    ], boots=[
        discord.app_commands.Choice(name='Aquamarine Boots', value=20),
        discord.app_commands.Choice(name='Arctic Boots', value=3),
        discord.app_commands.Choice(name='Boots of Steel', value=1),
        discord.app_commands.Choice(name='Bronze Greaves', value=6),
        discord.app_commands.Choice(name='Dark Walkers', value=4),
        discord.app_commands.Choice(name='Divine Greaves', value=10),
        discord.app_commands.Choice(name='Flippers', value=18),
        discord.app_commands.Choice(name='Fuzzy Slides', value=15),
        discord.app_commands.Choice(name='Galaxy Greaves', value=17),
        discord.app_commands.Choice(name='Glass Shoes', value=5),
        discord.app_commands.Choice(name='Grandeur Greaves', value=8),
        discord.app_commands.Choice(name='Leather Boots', value=0),
        discord.app_commands.Choice(name='Midas Boots', value=2),
        discord.app_commands.Choice(name='Mithril Greaves', value=7),
        discord.app_commands.Choice(name='Oriental Greaves', value=16),
        discord.app_commands.Choice(name='Red Sneakers', value=12),
        discord.app_commands.Choice(name='Sandals', value=19),
        discord.app_commands.Choice(name='Slides', value=14),
        discord.app_commands.Choice(name='Socks', value=13),
        discord.app_commands.Choice(name='Transparent Boots', value=100),
        discord.app_commands.Choice(name='Voidtreads', value=9),
        discord.app_commands.Choice(name='White Sneakers', value=11),
    ])
    async def defefender(self, interaction: discord.Interaction, helmet: discord.app_commands.Choice[int], rest_of_the_helmets: discord.app_commands.Choice[int],
                         chestplate: discord.app_commands.Choice[int], boots: discord.app_commands.Choice[int], invisible: bool = True):
        helm_value = helmet.value
        if helmet.value == 69:
            helm_value = rest_of_the_helmets.value
        print(chestplate.value)
        outfit(helm_value, chestplate.value, boots.value, interaction.guild.id)
        if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
            await interaction.response.send_message(file=discord.File('defender drip.png'))
        elif invisible is True:
            await interaction.response.send_message(file=discord.File('defender drip.png'), ephemeral=True)
        else:
            await interaction.response.send_message(file=discord.File('defender drip.png'))
        await interaction.response.send_message(file=discord.File('defender drip.png'))

    @app_commands.command(name="random_defender_outfit", description="Visual representation of random gear on Defender")
    @app_commands.describe(invisible="Enabling this will only make the command visible for you (automatically off for #bot-commands")
    async def random_defefefneder(self, interaction: discord.Interaction, invisible: bool = True):
        helmet_rando = random.randint(0, 33)
        if helmet_rando == 33:
            helmet_rando = 100
        helmet_rando += 1 if helmet_rando == 14 else 0
        armor_rando = random.randint(0, 22)
        if armor_rando == 22:
            armor_rando = 100
        boots_rando = random.randint(0, 21)
        if boots_rando == 21:
            boots_rando = 100
        outfit(helmet_rando, armor_rando, boots_rando, interaction.guild.id)

        if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
            await interaction.response.send_message(file=discord.File('defender drip.png'))
        elif invisible is True:
            await interaction.response.send_message(file=discord.File('defender drip.png'), ephemeral=True)
        else:
            await interaction.response.send_message(file=discord.File('defender drip.png'))
        await interaction.response.send_message(file=discord.File('defender drip.png'))

    @app_commands.command(name="kurukuru_leaderboard", description="Leaderboard for the Kurukuru reactions/replies")
    @app_commands.describe(invisible="Enabling this will only make the command visible for you (automatically off for #bot-commands")
    @app_commands.choices(stats=[
        discord.app_commands.Choice(name='Kurukuru Reaction #1', value=1),
        discord.app_commands.Choice(name='Kurukuru Reaction #2', value=2),
        discord.app_commands.Choice(name='Kurukuru Emote reply', value=3),
        discord.app_commands.Choice(name='Kurukuru GIF reply', value=4)])
    async def kurukuru_leaderboard(self, interaction: discord.Interaction, stats: discord.app_commands.Choice[int], invisible: bool = True):
        if interaction.guild.id in [570929677732937738, 993818190008287283]:
            embed = leaderboard(interaction.user.id, stats.value, lb_name=stats.name)
            if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
                await interaction.response.send_message(embed=embed)
            elif invisible is True:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("This only works in the official Days Bygone server.", ephemeral=True)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.channel.name == "counting-game" and message.guild.id == 570929677732937738:
            if message.author.id == 639599059036012605 and "ruined it" in message.content.lower():
                number = re.findall(r'^\D*(\d+)',str(message.content)[21:])[0]
                print(number)
                original_message = None

                if message.reference and isinstance(message.reference.resolved, discord.Message):
                    original_message = message.reference.resolved
                elif message.reference:
                    # Fallback if the message isn't cached
                    channel = message.channel
                    original_message = await channel.fetch_message(message.reference.message_id)


                update_counting_sheet(number, original_message.author.display_name, original_message.author.id, datetime.datetime.now(), str(original_message.content))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def alta_history(self, ctx):
        date = pytz.timezone("Europe/Bucharest").localize(datetime.datetime(2025, 2, 9, 23, 0))
        channel = self.bot.get_channel(1367130635801722972)
        utc_time = date.astimezone(pytz.utc)
        lista = []
        print(channel)

        async for message in channel.history(limit=None, after=utc_time, oldest_first=True):
            if message.author.id == 639599059036012605 and "ruined it" in message.content.lower():
                number = re.findall(r'^\D*(\d+)',str(message.content)[21:])[0]
                print(number)
                original_message = None

                try:
                    if message.reference and isinstance(message.reference.resolved, discord.Message):
                        original_message = message.reference.resolved
                    elif message.reference:
                        # Fallback if the message isn't cached
                        channel = message.channel
                        original_message = await channel.fetch_message(message.reference.message_id)
                except:
                    continue

                if not original_message:
                    continue

                lista.append([str(number), original_message.author.display_name, str(original_message.author.id), message.created_at.strftime("%d/%m/%Y %I:%M:%S %p"), str(original_message.content)])

        print(lista)
        update_with_matrix(lista)

    @stab.error
    @pet.error
    async def on_pet_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(str(error), ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
