import discord
from discord.ext import commands
from discord import app_commands

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slash commands up")

    @commands.command()
    async def angel(self, ctx, *, arg):
        print(arg)
        await ctx.message.delete()
        await ctx.channel.send(arg)
    
    @app_commands.command(name="ping", description="funniest ping in the east")
    async def ping(self, interaction: discord.Interaction):
        bot_latency = round(self.client.latency * 1000)
        await interaction.response.send_message(f"Pong! {bot_latency} ms.")


async def setup(client):
    await client.add_cog(Slash(client))