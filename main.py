import discord
from discord.ext import commands

import os
import asyncio

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f'{client.user} has awoken')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="you crying"))
    print("Streaming Amogus")
    await client.tree.sync()
    print("copacu gata sefu")


async def load_extensions():
    for filename in os.listdir("./chestii"):
        if filename.endswith(".py"):
            await client.load_extension(f"chestii.{filename[:-3]}")
            print("ඞ")


async def amogus():
    await load_extensions()
    await client.start("MTEzNTk4MzcxNTY0Njk3NjExMQ.GskQxz.x2ZkVeaBP1soZDVkfG9wz0TsiyXVyWqj1bU-tY")

asyncio.run(amogus())
