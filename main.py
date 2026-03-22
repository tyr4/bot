import asyncio
import os

import discord
from typing import Literal, Optional
from discord.ext import commands
from discord.ext.commands import Greedy, Context
import logging

from chestii.shopping_list import AddButton

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents, help_command=None)
discord.utils.setup_logging(level=logging.INFO, root=False)

@bot.command()
@commands.is_owner()
async def server_info(ctx):
    guilds = ""
    for guild in bot.guilds:
        guilds += f"{guild.name}\n"
        await asyncio.sleep(1)
    await ctx.reply(guilds, mention_author=False)

@bot.command()
@commands.guild_only()
async def sync(
  ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if ctx.author.id == 556836294710525952:
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
    else:
        await ctx.send("Stop syncing idiot")


@bot.event
async def on_ready():
    # with open ("avatar2.gif", "rb") as avatar:
    #     await bot.user.edit(avatar=avatar.read())
    print(f'{bot.user} has awoken')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="kurukuru"))

    bot.add_view(AddButton())
    print("ඞ")


async def load_extensions():
    for filename in os.listdir("chestii"):
        if filename.endswith(".py"):
            await bot.load_extension(f"chestii.{filename[:-3]}")
            print(f"{filename[:-3].title()} loaded!")


async def amogus():
    await load_extensions()
    bot.tree.copy_global_to(guild=discord.Object(id=993818190008287283))
    await bot.start(os.environ["TOKEN"])

asyncio.run(amogus())
