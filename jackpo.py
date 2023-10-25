import discord
from random import randint
from discord.ext import commands

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
lista = []


class Jackpo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Jackpo up")

    @commands.Cog.listener()
    async def on_message(self, message):

        global lista

        if message.author.nick:
            name = message.author.nick
        else:
            name = str(message.author).title()

        if message.author == self.client.user:
            return

        if message.author != client.user and "#0000" not in str(message.author):
            if str(message.author) not in lista and len(lista) >= 1:
                lista = []
                lista.append(str(message.author))
            else:
                lista.append(str(message.author))

        print(lista)
        print(f"{message.author} imparte intelepciune: '{message.content}', #{message.channel}, "
              f"length: {len(message.content)}")


        jackpot = ["J", "A", "C", "K", "P", "O", "T", "E"]
        num = randint(1, 1000)
        counter = 0
        fake_num = 0
        if len(lista) >= 1:
            for nume in range(len(lista)):
                if lista[0] == lista[nume]:
                    counter += 1
                if counter >= 4:
                    fake_num = num
                elif lista[0] != lista[nume]:
                    lista = []

        if str(message.channel) == "amogus-testing":
            num = 0
        if num == 1:
            await message.channel.send("Nice try buddy, but you rolled 1!", reference=message, mention_author=True)
        if num == 999:
            await message.channel.send("Nice try buddy, but you rolled 999!", reference=message, mention_author=True)
        if num == 1000 and len(message.content) < 5:
            await message.channel.send(f"This would've been a winning message of the letter "
                                       f"{jackpot[randint(0, (len(jackpot) - 1))]}, but it was **{len(message.content)}** "
                                       f"characters long. Keep trying bozo. <:pepe_flower:901873383212462091>",
                                       reference=message, mention_author=True)
        elif num == 1000 and len(message.content) >= 5:
            await message.channel.send(f"fuck u and ur {jackpot[randint(0, (len(jackpot) - 1))]}", reference=message, mention_author=False)
        elif fake_num == 1000:
            await message.channel.send(f"<@&1136310506471309383> WE HAVE A WINNER!!!\n{name} got the letter "
                                       f"**{jackpot[randint(0, (len(jackpot) - 1))]}**"
                                       f"\nCongrats my friend {name}! <:pepeloon:910540003828985926>"
                                       f"\n\nBUUUUUUUUUUUUUUUUUUT YOU DIDNT QUALIFY AS YOU SENT {len(lista)} MESSAGES IN A "
                                       f"ROW!!!!!", reference=message, mention_author=True)
        jackpo = randint(1, 100000)
        counter = 0
        fake_jackpo = 0
        if len(lista) >= 0:
            for nume in range(len(lista)):
                if lista[0] == lista[nume]:
                    counter += 1
                if counter >= 4:
                    fake_jackpo = jackpo
                elif lista[0] != lista[nume]:
                    lista = []
        if str(message.channel) == "amogus-testing":
            jackpo = 0
        if jackpo >= 99990:
            await message.channel.send(f"YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO YOU ROLLED {jackpo} MY FRIEND, KEEP TRYING!",
                                       reference=message, mention_author=True)
        emote = "<:LETSFUCKINGGOO:901184486702710804>" * 20
        if jackpo == 100000 and len(message.content) < 5:
            await message.channel.send(
                f"YOOOOOOOOOO you're so unlucky {name}!!!!! This would've been a winning message for "
                f"JACKPO, but it was **{len(message.content)}** characters long. Keep trying bozo. "
                f"<:pepe_flower:901873383212462091>")
        if jackpo == 100000 and len(message.content) >= 5:
            await message.channel.send(
                f"<@&1136310506471309383> YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO WTF IS YOUR LUCK "
                f"{name}\n You got JACKPO!!!!!!!!!!!!!!! "
                f"\nCONGRATSSSSSSSSSS {name}! {emote}", reference=message,
                mention_author=True)

        if fake_jackpo == 1000:
            await message.channel.send(
                f"<@&1136310506471309383> YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO WTF IS YOUR LUCK "
                f"{name}\n You got JACKPO!!!!!!!!!!!!!!! "
                f"\nCONGRATSSSSSSSSSS {name}! {emote}",
                f"\n\nBUUUUUUUUUUUUUUUUUUT YOU DIDNT QUALIFY AS YOU SENT {len(lista)} MESSAGES IN A ROW!!!!!",
                reference=message,
                mention_author=True)

        if fake_num != 0 or fake_jackpo != 0:
            print(f"{message.author} rolled {fake_num} for FAKE LETTERS and {fake_jackpo} for FAKE JACKPO\n")
        else:
            print(f"{message.author} rolled {num} for letters and {jackpo} for JACKPO\n")


async def setup(client):
    await client.add_cog(Jackpo(client))
