import discord
from discord.ext import commands
from random import randint
import asyncio
import re
jailtime = True
ceva_id = [1007925941093281812]

class Funni(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def angel(self, ctx, *, arg):
        print(arg)
        await ctx.message.delete()
        await ctx.channel.send(arg)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def jail(self, ctx):  
        global jailtime
        # if ctx.author.id == 399022430699520006:
        #     await ctx.reply("Caca nu e voie!", mention_author = False)
        if jailtime:
            jailtime = False
            await ctx.reply("Deactivated jailtime!", mention_author=False)
        else:
            jailtime = True
            await ctx.reply("Activated jailtime!", mention_author=False)
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def list(self, ctx):
        le_copie = ""
        for user_id in ceva_id:
            le_copie += f"<@{user_id}>\n"
        if le_copie == "":
            await ctx.reply("Jail empty idiot", mention_author=False)
        else:
            await ctx.reply(le_copie, mention_author=False)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def jailadd(self, ctx, user_id: int):
        if user_id in [556836294710525952, 970592525230407680]:
            await ctx.reply("You don't have something better to do?", mention_author=False)
        elif user_id not in ceva_id:
            ceva_id.append(user_id)
            await ctx.reply(f"Added `{user_id}` to the jail list! <:PeepoNote:802224247098572810>", mention_author=False)
        else:
            await ctx.reply("It's already in there you dummmy", mention_author=False)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def jailremove(self, ctx, user_id: int):
        if user_id in ceva_id:
            ceva_id.remove(user_id)
            await ctx.reply(f"Removed `{user_id}` from the jail list!", mention_author=False)
        else:
            await ctx.reply("It's not in there you dummy", mention_author=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        print(f"{message.author} imparte intelepciune: '{message.content}', #{message.channel}")
        masaj = re.findall(r'\w+', str(message.content.lower()))
        if str(message.author) == "clyde#0000":
            name = message.author
            message.author.nick = False
        elif message.author.nick:
            name = message.author.nick
        else:
            name = str(message.author).title()

        channel = self.bot.get_channel(1166774967552184380)
        if message.author == self.bot.user:
            return

        if message.guild.id in [570929677732937738]:
            if "the man" in message.content.lower() and message.author.id in [556836294710525952, 278798822937853953]:
                await message.channel.send("Dave the man <:LETSFUCKINGGOO:901184486702710804>", reference=message, mention_author=False)
            channel2 = self.bot.get_channel(1170111919512887376)
            if message.channel.name in ["bot", "staff"]:
                await channel2.send(f"**{name}** in **#{message.channel}**: '{str(message.content)}'")
            pass
        elif message.guild.id in [993818190008287283, 748126143584141332, 1030490217855074304]:
            global jailtime
            x = randint(1, 250)

            if message.author.id in ceva_id and jailtime is True:
                a = message.content
                if a == "":
                    a = "*some random attachment*"
                await channel.send(f"**{name} in <#{message.channel.id}>**: {a}")
                await asyncio.sleep(2)
                await message.delete()

            if message.author.id == 556837875803488256:
                duration = datetime.timedelta(seconds=5, minutes=0, hours=0, days=0)
                await message.author.timeout(until=duration)

            if str(message.channel) == "administratum" or str(message.channel) == "teme":
                x = 0
            elif str(message.channel) == "amogus-testing":
                x = 250
            if x == 250:
                funni = [f"Haha how funny of you {name} <:keek:806077897584410685>", "Ong fr fr", "*silence*",
                         "<:pogFrog:802088916244234261>", "Just no <:pepe_flower:901873383212462091>", "YES", "ඞ",
                         f"{name} stinks", "Based", "Why?", "Are you sure?", "💀", "Please don't", "Please do", "Not based",
                         "Great idea!", "Bad idea!", "*claps*", "*throws up*", "🤝", "<a:kurukuru:1113242215083421707>",
                         "Who asked?", "And?", "Ok buddy", f"This is why {name} shouldn't run for president",
                         "Thanks for the idea",
                         "Why does that matter?", "My reaction to that information: 💀",
                         "Do you know what you're talking about?",
                         f"This is not proper etiquette, {name}", "Do NOT say this again", "You can say that again!", "Fr?",
                         "🧢",
                         "I was today years old when I realized I didn’t like you.",
                         "Someday you’ll go far. And I really hope you stay there.",
                         "Oops, my bad. I could’ve sworn I was dealing with an adult.",
                         "I love what you’ve done with your hair. How do you get it to come out of your nostrils like that?",
                         "Remember that time you were saying that thing I didn’t care about? Yeah, that is now.",
                         "You’re the reason God created the middle finger.",
                         "I’m busy right now, can I ignore you another time?",
                         "Oh, you don’t like being treated the way you treat me? That must suck.",
                         "I wish I had a flip phone, so I could slam it shut on this conversation.",
                         "N’Sync said it best, “BYE, BYE, BYE!”",
                         "I’ve been called worse things by better men.",
                         "You’re a gray sprinkle on a rainbow cupcake.",
                         "Your secrets are always safe with me. I never even listen when you tell me them.",
                         "You bring everyone so much joy! You know, when you leave the room. But, still.",
                         "How many licks until I get to the interesting part of this conversation?",
                         "Keep rolling your eyes, you might eventually find a brain.",
                         "Your face makes onions cry.",
                         "Did I invite you to the barbecue? Then why are you all up in my grill?",
                         "Our kid must have gotten his brain from you! I still have mine.",
                         "You have so many gaps in your teeth it looks like your tongue is in jail.",
                         "If your brain was dynamite, there wouldn’t be enough to blow your hat off.",
                         "You are more disappointing than an unsalted pretzel.",
                         "It’s impossible to underestimate you.",
                         "Wow, your maker really didn’t waste time giving you a personality, huh?",
                         "Her teeth were so bad she could eat an apple through a fence.",
                         "I’ll never forget the first time we met. But I’ll keep trying.",
                         "Oh, I’m sorry. Did the middle of my sentence interrupt the beginning of yours?",
                         "Hold still. I’m trying to imagine you with personality.",
                         "I’m not insulting you, I’m describing you.",
                         "You are the human version of period cramps.",
                         "You’re cute. Like my dog. He also chases his tail for entertainment.",
                         "You are like a cloud. When you disappear, it’s a beautiful day.",
                         "You have an entire life to be an idiot. Why not take today off?",
                         "Your kid is so annoying, he makes his Happy Meal cry.",
                         "Your face is just fine, but we’ll have to put a bag over that personality.",
                         "I’m not a nerd. I’m just smarter than you.",
                         "I may love to shop but I will never buy your bull.",
                         "Child, I’ve forgotten more than you ever knew.",
                         "I’m an acquired taste. If you don’t like me, acquire some taste.",
                         "Bye. Hope to see you never.",
                         "Don’t worry, the first 40 years of childhood are always the hardest.",
                         "If you’re going to be two-faced, at least make one of them pretty.",
                         "The only way my husband would ever get hurt during an activity is if the TV exploded.",
                         "If you have a problem with me, write the problem on a piece of paper, fold it, and shove it up your ass.",
                         "Complete this sentence for me: 'I never want to see you ————!'",
                         "I thought of you today. It reminded me to take out the trash.",
                         "You bring everyone so much joy when you leave the room.",
                         "Did the mental hospital test too many drugs on you today?",
                         "OH MY GOD! IT SPEAKS!",
                         "Beauty is only skin deep, but ugly goes clean to the bone.",
                         "I’d like to help you out. Which way did you come in?",
                         "I forgot the world revolves around you. My apologies, how silly of me.",
                         "Light travels faster than sound which is why you seemed bright until you spoke.",
                         "I’d rather treat my baby’s diaper rash than have lunch with you.",
                         "You look so pretty. Not at all gross, today.",
                         "I only take you everywhere I go, so I don’t have to kiss you goodbye.",
                         "We were happily married for one month, but unfortunately, we’ve been married for 10 years.",
                         "When you look in the mirror, say hi to the clown you see in there for me, would you?",
                         "Somewhere out there is a tree tirelessly producing oxygen for you. You owe it an apology.",
                         "That sounds like a you problem.",
                         "You have miles to go before you reach mediocre."]

                if funni and str(message.channel) == "amogus-testing":
                    angel = ["What is the largest continent on Earth?",
                             "Which river is the longest in the world?",
                             "What is the capital of Australia?",
                             "Which country is known as the Land of the Rising Sun?",
                             "Which desert is the largest in the world?",
                             "What is the highest mountain peak in North America?",
                             "In which country would you find the Amazon Rainforest?",
                             "Which African country is known as the \"Pearl of Africa\"?",
                             "What is the capital of New Zealand?",
                             "Name the largest ocean on Earth.",
                             "Which country is known as the \"Land of Fire and Ice\"?",
                             "What is the smallest continent?",
                             "Which river flows through Cairo?",
                             "What is the capital of Russia?",
                             "What is the southernmost continent?",
                             "Which country is the smallest in terms of land area?",
                             "In which ocean is the Great Barrier Reef located?",
                             "What is the capital of Egypt?",
                             "Which African country is known as the \"Rainbow Nation\"?",
                             "Which European city is famous for its canals?",
                             "What is the capital of Argentina?",
                             "Which river forms part of the border between the United States and Mexico?",
                             "Which country is known as the \"Land of the Rising Sun\"?",
                             "What is the largest country by land area in South America?",
                             "Which mountain range stretches across the northern border of India?",
                             "What is the capital of South Korea?",
                             "In which country would you find the city of Marrakech?",
                             "Which river is often called the \"Father of Waters\"?",
                             "What is the highest mountain peak in the world?",
                             "Which African country is known as the \"Giant of Africa\"?",
                             "What is the capital of Canada?",
                             "Which desert is located in the southwestern United States and northern Mexico?",
                             "What is the capital of Turkey?",
                             "Which country is known as the \"Land of a Thousand Lakes\"?",
                             "What is the largest island in the Mediterranean Sea?",
                             "Which river flows through Paris?",
                             "What is the capital of Chile?",
                             "In which country would you find the city of Dubai?",
                             "Which African country is known as the \"Horn of Africa\"?",
                             "Which European country is known as the \"Land of the Midnight Sun\"?",
                             "What is the capital of Brazil?",
                             "Which river is the longest in Europe?",
                             "What is the highest mountain peak in Africa?",
                             "Which country is known as the \"Land of the Long White Cloud\"?",
                             "Which strait separates Asia from North America?",
                             "What is the capital of Thailand?",
                             "In which country would you find the city of Vienna?",
                             "What is the largest lake in Africa?",
                             "Which mountain range runs along the western edge of South America?",
                             "What is the capital of Spain?",
                             "What is the capital of California?",
                             "Which river forms the eastern border of Texas?",
                             "What is the highest peak in the Rocky Mountains?",
                             "In which state would you find the Grand Canyon?",
                             "What is the largest state by land area in the U.S.?",
                             "Which Great Lake is the largest by surface area?",
                             "What is the capital of New York?",
                             "Which river flows through Chicago?",
                             "In which state is Yellowstone National Park located?",
                             "What is the capital of Florida?",
                             "Which state is known as the \"Sunflower State\"?",
                             "What is the highest mountain peak in the contiguous United States?",
                             "In which state would you find Denali (formerly known as Mount McKinley)?",
                             "What is the largest city in Texas?",
                             "Which river flows through New Orleans?",
                             "In which state is the Statue of Liberty located?",
                             "What is the capital of Illinois?",
                             "Which state is known as the \"Peach State\"?",
                             "What is the highest peak in Hawaii?",
                             "In which state would you find Bryce Canyon National Park?",
                             "What is the capital of Nevada?",
                             "Which river forms part of the border between Arizona and California?",
                             "In which state is the Great Smoky Mountains National Park located?",
                             "What is the largest city in Arizona?",
                             "Which state is known as the \"Last Frontier\"?",
                             "What is the highest peak in the Cascade Range?",
                             "In which state would you find Acadia National Park?",
                             "What is the capital of Colorado?",
                             "Which river flows through Portland, Oregon?",
                             "In which state is Mount Rushmore located?",
                             "What is the capital of France?",
                             "Which river flows through Budapest?",
                             "What is the largest island in the Mediterranean Sea?",
                             "In which country would you find the city of Athens?",
                             "Which mountain range runs along the border of France and Spain?",
                             "What is the capital of Germany?",
                             "Which river flows through Vienna?",
                             "In which country would you find the city of Prague?",
                             "Which island nation is located in the North Atlantic Ocean, known for its geothermal activity?",
                             "What is the capital of Italy?",
                             "Which river flows through Amsterdam?",
                             "In which country would you find the city of Dublin?",
                             "What is the largest country by land area in Europe?",
                             "Which mountain range forms the natural border between Europe and Asia?",
                             "What is the capital of Russia?",
                             "Which river flows through London?",
                             "In which country would you find the city of Warsaw?",
                             "Which country is known for its fjords and is located on the western coast of the Scandinavian Peninsula?",
                             "What is the capital of Spain?",
                             "Which river flows through Rome?",
                             "What is the capital of Japan?",
                             "Which river flows through Beijing?",
                             "What is the largest desert in Asia?",
                             "In which country would you find the city of Mumbai (formerly Bombay)?",
                             "Which mountain range stretches across northern India and into Nepal?",
                             "What is the capital of China?",
                             "Which river flows through Seoul?",
                             "In which country would you find the city of Bangkok?",
                             "Which Asian country is known as the \"Land of the Rising Sun\"?",
                             "What is the capital of India?",
                             "Which river is often referred to as the \"Cradle of Civilization\"?",
                             "In which country would you find the city of Riyadh?",
                             "Which Asian country is known as the \"Land of the Thunder Dragon\"?",
                             "What is the capital of South Korea?",
                             "Which river flows through Shanghai?",
                             "In which country would you find the city of Dubai?",
                             "Which Asian country is known as the \"Emerald Isle\"?",
                             "What is the capital of Thailand?",
                             "Which river forms the border between China and North Korea?",
                             "In which country would you find the city of Jakarta?",
                             "What is the capital of Egypt?",
                             "Which river is the longest in Africa?",
                             "What is the largest desert in Africa?",
                             "In which country would you find the city of Nairobi?",
                             "Which mountain range runs along the eastern edge of Africa?",
                             "What is the capital of Nigeria?",
                             "Which river flows through Kinshasa, the capital of the Democratic Republic of the Congo?",
                             "In which country would you find the city of Cape Town?",
                             "Which African country is known as the \"Land of a Thousand Hills\"?",
                             "What is the capital of South Africa?",
                             "Which river is the longest in the world?",
                             "What is the capital of Australia?",
                             "Which country is known as the Land of the Rising Sun?",
                             "Which desert is the largest in the world?",
                             "What is the highest mountain peak in North America?",
                             "In which country would you find the Amazon Rainforest?",
                             "Which African country is known as the \"Pearl of Africa\"?",
                             "What is the capital of New Zealand?"]
                    funni += angel
                    if message.guild.id == 1030490217855074304:
                        badescu_quotes = ["Badescu can divide by zero.",
                                        "Badescu counted to infinity. Twice.",
                                        "When Badescu enters a room, he doesn't turn the lights on; he turns the dark off.",
                                        "Badescu can slam a revolving door.",
                                        "Badescu can unscramble an egg.",
                                        "Badescu can hear sign language.",
                                        "Badescu can find the needle in the haystack and the haystack in the needle.",
                                        "Badescu can speak Braille.",
                                        "Badescu can win a game of Connect Four in three moves.",
                                        "When Badescu does push-ups, he doesn't push himself up; he pushes the Earth down.",
                                        "Badescu can make a happy meal cry.",
                                        "Badescu doesn't wear a watch; he decides what time it is.",
                                        "Badescu can build a snowman out of rain.",
                                        "Badescu doesn't need GPS; he is the direction.",
                                        "Badescu can unbreak broken glass.",
                                        "Badescu can hear your thoughts, but he's not interested.",
                                        "When Badescu does a push-up, he's not lifting himself up; he's pushing the Earth down.",
                                        "Badescu can delete the Recycling Bin.",
                                        "Badescu can un-invent the wheel.",
                                        "Badescu can divide by zero and get a valid answer.",
                                        "Badescu can pick oranges from an apple tree and make the best lemonade you've ever tasted.",
                                        "Badescu's tears can cure cancer. Too bad he has never cried.",
                                        "Badescu can win a game of chess with just one move: a roundhouse kick to the opponent's king.",
                                        "Badescu can hear a pin drop in a thunderstorm.",
                                        "Badescu can hear the sound of one hand clapping.",
                                        "Badescu can taste the rainbow.",
                                        "Badescu can hear silence.",
                                        "Badescu can turn water into wine, but he prefers beer.",
                                        "Badescu can hear you blinking.",
                                        "Badescu can slam a revolving door.",
                                        "Badescu can make a fire by rubbing two ice cubes together.",
                                        "Badescu can drown a fish.",
                                        "Badescu can breathe underwater, but he chooses not to, to give other fish a chance.",
                                        "Badescu doesn't do push-ups; he pushes the Earth down.",
                                        "Badescu can divide by zero.",
                                        "Badescu can build a snowman out of rain.",
                                        "Badescu can find the remote control without looking.",
                                        "Badescu can win a game of hide and seek in the dark.",
                                        "Badescu can slam a revolving door.",
                                        "Badescu can write a novel with a single letter.",
                                        "Badescu can make a snow angel in the desert.",
                                        "Badescu can grill a popsicle.",
                                        "Badescu can tie his shoes with his feet.",
                                        "Badescu can cut through a hot knife with butter.",
                                        "Badescu can uncook a scrambled egg.",
                                        "Badescu can speak braille.",
                                        "Badescu can unscramble scrambled eggs.",
                                        "Badescu can break the sound barrier with his silence.",
                                        "Badescu can make a volcano erupt by staring at it.",
                                        "Badescu can make onions cry.",
                                        "Badescu can slam a revolving door.",
                                        "Badescu can eat just one Lay's potato chip.",
                                        "Badescu can win a staring contest against the sun.",
                                        "Badescu can talk in Morse code.",
                                        "Badescu can play the violin with a piano.",
                                        "Badescu can fold a piece of paper more than seven times.",
                                        "Badescu can alphabetize a dictionary.",
                                        "Badescu can make a circle with a square.",
                                        "Badescu can cut a knife with butter.",
                                        "Badescu can make a snake laugh.",
                                        "Badescu can make a triangle with two sides.",
                                        "Badescu can unscramble a jigsaw puzzle in one second.",
                                        "Badescu can make a square dance in a round room.",
                                        "Badescu can jump off the ground and miss.",
                                        "Badescu can draw a perfect circle without a compass.",
                                        "Badescu can write a book without words.",
                                        "Badescu can color a rainbow with just one crayon.",
                                        "Badescu can solve a Rubik's Cube blindfolded... with his feet.",
                                        "Badescu can speak every language, including sign language.",
                                        "Badescu can ride a unicycle... with training wheels.",
                                        "Badescu can make a snowman out of sand.",
                                        "Badescu can eat soup with a fork.",
                                        "Badescu can make a cat bark.",
                                        "Badescu can make a pineapple pizza taste good.",
                                        "Badescu can walk on sunshine.",
                                        "Badescu can make a black hole blink.",
                                        "Badescu can make a tree fall in a forest and everyone will hear it.",
                                        "Badescu can make a mirror reflect on its life choices.",
                                        "Badescu can make a rock sweat.",
                                        "Badescu can make a triangle have four sides.",
                                        "Badescu can hear a pin drop in a thunderstorm.",
                                        "Badescu can hear the sound of one hand clapping.",
                                        "Badescu can taste the rainbow.",
                                        "Badescu can hear silence.",
                                        "Badescu can turn water into wine, but he prefers beer.",
                                        "Badescu can hear you blinking.",
                                        "Badescu can slam a revolving door.",
                                        "Badescu can make a fire by rubbing two ice cubes together.",
                                        "Badescu can drown a fish.",
                                        "Badescu can breathe underwater, but he chooses not to, to give other fish a chance.",
                                        "Badescu doesn't do push-ups; he pushes the Earth down.",
                                        "Badescu can divide by zero.",
                                        "Badescu can build a snowman out of rain.",
                                        "Badescu can find the remote control without looking.",
                                        "Badescu can win a game of hide and seek in the dark.",
                                        "Badescu can slam a revolving door.",
                                        "Badescu can write a novel with a single letter.",
                                        "Badescu can make a snow angel in the desert.",
                                        "Badescu can grill a popsicle.",
                                        "Badescu can tie his shoes with his feet.",
                                        "Badescu can cut through a hot knife with butter.",
                                        "Badescu can uncook a scrambled egg.",
                                        "Badescu can speak braille.",
                                        "Badescu can unscramble scrambled eggs.",
                                        "Badescu can break the sound barrier with his silence.",
                                        "Badescu can make a volcano erupt by staring at it.",
                                        "Badescu can make onions cry.",
                                        "Badescu can slam a revolving door.",
                                        "Badescu can eat just one Lay's potato chip."]
                        funni += badescu_quotes


                random = randint(0, (len(funni) - 1))
                chestie = funni[random]
                user_id = [556836294710525952, 1012877247956402257, 555455936760905780]
                if chestie == f"{name} stinks" and message.author.id in user_id:
                    await message.channel.send(f"{name} smells good. <:pepeloon:910540003828985926>", reference=message,
                                               mention_author=False)
                elif chestie == "ඞ":
                    random_amogus = randint(0, 100)
                    chestie *= random_amogus
                    await message.channel.send(f"{chestie}, *Amogus rolled: {random_amogus}*", reference=message,
                                               mention_author=False)
                else:
                    await message.channel.send(chestie, reference=message, mention_author=False)

            if "the" in masaj and "man" in masaj:
                if masaj.index("the") < masaj.index("man"):
                    await message.channel.send("Dave the man <:LETSFUCKINGGOO:901184486702710804>", reference=message,
                                               mention_author=False)
            if "becky" in masaj:
                await message.channel.send("My name is not Becky idiot", reference=message, mention_author=False)

            if "esketit" in masaj:
                await message.channel.send("https://tenor.com/view/lets-lets-get-it-gif-14167426", reference=message,
                                           mention_author=False)

            if "<@1135983715646976111>" in message.content.lower():
                reply = ["https://cdn.discordapp.com/emojis/1078009688366522580.gif", "I require professional help",
                         "My mental state is declining <a:kurukuru:1113242215083421707>"]
                random_reply = randint(0, (len(reply) - 1))
                await message.channel.send(reply[random_reply], reference=message, mention_author=True)

            if message.author.id == 763698307276079155 and "badescu" in message.content.lower():
                await message.channel.send("I love you too, cocalarule", reference=message, mention_author=False)

            if "Did you ever heard about our god and savior" in message.content:
                await message.channel.send("No I haven't, and leave me the fuck alone", reference=message, mention_author=False)
        

async def setup(bot):
    await bot.add_cog(Funni(bot))