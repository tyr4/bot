import discord
from discord.ext import commands
from discord import app_commands

class ListModal(discord.ui.Modal, title="ceva"):
    def __init__(self, default_text: str, message: discord.Message):
        super().__init__(title="ceva")

        self.message = message

        self.feedback = discord.ui.TextInput(
            label="Your a",
            style=discord.TextStyle.paragraph,
            placeholder="Type something here...",
            default=default_text,
            required=True,
            max_length=500
        )

        self.add_item(self.feedback)

    async def on_submit(self, interaction: discord.Interaction):
        await self.message.edit(content=self.feedback.value)

        await interaction.response.send_message(f"Updated", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message("esti prost", ephemeral=True)

        raise error

class AddButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.green, custom_id="edit_shopping_list")
    async def edit_shopping_list( self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message.content

        await interaction.response.send_modal(ListModal(default_text=message, message=interaction.message))

class ShoppingList(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="init", description="init message")
    async def init_shopping_list(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="ceva placeholder", view=AddButton())

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ShoppingList(bot), guild=discord.Object(id=1030490217855074304))