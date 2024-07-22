import discord
from discord.ext import commands
from discord import app_commands
import json
import asyncio
import threading
import os
from random import randint

jailtime = True
ceva_id = []
coldoun = 0
lock = threading.Lock()
symbols = ["clubs", "diamonds", "hearts", "spades"]


# async def idiotuApasa():
#     global coldoun
#     if not coldoun:
#         for i in range(0, 3):
#             await asyncio.sleep(1)
#             coldoun += 1
#         coldoun = 0


def symbol(name):
    if name == "spades":
        return "♠"
    elif name == "hearts":
        return "♥"
    elif name == "clubs":
        return "♣"
    elif name == "diamonds":
        return "♦"


def suma(player_cards, hidden_card):
    lista = []
    ace = False
    for card in player_cards:
        if card[0] == 14:
            if ace:
                aux = 1
            else:
                ace = True
                aux = 11 if ace else 1
        elif card[0] in range(11, 14):
            aux = 10
        elif card[0] == 15:
            aux = 0
        else:
            aux = card[0]
        lista.append(aux)
    suma = sum(card for card in lista)
    if hidden_card:
        pass
    else:
        suma -= 10 if suma > 21 and ace else 0
    return suma


def add_cards(player_cards, dealer_cards, mode, hidden_card):
    global symbols
    while True:
        lista = []
        cards_rando = randint(2, 14)
        symbols_rando = randint(0, 3)
        lista.append(cards_rando)
        lista.append(symbols[symbols_rando])
        if lista not in player_cards and lista not in dealer_cards and lista not in hidden_card:
            if mode == 0:
                player_cards.append(lista)
                return player_cards
            else:
                if lista not in player_cards and lista not in hidden_card and lista not in dealer_cards:
                    if not hidden_card:
                        hidden_card.append(lista)
                        dealer_cards.append([15, 'clubs'])
                        return hidden_card, dealer_cards
                    else:
                        dealer_cards.append(lista)
                        return dealer_cards


def rules(player_cards, dealer_cards, player_sum, dealer_sum, score, bet, hidden_card):
    embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
    embed.add_field(name="Your cards:", value=f"**Sum: {suma(player_cards, hidden_card)}**\n"
                                              f"{nice_print(player_cards)}", inline=False)
    won, lost, tie = False, False, False
    if not hidden_card:
        if dealer_sum == player_sum:
            tie = True
        elif dealer_sum < player_sum or dealer_sum > 21 or player_sum == 21 and player_sum <= 21:
            score += bet
            won = True
        else:
            score -= bet
            score = max(0, score)
            lost = True

        embed.add_field(name="Dealer's cards:", value=f"**Sum: {suma(dealer_cards, hidden_card)}**\n"
                                                      f"{nice_print(dealer_cards)}", inline=False)
        if lost:
            embed.add_field(name="You lost...", value=f"Your score is now {score} points. Play again?")
        elif won:
            embed.add_field(name="You won!", value=f"Your score is now {score} points. Play again?")
        elif tie:
            embed.add_field(name="You tied!", value=f"Your score is now {score} points. Play again?")
        return score, bet, embed

    if player_sum > 21:
        score -= bet
        score = max(0, score)
        dealer_cards[0][0] = hidden_card[0][0]
        dealer_cards[0][1] = hidden_card[0][1]
        hidden_card = []
        embed.add_field(name="Dealer's cards:", value=f"**Sum: {suma(dealer_cards, hidden_card)}**\n"
                                                      f"{nice_print(dealer_cards)}", inline=False)
        embed.add_field(name="You lost...", value=f"Your score is now {score} points. Play again?")
        return score, bet, embed

    if player_sum == 21:
        dealer_cards[0][0] = hidden_card[0][0]
        dealer_cards[0][1] = hidden_card[0][1]
        hidden_card = []
        dealer_sum = suma(dealer_cards, hidden_card)
        embed.add_field(name="Dealer's cards:", value=f"**Sum: {suma(dealer_cards, hidden_card)}**\n"
                                                      f"{nice_print(dealer_cards)}", inline=False)
        if dealer_sum == 21:
            embed.add_field(name="You tied!", value=f"Your score is now {score} points. Play again?")
        else:
            score += bet
            embed.add_field(name="You won!", value=f"Your score is now {score} points. Play again?")

        return score, bet, embed
    else:
        if dealer_sum == 21:
            if player_sum == 21:  # niciodata nu va intra aici cred
                embed.add_field(name="You tied!", value=f"Your score is now {score} points. Play again?")
            else:
                dealer_cards[0][0] = hidden_card[0][0]
                dealer_cards[0][1] = hidden_card[0][1]
                hidden_card = []
                dealer_sum = suma(dealer_cards, hidden_card)
                embed.add_field(name="Dealer's cards:", value=f"**Sum: {suma(dealer_cards, hidden_card)}**\n"
                                                              f"{nice_print(dealer_cards)}", inline=False)
                score -= bet
                score = max(0, score)
                embed.add_field(name="You lost...", value=f"Your score is now {score} points. Play again?")
                return score, bet, embed

    # embed.add_field(name="Dealer's cards:", value=f"**Sum: {suma(dealer_cards, hidden_card)}**\n"
    #                                               f"?? ?? / {nice_print(dealer_cards)}", inline=False)
    return 0, 0, 0


def update(user_id, name, bet, score, dealer_cards, player_cards, hidden_card, mode):
    user_id = str(user_id)

    with lock:
        try:
            if os.path.exists('jail.json'):
                with open('jail.json', 'r') as json_file:
                    try:
                        data = json.load(json_file)
                    except Exception as e:
                        print(f"esti prost: {e}")

            if user_id not in data:
                data[user_id] = {"name": name, "score": 1000, "bet": 0, "dealer_cards": [],
                                 "player_cards": [], "hidden_card": [], "in_game": False}

            if mode == "bet":
                data[user_id]["bet"] += bet
                data[user_id]["bet"] = max(data[user_id]["bet"], 0)
                data[user_id]["in_game"] = True

                if data[user_id]["score"] < data[user_id]["bet"]:
                    data[user_id]["bet"] = data[user_id]["score"]

            elif mode == "game":
                print(dealer_cards, hidden_card, player_cards)
                data[user_id]["dealer_cards"] = dealer_cards
                data[user_id]["hidden_card"] = hidden_card
                data[user_id]["player_cards"] = player_cards
                data[user_id]["in_game"] = True
            elif mode == "end":
                data[user_id]["dealer_cards"] = []
                data[user_id]["hidden_card"] = []
                data[user_id]["player_cards"] = []
                data[user_id]["in_game"] = False
                data[user_id]['score'] = score
                data[user_id]['bet'] = 0
            elif mode == "clear":
                data[user_id]["dealer_cards"] = []
                data[user_id]["hidden_card"] = []
                data[user_id]["player_cards"] = []
                data[user_id]["in_game"] = False
                data[user_id]['score'] = 1000
                data[user_id]['bet'] = 0
            elif mode == "reset":
                data[user_id]["score"] = 1000

            temp_filepath = 'jail_temp.json'
            with open(temp_filepath, 'w') as temp_file:
                json.dump(data, temp_file, indent=4)

            os.replace(temp_filepath, 'jail.json')

        except Exception as e:
            print(f"Eroare la actualizarea fișierului JSON: {e}")

    if mode == "bet":
        return data[user_id]["bet"]


def get_value(user_id, value, name):
    user_id = str(user_id)
    with lock:
        with open("jail.json", 'r+') as json_file:
            data = json.load(json_file)
            if user_id not in data:
                data[user_id] = {"name": name, "score": 1000, "bet": 0, "dealer_cards": [],
                                 "player_cards": [], "hidden_card": [], "in_game": False}

            return data[user_id][value]


def nice_print(player_cards):
    ceva = ""
    for card in player_cards:
        if card[0] == 11:
            aux = "J"
        elif card[0] == 12:
            aux = "Q"
        elif card[0] == 13:
            aux = "K"
        elif card[0] == 14:
            aux = "A"
        else:
            aux = card[0]

        symbol = card[1]
        if aux == 15:
            pass
        else:
            ceva += f"{aux} :{symbol}: / "

    ceva = ceva[:-3]
    return ceva


class Jail(commands.GroupCog, name="jail"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="activate", description="Activate/deactivate jail or something idk")
    @app_commands.checks.has_permissions(administrator=True)
    async def jailactivate(self, interaction: discord.Interaction):
        global jailtime
        if jailtime:
            jailtime = False
            await interaction.response.send_message("Deactivated jailtime!")
        else:
            jailtime = True
            await interaction.response.send_message("Activated jailtime!")

    @app_commands.command(name="add", description="Add someone to jail or something idk")
    @app_commands.checks.has_permissions(administrator=True)
    async def jailadd(self, interaction: discord.Interaction, user: discord.Member):
        if user.id in [556836294710525952, 1135983715646976111]:
            await interaction.response.send_message("You don't have something better to do?", ephemeral=True)
        elif user.id not in ceva_id:
            ceva_id.append(user.id)
            await interaction.response.send_message(f"Added `{user.name}` to the jail list! <:PeepoNote:802224247098572810>")
        else:
            await interaction.response.send_message("It's already in there you dummmy")

    @app_commands.command(name="list", description="List of jailed people or something idk")
    async def list(self, interaction: discord.Interaction):
        ceva = ''
        if ceva_id:
            for id in ceva_id:
                ceva += f"<@{id}>\n"
            embed = discord.Embed(title=f"Jail list or something idk", color=0x71368a)
            embed.add_field(name="hehe", value=ceva, inline=False)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Jail empty idiot")

    @app_commands.command(name="clear", description="Clears the jail list or something idk")
    @app_commands.checks.has_permissions(administrator=True)
    async def clear(self, interaction: discord.Interaction):
        global ceva_id
        if ceva_id:
            ceva_id = []
            await interaction.response.send_message("Jail cleared!")
        else:
            await interaction.response.send_message("Jail already empty idiot")

    @app_commands.command(name="remove", description="Removes someone jail list or something idk")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove(self, interaction: discord.Interaction, user: discord.User):
        if user.id in ceva_id:
            ceva_id.remove(user.id)
            await interaction.response.send_message(f"Removed `{user.name}` from the jail list!")
        else:
            await interaction.response.send_message("It's not in there you dummy")

    @app_commands.command(name="status", description="Says whether jail is on/off or something idk")
    async def status(self, interaction: discord.Interaction):
        if jailtime:
            await interaction.response.send_message("Jail is currently **activated**!")
        else:
            await interaction.response.send_message("Jail is currently **deactivated**!")

    @app_commands.command(name="blackjack", description="Free yourself or something idk")
    async def blackjack(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
        in_game = get_value(interaction.user.id, 'in_game', interaction.user.name)
        if not in_game:
            if interaction.user.id in ceva_id:
                if interaction.channel.id == 1240665294767263826:
                    view = InitialView()

                    embed.add_field(name="You made it to Gulag!", value=f"Get over **5000** points in order "
                                                                        f"to free yourself!", inline=False)
                    embed.add_field(name=f"You currently have {get_value(interaction.user.id, 'score', interaction.user.name)} points",
                                    value="How to play:\n- Try to get a score as close to 21 as possible\n- Be lucky", inline=False)
                    await interaction.response.send_message(view=view, embed=embed)
                else:
                    embed.add_field(name="#jailbreak idiot", value="", inline=False)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed.add_field(name="You're not jailed idiot", value="", inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            bet = get_value(interaction.user.id, 'bet', interaction.user.name)
            if bet != 0 and get_value(interaction.user.id, "player_cards", interaction.user.name):
                player_cards = get_value(interaction.user.id, 'player_cards', interaction.user.name)
                dealer_cards = get_value(interaction.user.id, 'dealer_cards', interaction.user.name)
                hidden_card = get_value(interaction.user.id, 'hidden_card', interaction.user.name)
                embed.add_field(name="Your cards:", value=f"**Sum: {suma(player_cards, hidden_card)}**\n"
                                                          f"{nice_print(player_cards)}", inline=False)
                embed.add_field(name="Dealer's cards:", value=f"**Sum: {suma(dealer_cards, hidden_card)}**\n"
                                                              f"?? ?? / {nice_print(dealer_cards)}", inline=False)
                await interaction.response.send_message(embed=embed, view=Game())
            else:
                embed.add_field(name="Your bet is now... ",
                                value=f"{bet} points (out of {get_value(interaction.user.id, 'score', interaction.user.name)})!", inline=False)
                await interaction.response.send_message(embed=embed, view=Bets())

    @remove.error
    async def remove_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.response.send_message("You don't have permissions idiot", ephemeral=True)

    @jailactivate.error
    async def jailactivate_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.response.send_message("You don't have permissions idiot", ephemeral=True)

    @jailadd.error
    async def jailadd_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.response.send_message("You don't have permissions idiot", ephemeral=True)

    @clear.error
    async def clear_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.response.send_message("You don't have permissions idiot", ephemeral=True)


class InitialView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Begin", style=discord.ButtonStyle.green, emoji="✅")
    async def begin(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ceva_id:
            return
        embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
        embed.add_field(name="Your bet is...", value="", inline=False)
        await interaction.response.edit_message(view=Bets(), embed=embed)

    @discord.ui.button(label="Reset score", style=discord.ButtonStyle.red, emoji="⏪")
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ceva_id:
            return
        update(interaction.user.id, interaction.user.name, 0, 1000, [], [], [], "clear")
        embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
        embed.add_field(name="You made it to Gulag!", value=f"Get over **5000** points in order "
                                                            f"to free yourself!", inline=False)
        embed.add_field(name=f"You currently have {get_value(interaction.user.id, 'score', interaction.user.name)} points",
                        value="How to play:\n- Try to get a score as close to 21 as possible\n- Be lucky", inline=False)
        await interaction.response.edit_message(view=self, embed=embed)


class Bets(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="+100 pts", style=discord.ButtonStyle.green, emoji="📈")  # or .success
    async def osuta(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ceva_id:
            return
        embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
        if not coldoun:
            bet = update(interaction.user.id, interaction.user.name, 100, 0, 0, 0, 0, "bet")
            embed.add_field(name="Your bet is now... ",
                            value=f"{bet} points (out of {get_value(interaction.user.id, 'score', interaction.user.name)})!", inline=False)
        else:
            embed.add_field(name=f"Wait {3 - coldoun}s idiot", value=f"", inline=False)
        await interaction.response.edit_message(view=self, embed=embed)
#         # await idiotuApasa()

    @discord.ui.button(label="+500 pts", style=discord.ButtonStyle.green, emoji="📈")  # or .success
    async def cincisute(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ceva_id:
            return
        embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
        if not coldoun:
            await asyncio.sleep(1)
            bet = update(interaction.user.id, interaction.user.name, 500, 0, 0, 0, 0, "bet")
            embed.add_field(name="Your bet is now... ",
                            value=f"{bet} points (out of {get_value(interaction.user.id, 'score', interaction.user.name)})!", inline=False)
        else:
            embed.add_field(name=f"Wait {3 - coldoun}s idiot", value=f"", inline=False)
        await interaction.response.edit_message(view=self, embed=embed)
        # await idiotuApasa()

    @discord.ui.button(label="+Max pts", style=discord.ButtonStyle.green, emoji="📈")  # or .success
    async def max(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ceva_id:
            return
        embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
        if not coldoun:
            bet = update(interaction.user.id, interaction.user.name, 999999999, 0, 0, 0, 0, "bet")
            embed.add_field(name="Your bet is now... ",
                            value=f"{bet} points (out of {get_value(interaction.user.id, 'score', interaction.user.name)})!", inline=False)
        else:
            embed.add_field(name=f"Wait {3 - coldoun}s idiot", value=f"", inline=False)
        await interaction.response.edit_message(view=self, embed=embed)
        # await idiotuApasa()

    @discord.ui.button(label="-100 pts", style=discord.ButtonStyle.red, emoji="📉")  # or .success
    async def neosuta(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ceva_id:
            return
        embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
        if not coldoun:
            bet = update(interaction.user.id, interaction.user.name, -100, 0, 0, 0, 0, "bet")
            embed.add_field(name="Your bet is now... ",
                            value=f"{bet} points (out of {get_value(interaction.user.id, 'score', interaction.user.name)})!", inline=False)
        else:
            embed.add_field(name=f"Wait {3 - coldoun}s idiot", value=f"", inline=False)
        await interaction.response.edit_message(view=self, embed=embed)
        # await idiotuApasa()

    @discord.ui.button(label="-500 pts", style=discord.ButtonStyle.red, emoji="📉")  # or .success
    async def necincisute(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ceva_id:
            return
        embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
        if not coldoun:
            bet = update(interaction.user.id, interaction.user.name, -500, 0, 0, 0, 0, "bet")
            embed.add_field(name="Your bet is now... ",
                            value=f"{bet} points (out of {get_value(interaction.user.id, 'score', interaction.user.name)})!", inline=False)
        else:
            embed.add_field(name=f"Wait {3 - coldoun}s idiot", value=f"", inline=False)
        await interaction.response.edit_message(view=self, embed=embed)
        # await idiotuApasa()

    @discord.ui.button(label="-Max pts", style=discord.ButtonStyle.red, emoji="📉")  # or .success
    async def nemax(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ceva_id:
            return
        embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
        if not coldoun:
            bet = update(interaction.user.id, interaction.user.name, -999999999, 0, 0, 0, 0, "bet")
            embed.add_field(name="Your bet is now... ",
                            value=f"{bet} points (out of {get_value(interaction.user.id, 'score', interaction.user.name)})!", inline=False)
        else:
            embed.add_field(name=f"Wait {3 - coldoun}s idiot", value=f"", inline=False)
        await interaction.response.edit_message(view=self, embed=embed)
        # await idiotuApasa()

    @discord.ui.button(label="Stop betting", style=discord.ButtonStyle.red, emoji="💵")  # or .success
    async def stopbet(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ceva_id:
            return
        if get_value(interaction.user.id, 'bet', interaction.user.name) > 0:
            embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)

            player_cards, dealer_cards, hidden_card = [], [], []
            player_cards = add_cards(player_cards, dealer_cards, 0, hidden_card)
            hidden_card, dealer_cards = add_cards(player_cards, dealer_cards, 1, hidden_card)
            player_cards = add_cards(player_cards, dealer_cards, 0, hidden_card)
            dealer_cards = add_cards(player_cards, dealer_cards, 1, hidden_card)
            update(interaction.user.id, interaction.user.name, 0, 0, dealer_cards, player_cards, hidden_card, "game")

            embed.add_field(name="Your cards:", value=f"**Sum: {suma(player_cards, hidden_card)}**\n"
                                                      f"{nice_print(player_cards)}", inline=False)
            embed.add_field(name="Dealer's cards:", value=f"**Sum: {suma(dealer_cards, hidden_card)}**\n"
                                                          f"?? ?? / {nice_print(dealer_cards)}", inline=False)
            if not rules(player_cards, dealer_cards, suma(player_cards, hidden_card), suma(dealer_cards, hidden_card),
                         get_value(interaction.user.id, 'score', interaction.user.name), get_value(interaction.user.id, 'bet', interaction.user.name), hidden_card)[2]:
                if score < 5000:
                    await interaction.response.edit_message(view=Game(), embed=embed)
                else:
                    embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
                    embed.add_field(name="You are free... for now", value="", inline=False)
                    ceva_id.remove(interaction.user.id)
                    update(interaction.user.id, interaction.user.name, 0, 1000, [], [], [], 'clear')
                    await interaction.response.edit_message(view=None, embed=embed)
            else:
                score, bet, embed = rules(player_cards, dealer_cards, suma(player_cards, hidden_card), suma(dealer_cards, hidden_card),
                                          get_value(interaction.user.id, 'score', interaction.user.name), get_value(interaction.user.id, 'bet', interaction.user.name), hidden_card)
                update(interaction.user.id, interaction.user.name, bet, score, dealer_cards, player_cards, hidden_card, "end")
                await interaction.response.edit_message(view=PlayAgain(), embed=embed)
        else:
            embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
            embed.add_field(name="Actually bet something idiot", value="", inline=False)
            await interaction.response.edit_message(view=self, embed=embed)

    @discord.ui.button(label="Reset score", style=discord.ButtonStyle.red, emoji="⏪")
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ceva_id:
            return
        update(interaction.user.id, interaction.user.name, 0, 1000, [], [], [], "clear")
        embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
        embed.add_field(name="You made it to Gulag!", value=f"Get over **5000** points in order "
                                                            f"to free yourself!", inline=False)
        embed.add_field(name=f"You currently have {get_value(interaction.user.id, 'score', interaction.user.name)} points",
                        value="How to play:\n- Try to get a score as close to 21 as possible\n- Be lucky", inline=False)
        await interaction.response.edit_message(view=self, embed=embed)


class Game(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Draw a card", style=discord.ButtonStyle.green, emoji="🃏")  # or .success
    async def draw(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ceva_id:
            return
        player_cards = get_value(interaction.user.id, "player_cards", interaction.user.name)
        dealer_cards = get_value(interaction.user.id, "dealer_cards", interaction.user.name)
        hidden_card = get_value(interaction.user.id, "hidden_card", interaction.user.name)
        player_cards = add_cards(player_cards, dealer_cards, 0, hidden_card)
        embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
        embed.add_field(name="Your cards:", value=f"**Sum: {suma(player_cards, hidden_card)}**\n"
                                                  f"{nice_print(player_cards)}", inline=False)
        embed.add_field(name="Dealer's cards:", value=f"**Sum: {suma(dealer_cards, hidden_card)}**\n"
                                                      f"?? ?? / {nice_print(dealer_cards)}", inline=False)

        update(interaction.user.id, interaction.user.name, 0, 0, dealer_cards, player_cards, hidden_card, "game")

        if not rules(player_cards, dealer_cards, suma(player_cards, hidden_card), suma(dealer_cards, hidden_card),
                     get_value(interaction.user.id, 'score', interaction.user.name), get_value(interaction.user.id, 'bet', interaction.user.name), hidden_card)[2]:
            await interaction.response.edit_message(view=Game(), embed=embed)
        else:
            score, bet, embed = rules(player_cards, dealer_cards, suma(player_cards, hidden_card), suma(dealer_cards, hidden_card),
                                      get_value(interaction.user.id, 'score', interaction.user.name), get_value(interaction.user.id, 'bet', interaction.user.name), hidden_card)
            update(interaction.user.id, interaction.user.name, bet, score, dealer_cards, player_cards, hidden_card, "end")
            if score < 5000:
                await interaction.response.edit_message(view=PlayAgain(), embed=embed)
            else:
                embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
                embed.add_field(name="You are free... for now", value="", inline=False)
                ceva_id.remove(interaction.user.id)
                update(interaction.user.id, interaction.user.name, 0, 1000, [], [], [], 'clear')
                await interaction.response.edit_message(view=None, embed=embed)

    @discord.ui.button(label="Stop drawing", style=discord.ButtonStyle.red, emoji="✖")
    async def end(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ceva_id:
            return
        player_cards = get_value(interaction.user.id, "player_cards", interaction.user.name)
        dealer_cards = get_value(interaction.user.id, "dealer_cards", interaction.user.name)
        hidden_card = get_value(interaction.user.id, "hidden_card", interaction.user.name)
        dealer_cards[0][0] = hidden_card[0][0]
        dealer_cards[0][1] = hidden_card[0][1]
        hidden_card = []
        dealer_sum = suma(dealer_cards, hidden_card)
        while suma(dealer_cards, hidden_card) < 17:
            dealer_cards = add_cards(player_cards, dealer_cards, 1, [1000, 'carte'])
            dealer_sum = suma(dealer_cards, hidden_card)

        score, bet, embed = rules(player_cards, dealer_cards, suma(player_cards, hidden_card), suma(dealer_cards, hidden_card),
                                  get_value(interaction.user.id, 'score', interaction.user.name), get_value(interaction.user.id, 'bet', interaction.user.name), hidden_card)
        update(interaction.user.id, interaction.user.name, bet, score, dealer_cards, player_cards, hidden_card, "end")
        if score < 5000:
            await interaction.response.edit_message(view=PlayAgain(), embed=embed)
        else:
            embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
            embed.add_field(name="You are free... for now", value="", inline=False)
            ceva_id.remove(interaction.user.id)
            update(interaction.user.id, interaction.user.name, 0, 1000, [], [], [], 'clear')
            await interaction.response.edit_message(view=None, embed=embed)
    # @discord.ui.button(label="Blurple Button", style=discord.ButtonStyle.blurple, emoji="🎁")  # or .primary
    # async def blurple_button(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     await interaction.response.edit_message(f"Your bet is now {bet}", view=self)
    #
    # @discord.ui.button(label="Gray Button", style=discord.ButtonStyle.gray, emoji="\U0001f974", disabled=False)  # or .secondary/.grey
    # async def gray_button(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     await interaction.response.edit_message(f"Your bet is now {bet}", view=self)
    #
    # @discord.ui.button(label="Green Button", style=discord.ButtonStyle.green, emoji="<:FD_pepeyay:878854266012438549>")  # or .success
    # async def green_button(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     await interaction.response.edit_message(f"Your bet is now {bet}", view=self)
    #
    # @discord.ui.button(label="Red Button", style=discord.ButtonStyle.red, emoji="<:arlelurk:1235264497476698235>")  # or .danger
    # async def red_button(self, button: discord.ui.Button, interaction: discord.Interaction):
    #     button.disabled = True
    #     await interaction.response.edit_message(f"Your bet is now {bet}", view=self)


class PlayAgain(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Play again", style=discord.ButtonStyle.green, emoji="💸")  # or .success
    async def again(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ceva_id:
            return
        embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
        embed.add_field(name="You made it to Gulag!", value=f"Get over **5000** points in order "
                                                            f"to free yourself!", inline=False)
        embed.add_field(name=f"You currently have {get_value(interaction.user.id, 'score', interaction.user.name)} points",
                        value="How to play:\n- Try to get a score as close to 21 as possible\n- Be lucky", inline=False)
        await interaction.response.edit_message(view=InitialView(), embed=embed)

    @discord.ui.button(label="Stop playing", style=discord.ButtonStyle.red, emoji="🤚")  # or .success
    async def kill(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id not in ceva_id:
            return
        embed = discord.Embed(title=f"Blackjack haha idk", color=0x71368a)
        embed.add_field(name=f"See you next time {interaction.user.name}", value=f"", inline=False)
        await interaction.response.edit_message(embed=embed, view=None)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Jail(bot), guild=discord.Object(id=748126143584141332))
