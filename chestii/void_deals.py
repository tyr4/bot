import discord
from discord.app_commands import describe
from discord.ext import commands
from discord import app_commands

from datetime import datetime, timedelta, timezone
import requests

url = "https://jxjshswlabnmkxhyhbdx.supabase.co/functions/v1/sandbox"
types = ["crate", "ticketShard", "ticket"]

def format_date(date):
    return date.strftime("%Y-%m-%d")

def call_api(payload):
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()

    return response.json()

def get_deal_date(start_date: datetime = None):
    if start_date is None:
        start_date = datetime.now(timezone.utc)

    if start_date.hour < 12:
        date = start_date - timedelta(days=1)
    else:
        date = start_date

    return format_date(date)

def get_void_deals(date: datetime):
    formatted = get_deal_date(date)
    print(formatted)

    response = call_api(
        {
          "domain": "void-deals",
          "options": { "voidDeals": { "date": formatted } }
        }
    )

    return response

def get_void_deals_next(start_date: datetime, class_name: str, max_cost_per_unit: int):
    formatted = get_deal_date(start_date)

    response = call_api(
        {
            "domain": "void-deals-next",
            "options": {
                "voidDealsNext": {
                    "startDate": formatted,
                    "className": class_name,
                    "maxCostPerUnit": max_cost_per_unit
                }
            }
        }
    )

    return response

def get_void_deals_projection(start_date: datetime, days: int):
    formatted = get_deal_date(start_date)

    response = call_api(
        {
            "domain": "void-deals-projection",
            "options": {
                "voidDealsProjection": {
                    "startDate": formatted,
                    "days": days
                }
            }
        }
    )

    return response

def get_void_deals_basic_embed():
    embed = discord.Embed(title="Void Deals <a:kafkakurukuru:1118233531110412461>", color=0x71368a)
    embed.set_footer(text="If you spot any issues with this bot, please ping '@_tyrael.'",
                     icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")

    return embed

def class2emote(class_name: str):
    if class_name == "crate":
        return "<:Resource_voidCrate:969533015074160730>"
    else:
        return "<:Resource_voidTicket:969512352674353182>"

def cost2emote(class_name: str):
    if class_name == "crate":
        return "<:Resource_crate:1167984753513873428>"
    elif class_name == "ticketShard":
        return "<:Resource_voidShard:969532979594551336>"
    elif class_name == "ticket":
        return "<:Resource_ticket:1137471573113176154>"

    return "not found idk"

def class2name(class_name: str):
    if class_name == "crate":
        return "Void Crate"
    else:
        return "Void Tickets"

def get_next_deals_timestamp():
    today = datetime.now(timezone.utc)
    reset_today = today.replace(hour=12, minute=0, second=0, microsecond=0)

    if today < reset_today:
        return reset_today.timestamp()
    else:
        return (reset_today + timedelta(days=1)).timestamp()


def build_embed_slot_field(embed, slot_count, slot: dict):
    slot_class = slot["className"]

    formatted = f"**x{slot['amount']} {class2name(slot_class)} {class2emote(slot_class)}**\n"
    formatted += f"**Cost:** {slot['cost']} {cost2emote(slot_class)}\n"

    if slot_class != "crate":
        formatted += f"\n**Rate:** {slot['costPerUnit']} {cost2emote(slot_class)}\n"

    embed.add_field(name=f"Slot {slot_count}", value=formatted, inline=False)

def build_all_embed_slots(embed, slots: list, date: datetime):
    tomorrow_timestamp = get_next_deals_timestamp()
    embed.add_field(name=f"Date: {format_date(date)}", value='', inline=False)

    build_embed_slot_field(embed, 1, slots[0])
    build_embed_slot_field(embed, 2, slots[1])
    build_embed_slot_field(embed, 3, slots[2])

    embed.add_field(name=f"Next deals are in <t:{tomorrow_timestamp:.0f}:R>", value='', inline=False)

def build_embed_today_deals():
    response = get_void_deals(datetime.now())
    embed = get_void_deals_basic_embed()
    slots = response['result']['slots']

    build_all_embed_slots(embed, slots, datetime.now())

    return embed

class VoidDeals(commands.GroupCog, name="void_deals"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="today", description="Sends today's void deals")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def void_deals_today(self, interaction: discord.Interaction,):
        embed = build_embed_today_deals()

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(VoidDeals(bot))