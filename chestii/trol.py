import discord
from discord.ext import commands
from discord import app_commands


class Trol(commands.GroupCog, name="trol"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="say", description="Send a message as the bot or something idk")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def mesaj(self, interaction: discord.Interaction, text: str, channel: str, reply: str = None):
        channel = int(channel)
        canal = self.bot.get_channel(channel)
        if reply:
            reply = int(reply)
            message_to_reply = await canal.fetch_message(reply)
            await canal.send(text, reference=message_to_reply, mention_author=False)
        elif not reply:
            await canal.send(text)

        await interaction.response.send_message("ok", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Trol(bot), guild=discord.Object(id=993818190008287283))