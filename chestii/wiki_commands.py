import asyncio
import re

import discord
import requests
from discord.ext import commands
from discord import app_commands
from rapidfuzz import process, fuzz

from chestii.sheet import get_event_week_data
from chestii.wrapped import update_wrapped_data

WIKI_URL = "https://daysbygone.wiki.gg/wiki"
PAGE_LIST_URL = "https://daysbygone.wiki.gg/api.php?action=query&list=allpages&aplimit=500&format=json"
PAGE_ANCHORS_URL = "https://daysbygone.wiki.gg/api.php?action=parse&prop=sections&format=json&page=REPLACEME"
headers = {"User-Agent": "Silwuf/1.0 (User:Tyrael; cevamail@gmail.com)"}
REPLACE_TOKEN = "REPLACEME"
MATCH_THRESHOLD = 70

def get_page_list_json():
    response = requests.get(PAGE_LIST_URL, headers=headers)

    return response.json()

def get_page_list():
    response = get_page_list_json()
    all_pages = []
    exclusion_list = ["days bygone - castle defense wiki",
                    "days bygone - castle defense wiki/about",
                    "days bygone - castle defense wiki/contribute",
                    "days bygone - castle defense wiki/external",
                    "days bygone - castle defense wiki/pages",
                    "days bygone - castle defense wiki/welcome",
                    "example character",
                    "multiinfobox/core",
                    ]

    for page in response['query']['allpages']:
        name = page['title']

        if name.lower() not in exclusion_list:
            all_pages.append(name)

    return all_pages

def get_page_anchors_json(parent_page):
    full_url = PAGE_ANCHORS_URL.replace(REPLACE_TOKEN, parent_page)
    response = requests.get(full_url, headers=headers)

    return response.json()

def get_page_anchors(parent_page):
    response = get_page_anchors_json(parent_page)
    results = []

    for anchor in response['parse']['sections']:
        results.append(anchor['anchor'])

    return results

def command_to_page_matcher(command: str):
    all_pages = get_page_list()
    lookup = {p.lower(): p for p in all_pages}
    choices = list(lookup.keys())

    results = process.extract(command.lower(), choices, scorer=fuzz.WRatio, limit=5)
    if results[0][1] < MATCH_THRESHOLD:
        return []

    return [(lookup[match], score, idx) for match, score, idx in results]

def command_to_page_anchor_matcher(command: list[str], parent_page: str | None = None):
    if len(command) != 2:
        return []

    pages = command_to_page_matcher(command[0])

    if not pages:
        return []

    best_match = pages[0][0]
    page_anchors = get_page_anchors(best_match)

    if not page_anchors:
        return pages

    lookup = {p.lower(): p for p in page_anchors}
    choices = list(lookup.keys())

    results = process.extract(command[1].lower(), choices, scorer=fuzz.WRatio, limit=5)
    if results[0][1] < MATCH_THRESHOLD:
        return pages

    return [pages[0], [(lookup[match], score, idx) for match, score, idx in results]]

async def parse_message(message: discord.Message):
    exclusion_list = [
        "evl",
        "tyr",
        "death",
        "rateup",
        "darksheet",
        "events",
        "wtcalc",
        "halloween",
        "mammoths",
        "deals"
    ]

    pattern = r"[?#]\S+(?:\s+\S+)?"
    for match in re.finditer(pattern, message.content): # change to message.content
        raw = match.group(0)
        raw_list = raw.split()
        skip_command = False

        for exclusion in exclusion_list:
            if exclusion in raw_list:
                skip_command = True
                break

        if skip_command:
            continue

        no_prefix_list = raw.lstrip("?#").split()

        print(raw)

        if len(no_prefix_list) == 2:
            result = command_to_page_anchor_matcher(no_prefix_list)
        else:
            result = command_to_page_matcher(no_prefix_list[0])

        if not result:
            continue

        url = build_wiki_link(result)
        await send_message(message, url, result)

def build_wiki_link(result):
    parent_page = result[0]
    anchor = None

    if len(result) == 2:
        anchor = result[1]

    fixed_parent = parent_page[0].replace(" ", "_")
    best_anchor = anchor[0][0] if anchor else ''

    page_link = f"{WIKI_URL}/{fixed_parent}#{best_anchor}"

    return page_link

async def send_message(message, url, result):
    if not result:
        return

    if len(result) == 2:
        formatted = f"[{result[0][0]} -> {result[1][0][0].replace("_", " ")}](<{url}>)"
    else:
        formatted = f"[{result[0][0]}](<{url}>)"

    await message.reply(formatted, mention_author=False)

class WikiCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in [1100716645875466270, 1135983715646976111]:
            return
        if message.guild.id not in [570929677732937738, 993818190008287283, 1507129472682426459]:
            return

        message_lower = message.content.lower()

        if "?gala" in message_lower:
            await message.reply(
                f"An updated gala for players at 0-36k like <@977660878080057344> and me: [THE NEW GALA](<https://docs.google.com/document/d/1ZBD3OQuU0kuBt3L-s7zq__QWxjnge1meVs5B_nke9nM/edit?tab=t.0>)\n\n"
                "If you only want to use the command for yourself, you can use it in <#699337693238263900> or find the link in <#637933543699513367>",
                mention_author=False)
            await update_wrapped_data("?gala", username=message.author.name, user_id=message.author.id)

        if "?evl" in message_lower:
            await message.reply(
                f"An updated evl for players at 0-36k like <@553194887701331969> and me: [THE NEW EVL](<https://docs.google.com/document/d/1ZBD3OQuU0kuBt3L-s7zq__QWxjnge1meVs5B_nke9nM/edit?tab=t.0>)\n\n"
                "If you only want to use the command for yourself, you can use it in <#699337693238263900> or find the link in <#637933543699513367>")
            await update_wrapped_data("?evl", username=message.author.name, user_id=message.author.id)

        if "?cyber" in message_lower:
            await message.reply(f"DBG Site with most sheets/formulas: https://dbg-calculator.vercel.app",
                                mention_author=False)
            await update_wrapped_data("?cyber", username=message.author.name, user_id=message.author.id)

        if "?tyr" in message_lower:
            await message.reply(
                "Updated Optimal Rewind Calculator with stats calculations: <https://docs.google.com/spreadsheets/d/1ChZHbUy914-4r9vvcjviKCUfBqnJKiUvpnsG321XoWM/edit?gid=0#gid=0>",
                mention_author=False)
            await update_wrapped_data("?tyr", username=message.author.name, user_id=message.author.id)

        if "?death" in message_lower:
            await message.channel.send("<@674287880981708821> Hi hi hello")

            await asyncio.sleep(6)

            await message.channel.send("<@674287880981708821> Once more for good measure")

            await update_wrapped_data("?death", username=message.author.name, user_id=message.author.id)

        if "?darksheet" in message_lower:
            await message.reply(
                "You can find all Dark Tome buff values and costs here: <https://docs.google.com/spreadsheets/d/1Q1c3qUT74m3kT6ePJOm-Nib05v7I1Ua5AB9XdKn6HME/edit?gid=0#gid=0>",
                mention_author=False)
            await update_wrapped_data("?darksheet", username=message.author.name, user_id=message.author.id)

        if "?events" in message_lower:
            embed = get_event_week_data()

            await message.reply(mention_author=False, embed=embed)
            await update_wrapped_data("?events", username=message.author.name, user_id=message.author.id)

        if "?wtcalc" in message_lower:
            text = "<:WT_Apple:1019750592001867867> **[World Tree Calculator](<https://docs.google.com/spreadsheets/d/1A-J5gifZtwgBL1_WzR9eXIM4InxccwyIc5f998ZPKXM/edit?gid=548764124#gid=548764124>)** <:WT_Apple:1019750592001867867>  /  *[[Alternative Calc in Browser]](https://dbg-calculator.vercel.app/pages/worldtree.html)*\n" \
                   "Use this to figure out where to invest your apples for the most optimal days of damage & Monarch's WT Planner to plan out your next World Tree Build! \n" \
                   "(short guide on how to use it here: https://discord.com/channels/570929677732937738/1191279847427817482/1458890737193193688) \n" \
                   "-# Don't forget you have to make a copy! If you're on phone, you have to download the Google Sheets app"

            await message.reply(text, mention_author=False)
            await update_wrapped_data("?wtcalc", username=message.author.name, user_id=message.author.id)

        if "?halloween" in message_lower:
            await message.reply(
                "Halloween Event Boss Team: <:Hero_DarkMerlin:703020537089097789> <:Hero_Mikhail:703033570402238495> <:Hero_Max:703017718835838997> <:Hero_Dewitt:703020422005915658> <:Hero_Saul:977594194988236861> <:Hero_Garp:729434017296023675> (decent for all difficulties)\n" \
                "For Insane, 15* <:Hero_DarkMerlin:703020537089097789> is required", mention_author=False)
            await update_wrapped_data("?halloween", username=message.author.name, user_id=message.author.id)

        if "?mammoths" in message_lower:
            if message.author.id != 954082451762847746:
                await message.reply("https://tenor.com/view/woolly-mammoth-aio-ai-vi!deo-gif-2546557529878141509",
                                    mention_author=False)
                await update_wrapped_data("?mammoths", username=message.author.name, user_id=message.author.id)

        response = await parse_message(message)
        print(response)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(WikiCommands(bot))

# print(parse_message("wow cool ?text and wowowoww cool ?stuff text ?skills but maybe ?daryon pros"))