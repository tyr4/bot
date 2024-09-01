import discord
from discord.ext import commands
from discord import app_commands

import os
import gspread
from google.oauth2.service_account import Credentials
import csv


def update_csv():
    # Path to your service account key file
    SERVICE_ACCOUNT_FILE = '../google_sheets_api_key.json'

    # Define the scope
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # Authenticate using the service account key
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Use gspread to access the Google Sheets API
    gc = gspread.authorize(creds)

    # Open the Google Sheet by its title or URL
    sheet = gc.open_by_key("1SO-E5YBBvrW_k_eI3_vz6Mk3ubEVT5varq6163_B72s")
    worksheet = sheet.worksheet('MobData')


    # Example: Read data from the first row
    all_values = worksheet.get_all_values()
    ceva = ''
    last = 0
    for i, row in enumerate(all_values, start=1):
        if row[1] == '' and i >= 3:
            break
        elif i >= 3:
            ceva += f"{row[0]},{row[1]},{row[2]}\n"
        last = row[0]

    with open('/ceva.csv', 'w+') as csv_file:
        csv_file.truncate()
        csv_file.write(ceva)

    return last


class Sheet(commands.GroupCog, name="sheet"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="update", description="Updates the Rewind sheet mob data (only works for me and Fishy)")
    async def sheet_update(self, interaction: discord.Interaction) -> None:
        if interaction.user.id in [556836294710525952, 586711955880935438]:
            await interaction.response.defer(ephemeral=True)
            try:
                last = update_csv()
                await interaction.followup.send(f"Maximum day: {last}")
            except Exception as e:
                await interaction.followup.send(f"i cant code: {e}")
        else:
            await interaction.response.send_message('Just ignore this command :)', ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Sheet(bot))

update_csv()