import pathlib

import discord
from discord.ext import commands
from discord import app_commands

import json

def load_wrapped_data():
    global wrapped_data

    current_file = pathlib.Path(__file__).resolve()
    print(current_file)

    with open('wrapped.json', 'r+') as json_file:
        wrapped_data = json.load(json_file)

    return wrapped_data

def save_wrapped_data():
    current_file = pathlib.Path(__file__).resolve()
    print(current_file)
    path = pathlib.Path("wrapped.json")
    tmp = path.with_suffix(".tmp")

    with tmp.open("w") as f:
        f.seek(0)
        json.dump(wrapped_data, f, indent=4)

    tmp.replace(path)

# automatically saves
def update_wrapped_data(command_type: str, *function_params, username: str = "", user_id: int = 0):
    global wrapped_data

    user_id = str(user_id)

    # init for empty json
    if not wrapped_data:
        wrapped_data = {"commands": {}, "kurukuru": {}, "total_cmd_uses": 0, "total_kurus": 0}

    # expect 4 params here, each if the user got each respective kuru
    if command_type == "kurukuru":
        if "kuru1" not in wrapped_data["kurukuru"]:
            wrapped_data["kurukuru"] = {"kuru1": 0, "kuru2": 0, "kuru3": 0, "kuru4": 0, "usernames": [], "ids": []}

        wrapped_data["kurukuru"]["kuru1"] += function_params[0]
        wrapped_data["kurukuru"]["kuru2"] += function_params[1]
        wrapped_data["kurukuru"]["kuru3"] += function_params[2]
        wrapped_data["kurukuru"]["kuru4"] += function_params[3]

        wrapped_data["kurukuru"]["usernames"].append(username)
        wrapped_data["kurukuru"]["ids"].append(user_id)
        wrapped_data["total_kurus"] += function_params[0] + function_params[1] + function_params[2] + function_params[3]

        save_wrapped_data()
        print(f"Updated wrapped with:\n{command_type}\n{function_params}\n{username}\n{user_id}")
        return

    # check if the command hasnt been added yet
    if command_type not in wrapped_data["commands"]:
        wrapped_data["commands"][command_type] = {"usernames": [], "ids": [], "uses": 0}

    for i, param in enumerate(function_params, start=1):
        param = str(param)
        i = str(i)

        # check if the params number doesnt exist
        if i not in wrapped_data["commands"][command_type]:
            wrapped_data["commands"][command_type][i] = []

        wrapped_data["commands"][command_type][i].append(param)

    wrapped_data["commands"][command_type]["usernames"].append(username)
    wrapped_data["commands"][command_type]["ids"].append(user_id)
    wrapped_data["commands"][command_type]["uses"] += 1
    wrapped_data["total_cmd_uses"] += 1

    save_wrapped_data()
    print(f"Updated wrapped with:\n{command_type}\n{function_params}\n{username}\n{user_id}")

wrapped_data = load_wrapped_data()

class Wrapped(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Wrapped(bot))