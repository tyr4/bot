import asyncio
import os

import discord
from typing import Literal, Optional
from discord.ext import commands
from discord.ext.commands import Greedy, Context

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all(), help_command=None)


@bot.command()
@commands.is_owner()
async def server_info(ctx):
    guilds = ""
    for guild in bot.guilds:
        guilds += f"{guild.name}\n"
    await ctx.reply(guilds, mention_author=False)


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


@bot.event
async def on_ready():
    print(f'{bot.user} has awoken')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="you crying"))
    print("Streaming Amogus")


async def load_extensions():
    for filename in os.listdir("./chestii"):
        if filename.endswith(".py"):
            await bot.load_extension(f"chestii.{filename[:-3]}")
            print(f"{filename[:-3].title()} loaded!")


async def amogus():
    await load_extensions()
    bot.tree.copy_global_to(guild=discord.Object(id=993818190008287283))
    await bot.start("ඞ")

asyncio.run(amogus())
