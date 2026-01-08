import pathlib

import discord
from discord.ext import commands
from discord import app_commands

import json
import asyncio

wrapped_lock = asyncio.Lock()

def load_wrapped_data():
    wrapped_data = {}

    with open('wrapped.json', 'r') as json_file:
        wrapped_data = json.load(json_file)

    return wrapped_data

def save_wrapped_data(wrapped_data):
    path = pathlib.Path("wrapped.json")
    tmp = path.with_suffix(".tmp")

    with tmp.open("w") as f:
        f.seek(0)
        json.dump(wrapped_data, f, indent=4)

    tmp.replace(path)

# automatically saves
async def update_wrapped_data(command_type: str, *function_params, username: str = "", user_id: int = 0):
    async with wrapped_lock:
        wrapped_data = load_wrapped_data()

        user_id = str(user_id)

        # init for empty json
        if not wrapped_data:
            wrapped_data = {"commands": {}, "kurukuru": {}, "total_cmd_uses": 0, "total_kurus": 0}

        # expect 4 params here, each if the user got each respective kuru
        if command_type == "kurukuru":
            print("AM INTRAT COAIE IN IF IAR")
            if "kuru1user" not in wrapped_data["kurukuru"]:
                wrapped_data["kurukuru"] = {"kuru1user": [], "kuru2user": [], "kuru3user": [], "kuru4user": [], "kuru1id": [], "kuru2id": [], "kuru3id": [], "kuru4id": [], "usernames": [], "ids": []}

            if function_params[0]:
                wrapped_data["kurukuru"]["kuru1user"].append(username)
                wrapped_data["kurukuru"]["kuru1id"].append(user_id)
            
            if function_params[1]:
                wrapped_data["kurukuru"]["kuru2user"].append(username)
                wrapped_data["kurukuru"]["kuru2id"].append(user_id)

            if function_params[2]:
                wrapped_data["kurukuru"]["kuru3user"].append(username)
                wrapped_data["kurukuru"]["kuru3id"].append(user_id)

            if function_params[3]:
                wrapped_data["kurukuru"]["kuru4user"].append(username)
                wrapped_data["kurukuru"]["kuru4id"].append(user_id)

            wrapped_data["kurukuru"]["usernames"].append(username)
            wrapped_data["kurukuru"]["ids"].append(user_id)
            wrapped_data["total_kurus"] += function_params[0] + function_params[1] + function_params[2] + function_params[3]

            save_wrapped_data(wrapped_data)
            print(f"Updated wrapped with:\ntype {command_type}\nparams {function_params}\nusername {username}\nid{user_id}")
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

        save_wrapped_data(wrapped_data)
        print(f"Updated wrapped with:\n{command_type}\n{function_params}\n{username}\n{user_id}")

class Wrapped(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Wrapped(bot))