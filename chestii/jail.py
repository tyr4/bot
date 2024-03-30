import discord
from discord.ext import commands
from discord import app_commands

jailtime = True
ceva_id = []
name_list = []


class Jail(commands.GroupCog, name="jail"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="activate", description="Activate/deactivate jail or something idk")
    @app_commands.default_permissions(administrator=True)
    async def jailactivate(self, interaction: discord.Interaction):
        global jailtime
        if jailtime:
            jailtime = False
            await interaction.response.send_message("Deactivated jailtime!")
        else:
            jailtime = True
            await interaction.response.send_message("Activated jailtime!")

    @app_commands.command(name="add", description="Add someone to jail or something idk")
    @app_commands.default_permissions(administrator=True)
    async def jailadd(self, interaction: discord.Interaction, user: discord.Member):
        if user.id in [556836294710525952, 1135983715646976111]:
            await interaction.response.send_message("You don't have something better to do?", ephemeral=True)
        elif user.id not in ceva_id:
            ceva_id.append(user.id)
            if user.name not in name_list:
                name_list.append(user.name)
            await interaction.response.send_message(f"Added **{user.name}** to the jail list! <:PeepoNote:802224247098572810>")
        else:
            await interaction.response.send_message("It's already in there you dummmy")

    @app_commands.command(name="list", description="List of jailed people or something idk")
    async def list(self, interaction: discord.Interaction):
        ceva = ''
        if name_list:
            for name in name_list:
                ceva += name
                ceva += '\n'
            await interaction.response.send_message(ceva)
        else:
            await interaction.response.send_message("Jail empty idiot")

    @app_commands.command(name="clear", description="Clears the jail list or something idk")
    @app_commands.default_permissions(administrator=True)
    async def clear(self, interaction: discord.Interaction):
        global name_list
        global ceva_id
        if ceva_id:
            name_list = []
            ceva_id = []
            await interaction.response.send_message("Jail cleared!")
        else:
            await interaction.response.send_message("Jail already empty idiot")

    @app_commands.command(name="remove", description="Removes someone jail list or something idk")
    @app_commands.default_permissions(administrator=True)
    async def remove(self, interaction: discord.Interaction, user: discord.User):
        if user.id in ceva_id:
            ceva_id.remove(user.id)
            name_list.remove(user.name)
            await interaction.response.send_message(f"Removed **{user.name}** from the jail list!")
        else:
            await interaction.response.send_message("It's not in there you dummy")

    @app_commands.command(name="status", description="Says whether jail is on/off or something idk")
    @app_commands.default_permissions(administrator=True)
    async def status(self, interaction: discord.Interaction):
        if jailtime:
            await interaction.response.send_message("Jail is currently **activated**!")
        else:
            await interaction.response.send_message("Jail is currently **deactivated**!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Jail(bot), guild=discord.Object(id=993818190008287283))
