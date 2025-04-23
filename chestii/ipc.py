import discord
from discord.ext import commands
from discord import app_commands
from grile import functie_babana
from random import randint

class IPC(commands.GroupCog, name="ipc"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="grile", description="grile la ipc idk")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def ipc_begin(self, interaction: discord.Interaction):
        global embed
        global question
        question = randint(1, 149)
        print(question)
        embed = functie_babana(question, 0)
        await interaction.response.send_message(view=Butoane(), embed=embed)


class Butoane(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="", style=discord.ButtonStyle.green, emoji="1️⃣")
    async def unu(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = functie_babana(question, 1)
        await interaction.response.edit_message(view=Butoane(), embed=embed)

    @discord.ui.button(label="", style=discord.ButtonStyle.green, emoji="2️⃣")
    async def doi(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = functie_babana(question, 2)
        await interaction.response.edit_message(view=Butoane(), embed=embed)

    @discord.ui.button(label="", style=discord.ButtonStyle.green, emoji="3️⃣")
    async def trei(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = functie_babana(question, 3)
        await interaction.response.edit_message(view=Butoane(), embed=embed)

    @discord.ui.button(label="", style=discord.ButtonStyle.red, emoji="⏭")
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        global question
        question = randint(1, 149)
        embed = functie_babana(question, 0)
        await interaction.response.edit_message(view=Butoane(), embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(IPC(bot), guild=discord.Object(id=993818190008287283))