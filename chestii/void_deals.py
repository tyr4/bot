import discord
from discord.ext import commands
from discord import app_commands

from datetime import datetime, timedelta, timezone
import requests
import json
import os

from void_deals_image_gen.image_gen import generate_image

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

def get_reset_date(start_date: datetime):
    date = start_date.astimezone(timezone.utc)

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

    # print(start_date, date)
    return format_date(date)

def get_void_deals(specific_date: datetime = None):
    if specific_date:
        formatted = get_deal_date(specific_date)
    else:
        formatted = format_date(get_last_reset_time())

    # print(formatted)

    response = call_api(
        {
          "domain": "void-deals",
          "options": { "voidDeals": { "date": formatted } }
        }
    )

    return response

def get_void_deals_next_hit(start_date: datetime, class_name: str, max_cost_per_unit: int):
    formatted = get_deal_date(start_date + timedelta(days=1))

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

def get_void_deals_next_x_raw(start_date: datetime, days):
    formatted = get_deal_date(start_date)

    response = call_api(
        {
            "domain": "void-deals-projection",
            "options": {
                "voidDealsProjection": {
                    "startDate": formatted,
                    "days": days,
                    "params": [
                        {
                            "id": "weaponcrate",
                            "className": "crate",
                            "rarity": ["common", "rare", "epic", "legendary", "perfect"],
                            "costPerUnitRange": {
                                "min": 150,
                                "max": 200
                            }
                        },
                        {
                            "id": "shardshigh",
                            "className": "ticketShard",
                            "amountBand": "high",
                            "rarity": ["common", "rare", "epic", "legendary", "perfect"],
                            "costPerUnitRange": {
                                "min": 150,
                                "max": 200
                            }
                        },
                        {
                            "id": "ticket",
                            "className": "ticket",
                            "rarity": ["common", "rare", "epic", "legendary", "perfect"],
                            "costPerUnitRange": {
                                "min": 200,
                                "max": 300
                            }
                        },
                        {
                            "id": "shardslow",
                            "className": "ticketShard",
                            "amountBand": "low",
                            "rarity": ["common", "rare", "epic", "legendary", "perfect"],
                            "costPerUnitRange": {
                                "min": 150,
                                "max": 200
                            }
                        }
                    ]
                }
            }
        }
    )

    return response

# def get_void_deals_projection(start_date: datetime, days: int):
#     formatted = get_deal_date(start_date)
#
#     response = call_api(
#         {
#             "domain": "void-deals-projection",
#             "options": {
#                 "voidDealsProjection": {
#                     "startDate": formatted,
#                     "days": days
#                 }
#             }
#         }
#     )
#
#     return response

def get_void_deals_basic_embed():
    embed = discord.Embed(title="Void Deals <a:kafkakurukuru:1118233531110412461>", color=0x71368a)
    embed.set_footer(text="Deals brought to you by Hommee",
                     icon_url="https://cdn.discordapp.com/emojis/1139252590278889529.gif")

    return embed

def class2emote(class_name: str):
    if class_name == "crate":
        return "<:Resource_voidCrate:969533015074160730>"
    else:
        return "<:Resource_voidTicket:969512352674353182>"

def cost_type2emote(class_name: str):
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

def rarity2emote(rarity):
    if rarity == "perfect":
        return "🟡🟡🟡"
    elif rarity == "legendary":
        return "🟡"
    elif rarity == "epic":
        return "🟣"
    elif rarity == "rare":
        return "🔵"
    else:
        return "⚪"

def get_next_deals_timestamp(date: datetime):
    today = date.astimezone(timezone.utc)
    reset_today = get_reset_date(today)

    if today < reset_today:
        return reset_today.timestamp()
    else:
        return (reset_today + timedelta(days=1)).timestamp()

def string2timestamp(formatted_date: str):
    return datetime.strptime(formatted_date, "%Y-%m-%d").replace(tzinfo=timezone.utc, hour=12).timestamp()

def build_embed_slot_field(embed, slot_count, slot: dict):
    slot_class = slot["className"]

    formatted = f"**x{slot['amount']} {class2name(slot_class)} {class2emote(slot_class)}**\n"
    formatted += f"**Cost:** {slot['cost']} {cost_type2emote(slot_class)}\n"

    if slot_class != "crate":
        formatted += f"**Rate:** {slot['costPerUnit']} {cost_type2emote(slot_class)}\n"

    embed.add_field(name=f"Slot {slot_count} {rarity2emote(slot['rarity'])}", value=formatted, inline=False)

def build_void_deals_ping():
    response = get_void_deals()
    slots = response['result']['slots']
    message = ''

    for slot in slots:
        message += class_and_cost2ping(slot["className"], slot["cost"])

    return message

def build_all_embed_slots(embed, slots: list, date: datetime, override_with_today_deals_date: bool = False):
    timestamp = get_next_deals_timestamp(date - timedelta(days=1)) if override_with_today_deals_date \
                else get_next_deals_timestamp(date)

    embed.add_field(name=f"Date: {format_date(date)}", value='', inline=False)

    # build_embed_slot_field(embed, 1, slots[0])
    # build_embed_slot_field(embed, 2, slots[1])
    # build_embed_slot_field(embed, 3, slots[2])

    image_path = generate_image(date)
    file = discord.File(image_path, filename="deals.png")

    embed.set_image(url="attachment://deals.png")
    embed.add_field(name=f"Next deals are <t:{timestamp:.0f}:R>", value='', inline=False)

    return file

def build_embed_today_deals():
    response = get_void_deals()
    embed = get_void_deals_basic_embed()
    slots = response['result']['slots']

    file = build_all_embed_slots(embed, slots, get_last_reset_time())

    return embed, file

def build_embed_pinned_message():
    embed, file = build_embed_today_deals()
    next_perfect_crate = get_void_deals_next_hit(datetime.now(), 'crate', 150)
    next_perfect_ticket_shard = get_void_deals_next_hit(datetime.now(), 'ticketShard', 150)
    next_perfect_ticket = get_void_deals_next_hit(datetime.now(), 'ticket', 200)

    crate_timestamp = string2timestamp(next_perfect_crate['result']['deal']['date'])
    ticket_shard_timestamp = string2timestamp(next_perfect_ticket_shard['result']['deal']['date'])
    ticket_timestamp = string2timestamp(next_perfect_ticket['result']['deal']['date'])

    formatted = f"**Next perfect {class2emote('crate')} is <t:{crate_timestamp:.0f}:R>**\n"
    formatted += f'**Next perfect {class2emote('ticketShard')} {cost_type2emote('ticketShard')} is <t:{ticket_shard_timestamp:.0f}:R>**\n'
    formatted += f'**Next perfect {class2emote('ticket')} {cost_type2emote('ticket')} is <t:{ticket_timestamp:.0f}:R>**'

    embed.add_field(name='', value=formatted, inline=False)

    return embed, file

def build_embed_next_hit_deals(class_name, max_cost_per_unit):
    response = get_void_deals_next_hit(datetime.now(), class_name, max_cost_per_unit)
    embed = get_void_deals_basic_embed()
    # print(response)

    if response['result']['deal'] is None:
        embed.add_field(name="No deals found for this price!", value='', inline=False)
        return embed

    date = datetime.strptime(response['result']['deal']['date'], "%Y-%m-%d").replace(tzinfo=timezone.utc, hour=12)
    print(date)

    full_deals = get_void_deals(date)
    slots = [slot for slot in full_deals['result']['slots']]

    file = build_all_embed_slots(embed, slots, date, override_with_today_deals_date=True)

    return embed, file

def build_embed_projection_deals(days, shard_ratio_threshold, buy_ticket_to_ticket):
    response = get_void_deals_next_x_raw(datetime.now(), days)
    embed = get_void_deals_basic_embed()

    spent_shard_sum = 0
    spent_ticket_sum = 0
    gained_ticket_shard_sum = 0
    gained_ticket_to_ticket_sum = 0

    if days <= 0:
        embed.add_field(name="Error", value='Days must be a positive value!', inline=False)
        return embed
    elif days >= 365:
        embed.add_field(name="Error", value='Days must be below 365!', inline=False)
        return embed

    # skip crate deals
    for i in range(1, 3):
        projection = response['result']['projections'][i]
        deals = projection['deals']

        for deal in deals:
            if deal['className'] == 'ticketShard':
                if deal['costPerUnit'] <= shard_ratio_threshold:
                    spent_shard_sum += deal['cost']
                    gained_ticket_shard_sum += deal['amount']

            elif deal['className'] == 'ticket' and buy_ticket_to_ticket:
                spent_ticket_sum += deal['cost']
                gained_ticket_to_ticket_sum += deal['amount']

    embed.add_field(name=f"Day period: {days} days\nMaximum Shard Ratio: {shard_ratio_threshold:.2f}\n"
                         f"Buying all Ticket to Ticket Deals: {'Yes' if buy_ticket_to_ticket else 'No'}", value='', inline=False)

    formatted_void_shards = (f"+{gained_ticket_shard_sum} Void Tickets {class2emote('ticketShard')}\n"
                             f"-{spent_shard_sum} Void Shards {cost_type2emote('ticketShard')}")
    embed.add_field(name=f"Type: {class2emote('ticketShard')} {cost_type2emote('ticketShard')}", value=formatted_void_shards, inline=False)

    if buy_ticket_to_ticket:
        formatted_tickets = (f"+{gained_ticket_to_ticket_sum} Void Tickets {class2emote('ticketShard')}\n"
                                 f"-{spent_ticket_sum} Tickets {cost_type2emote('ticket')}")
        embed.add_field(name=f"Type: {class2emote('ticketShard')} {cost_type2emote('ticket')}",
                        value=formatted_tickets, inline=False)

    embed.add_field(name=f"~~                                                                              ~~\n"
                         f"__Total Void Tickets Gained: **{gained_ticket_to_ticket_sum + gained_ticket_shard_sum}**__ {class2emote('ticketShard')} ",
                    value='', inline=False)

    return embed

class VoidDeals(commands.GroupCog, name="void_deals"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="today", description="Sends today's void deals")
    async def void_deals_today(self, interaction: discord.Interaction, invisible: bool = True):
        if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
            await interaction.response.defer()
        elif invisible is True:
            await interaction.response.defer(ephemeral=True)
        else:
            await interaction.response.defer()

        embed, file = build_embed_today_deals()

        await interaction.followup.send(embed=embed, file=file)

    @app_commands.command(name="next_hit", description="Sends the deals for the day that matches your specified criteria")
    @app_commands.choices(deal_type=[
        discord.app_commands.Choice(name="Void Crate", value='crate'),
        discord.app_commands.Choice(name="Void Ticket to Ticket", value='ticket'),
        discord.app_commands.Choice(name="Void Ticket to Shards", value='ticketShard'),
    ])
    @app_commands.describe(deal_type="The desired deal type")
    @app_commands.describe(maximum_price_per_unit="Crate cost range: 150-190, Ticket to Ticket cost range: 200-300, Ticket to Shard cost range: 150-200")
    async def void_deals_next_hit(self, interaction: discord.Interaction, deal_type: discord.app_commands.Choice[str],
                                  maximum_price_per_unit: int, invisible: bool = True):
        if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
            await interaction.response.defer()
        elif invisible is True:
            await interaction.response.defer(ephemeral=True)
        else:
            await interaction.response.defer()

        embed, file = build_embed_next_hit_deals(deal_type.value, maximum_price_per_unit)

        await interaction.followup.send(embed=embed, file=file)

    @app_commands.command(name="projection", description="Sends the amount of Void Tickets you can get in a timeframe. Shards not supported")
    @app_commands.describe(day_period="The amount of days to sum up deals for. Value range is 1-365 days.")
    async def void_deals_projection(self, interaction: discord.Interaction, day_period: int, max_shard_ratio: float,
                                    buy_ticket_to_ticket: bool, invisible: bool = True):
        if interaction.channel.name in ["bot", "amogus-testing", "bot-commands"]:
            await interaction.response.defer()
        elif invisible is True:
            await interaction.response.defer(ephemeral=True)
        else:
            await interaction.response.defer()

        embed = build_embed_projection_deals(day_period, max_shard_ratio, buy_ticket_to_ticket)

        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(VoidDeals(bot))


#
# print(gained_ticket_sum, spent_shard_sum, spent_ticket_sum)

# print(get_void_deals_next_hit(datetime.now(), 'crate', 150))
# print(get_void_deals_next_x_raw(datetime.now(), 10))