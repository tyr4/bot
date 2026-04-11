import discord
from discord.ext import commands
from discord import app_commands
import json

with open("rage_json.json", 'r+') as json_file:
        idk = json.load(json_file)

async def update_rage(user_id, user_name):
    global idk
    with open("rage_json.json", 'r+') as json_file:
        data = json.load(json_file)
        if user_id not in data:
            data[user_id] = {'counter': 1, 'name': user_name}
        else:
            data[user_id]['counter'] += 1
        json_file.seek(0)
        json.dump(data, json_file, indent=4)

        idk = data
        return data[user_id]['counter']

class Rage(commands.GroupCog, name="rage"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="la_ceva", description="bagi ceva in viata idk")
    async def semafor(self, interaction: discord.Interaction, text: str):
        count = await update_rage(str(interaction.user.id), interaction.user.name)
        embed = discord.Embed(title=f"{interaction.user.display_name} spune...", color=0x71368a)
        embed.add_field(name="", value=text)

        await interaction.response.send_message(f"\n\nAi dat rage de {count} ori, bravo coaie", embed=embed)


    @app_commands.command(name="leaderboard", description="bagi ceva in semafor idk")
    async def rage_leaderboard(self, interaction: discord.Interaction):
        global idk
        embed = discord.Embed(title=f"Wooo Leaderboard", color=0x71368a)
        sorted_data = sorted(idk.items(), key=lambda x: x[1]['counter'], reverse=True)
        for key, value in sorted_data:
            embed.add_field(name="", value=f"<@{key}> --- {value['counter']} ori total", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Rage(bot), guild=discord.Object(id=1030490217855074304))
