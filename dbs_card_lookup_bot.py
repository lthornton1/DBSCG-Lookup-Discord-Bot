# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~ DBSCG Lookup Discord Bot ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~ Main python program for running bot a scrappers ~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import os
import discord
import re
import pandas as pd
import asyncio
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from imagescrape import cardImgScrape
from allsetscrape import cardDataScrape
from datetime import datetime


TOKEN = open('token.txt').read().splitlines()[0]
client = discord.Client()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Any time a message is recieved from client, check if it contains a bot command
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@client.event
async def on_message(message):

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~ Help Command, tells users how to use the bots commands ~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if '>>help' in message.content.lower():
        embed2 = discord.Embed(title="Need some help?",color=0x00ff00)
        embed2.add_field(name="Current list of commands", value="**[*your_input*]** - Will give you the info for the card that closest matches the given name", inline=False)
        embed2.set_thumbnail(url="https://yt3.ggpht.com/a/AATXAJx7L9bdQ0_hVrq8G0QkykKK7Y7LB__5mqRzYg=s288-c-k-c0xffffffff-no-rj-mo")
        await message.channel.send(embed=embed2)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~ Checks to see if the message has [] in them to trigger card search ~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if re.search(r'\[[^\[\]]+\]', message.content):
        cn = re.findall(r'\[[^\[\]]+\]',message.content)[0][1:-1]

        highest = process.extractOne(cn,[item[2] for item in s.names])
        cn = highest[0]
        type = getType(cn)
        if type[1] == 'LEADER':
            curid = s.leader[s.leader['bname'] == cn].iloc[0]['id']
            curitem = s.leader[s.leader['bname'] == cn].iloc[0]
            cururl = s.img[s.img['id'] == curid].iloc[0]['img']
            embed = discord.Embed(title=str(curitem['fname'])+' // '+cn,color=0x00ff00)
            iteminfofront="**Front Power:** "+str(curitem['fplv'])+" **Character:** "+str(curitem['fcname'])+" **Special Trait:** "+str(curitem['fspt'])+" **Era:** "+str(curitem['fename'])
            iteminfoback="**Back Power:** "+str(curitem['bplv'])+" **Character:** "+str(curitem['bcname'])+" **Special Trait:** "+str(curitem['bspt'])+" **Era:** "+str(curitem['bename'])
            embed.add_field(name="Card Info", value=iteminfofront+'\n'+iteminfoback, inline=False)
            embed.add_field(name="Front Effect", value=curitem['fskl'], inline=False)
            embed.add_field(name="Back Effect", value=curitem['bskl'], inline=False)
            embed.set_image(url=cururl)

        elif type[1] == 'BATTLE':
            curid = s.battle[s.battle['fname'] == cn].iloc[0]['id']
            curitem = s.battle[s.battle['fname'] == cn].iloc[0]
            cururl = s.img[s.img['id'] == curid].iloc[0]['img']
            embed = discord.Embed(title=cn,color=0x00ff00)
            iteminfo="**Energy:** "+str(curitem['energy'])+" **Power:** "+str(curitem['fplv'])+" **Combo Energy:** "+str(curitem['cenergy'])+" **Combo Power:** "+str(curitem['cpower'])+"\n**Character:** "+str(curitem['fcname'])+" **Special Trait:** "+str(curitem['fspt'])+" **Era:** "+str(curitem['fename'])
            embed.add_field(name="Card Info", value=iteminfo, inline=False)
            embed.add_field(name="Effect", value=curitem['fskl'], inline=False)
            embed.set_image(url=cururl)

        elif type[1] == 'EXTRA':
            curid = s.extra[s.extra['fname'] == cn].iloc[0]['id']
            curitem = s.extra[s.extra['fname'] == cn].iloc[0]
            cururl = s.img[s.img['id'] == curid].iloc[0]['img']
            embed = discord.Embed(title=cn,color=0x00ff00)
            embed.add_field(name="Effect", value=curitem['fskl'], inline=False)
            embed.set_image(url=cururl)

        await message.channel.send(embed=embed)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~ Admin Only Commands ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~ Set a specific channel in your server to accept admin commands ~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    channel = client.get_channel(int(open('adminchannel.txt').read().splitlines()[0]))
    if '>>logout' in message.content.lower() and channel == message.channel:
        print("Logging out!")
        exit(0)

    if '>>run' in message.content.lower() and channel == message.channel:
        print("Manually Running Scraper")
        s.runTheScraper()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~ Sets help command as game the bot is playing ~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    activity = discord.Game(name=">>help for commands")
    await client.change_presence(status=discord.Status.idle, activity=activity)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~ Runs a background_loop that runs the scrapper every midnight ~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
async def background_loop():
    print("waiting on client...")
    await client.wait_until_ready()
    print("client ready!")

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        if current_time == '00:00':
            s.runTheScraper()
        await asyncio.sleep(60)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~ Helper function to make finding cards by type easier ~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getType(goal):
    for i in s.names:
        if i[2] == goal:
            return i

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~ Class that holds all of the loaded card data ~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class scraper:
    def __init__(self):
        self.leader_df = ['id', 'type2', 'fname', 'bname', 'cname', 'sname', 'rname', 'fplv', 'bplv', 'fcname','bcname','fspt','bspt','fename','bename','rdate','fskl','bskl']
        self.battle_df = ['id', 'type2', 'fname', 'cname', 'sname', 'rname', 'fplv', 'fcname','fspt','fename','rdate','fskl','energy','cenergy','cpower']
        self.extra_df = ['id', 'type2', 'fname', 'cname', 'sname', 'rname', 'rdate','fskl','energy']
        self.img_df = ['id', 'img']

    def runTheScraper(self):
        cardImgScrape()
        cardDataScrape()
        print("scaper run")
        self.leader = pd.read_csv("csv/leader.csv",skipinitialspace=True,usecols=self.leader_df)
        self.extra = pd.read_csv("csv/extra.csv",skipinitialspace=True,usecols=self.extra_df)
        self.battle = pd.read_csv("csv/battle.csv",skipinitialspace=True,usecols=self.battle_df)
        self.img = pd.read_csv("csv/cardimg.csv",skipinitialspace=True,usecols=self.img_df)

        self.names = []
        namelist = self.battle['fname']
        for x in range(0,len(namelist)-1):
            self.names.append((self.battle['id'][x],self.battle['type2'][x],namelist[x]))
        namelist = self.leader['bname']
        for x in range(0,len(namelist)-1):
            self.names.append((self.leader['id'][x],self.leader['type2'][x],namelist[x]))
        namelist = self.extra['fname']
        for x in range(0,len(namelist)-1):
            self.names.append((self.extra['id'][x],self.extra['type2'][x],namelist[x]))


s = scraper()
s.runTheScraper()
client.loop.create_task(background_loop())
client.run(TOKEN)
