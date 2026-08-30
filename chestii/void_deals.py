import discord
from discord.ext import commands
from discord import app_commands

from datetime import datetime, timedelta, timezone
import requests
import json
import os

url = "https://jxjshswlabnmkxhyhbdx.supabase.co/functions/v1/sandbox"
STATE_FILE = "void_deals_state.json"

def load_state() -> dict:
    if not os.path.exists(STATE_FILE):
        return {"last_reset": None, "sent": False}

    with open(STATE_FILE) as f:
        try:
            loaded = json.load(f)
        except json.JSONDecodeError:
            return {"last_reset": None, "sent": False}

    return {
        "last_reset": loaded.get("last_reset"),
        "sent": loaded.get("sent", False)
    }

def save_state(state: dict) -> None:
    temp_path = f"{STATE_FILE}.tmp"

    with open(temp_path, "w") as f:
        json.dump(state, f, indent=4)

    os.replace(temp_path, STATE_FILE)

def should_send_deals_today() -> bool:
    current_reset = get_last_reset_time()
    state = load_state()

    stored_reset = (
        datetime.fromisoformat(state["last_reset"])
        if state["last_reset"] else None
    )

    # a new reset window has started since we last checked -> flag resets itself
    if stored_reset != current_reset:
        state = {"last_reset": current_reset.isoformat(), "sent": False}

    if state["sent"]:
        save_state(state)
        return False

    state["sent"] = True
    save_state(state)

    return True

def get_last_reset_time() -> datetime:
    now = datetime.now(timezone.utc)
    reset_today = now.replace(hour=12, minute=0, second=0, microsecond=0)

    if now < reset_today:
        return reset_today - timedelta(days=1)

    return reset_today

def get_reset_date():
    date = datetime.now(timezone.utc)

    return date.replace(hour=12, minute=0, second=0, microsecond=0)

def format_date(date):
    return date.strftime("%Y-%m-%d")

def call_api(payload):
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()

    return response.json()

def get_deal_date(start_date: datetime = None):
    if start_date is None:
        start_date = datetime.now(timezone.utc)

    start_date = start_date.astimezone(timezone.utc)
    if start_date.hour < 12:
        date = start_date - timedelta(days=1)
    else:
        date = start_date

    print(start_date, date)
    return format_date(date)

def get_void_deals():
    formatted = format_date(get_last_reset_time())
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

def class_and_cost2ping(class_name: str, cost: int):
    if cost == 150:
        if class_name == "crate":
            return '<@&1257074975509053544> '
        elif class_name == "ticketShard":
            return '<@&1199972145581789196> '

    return ''

def class_and_cost2rarity(slot: dict):
    class_name = slot['className']
    cost = slot['costPerUnit']

    print(class_name, cost)

    if class_name == "crate":
        cost = slot['cost'] # small api bug

        if 150 <= cost <= 160:
            return "🟡"
        elif cost == 170:
            return "🟣"
        elif cost == 180:
            return "🔵"
        elif cost == 190:
            return "⚪"

    elif class_name == "ticket":
        if 200 <= cost < 226:
            return "🟡"
        elif 226 <= cost <= 250:
            return "🟣"
        elif 251 <= cost <= 276:
            return "🔵"
        elif 276 < cost:
            return "⚪"

    elif class_name == "ticketShard":
        if 150 <= cost < 163:
            return "🟡"
        elif 163 <= cost <= 176:
            return "🟣"
        elif 176 <= cost <= 188:
            return "🔵"
        elif 188 < cost:
            return "⚪"

    return ''

def get_next_deals_timestamp():
    today = datetime.now(timezone.utc)
    reset_today = get_reset_date()

    if today < reset_today:
        return reset_today.timestamp()
    else:
        return (reset_today + timedelta(days=1)).timestamp()


def build_embed_slot_field(embed, slot_count, slot: dict):
    slot_class = slot["className"]

    formatted = f"**x{slot['amount']} {class2name(slot_class)} {class2emote(slot_class)}**\n"
    formatted += f"**Cost:** {slot['cost']} {cost2emote(slot_class)}\n"

    if slot_class != "crate":
        formatted += f"**Rate:** {slot['costPerUnit']} {cost2emote(slot_class)}\n"

    embed.add_field(name=f"Slot {slot_count} {class_and_cost2rarity(slot)}", value=formatted, inline=False)

def build_void_deals_ping():
    response = get_void_deals()
    slots = response['result']['slots']
    message = ''

    for slot in slots:
        message += class_and_cost2ping(slot["className"], slot["cost"])

    return message

def build_all_embed_slots(embed, slots: list, date: datetime):
    tomorrow_timestamp = get_next_deals_timestamp()
    embed.add_field(name=f"Date: {format_date(date)}", value='', inline=False)

    build_embed_slot_field(embed, 1, slots[0])
    build_embed_slot_field(embed, 2, slots[1])
    build_embed_slot_field(embed, 3, slots[2])

    embed.add_field(name=f"Next deals are <t:{tomorrow_timestamp:.0f}:R>", value='', inline=False)

def build_embed_today_deals():
    response = get_void_deals()
    embed = get_void_deals_basic_embed()
    slots = response['result']['slots']

    build_all_embed_slots(embed, slots, get_last_reset_time())

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

rez = get_deal_date(datetime.now())
print(rez)