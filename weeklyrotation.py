import discord,asyncio,os
from datetime import datetime, timedelta, date
from discord.ext import commands, tasks
from urllib import parse, request
import re
import sys
from dateutil.relativedelta import *

bot = commands.Bot(command_prefix='>', description="This is a Helper Bot")

#This script is scheduled to run via task scheduled every other Wednesday. In progress to migarte this script to the main script (seagullbot & commands)
@client.event
async def on_ready():                                   # Upon starting script, posts on the CMD screen the following messages below
    datee = str(datetime.date(datetime.now() + timedelta(days=14)))
    dateee = str(datetime.date(datetime.now() + timedelta(days=15)))
    result2 = datee + " at 7pm EST"
    result3 = datee + " at 12am BST"
    
    with open('nestrotatedate_easterntime.txt', 'w') as file:
        file.write(str(result2).replace("'",""))
    with open('nestrotatedate_gmtime.txt', 'w') as file:
        file.write(str(result3).replace("'",""))
    
    # SEND ROTATION MESSAGE TO DISCORD
    todayy = str(date.today())
    location1 = 000000000000000000 #channel id of location 1
    location2 = 000000000000000000 #channel id of location 2
    location3 = 000000000000000000 #channel id of location 3
    location4 = 000000000000000000 #channel id of location 4
    location5 = 000000000000000000 #channel id of location 5
    location6 = 000000000000000000 #channel id of location 6
    location7 = 000000000000000000 #channel id of location 7
    channel1 = client.get_channel(location1) #Lexington
    channel11 = client.get_channel(location2) #Lexington
    channel2 = client.get_channel(location3) #Georgetown
    channel22 = client.get_channel(location4) #Georgetown
    channel3 = client.get_channel(location5) #Frankfort
    channel33 = client.get_channel(location6) #Frankfort
    channel4 = client.get_channel(location7) #SL3
    await channel1.purge(limit=1)
    await channel2.purge(limit=1)
    await channel3.purge(limit=1)
    await channel4.purge(limit=1)
    embedVar = discord.Embed(title="Bi-Weekly Nest Rotation\n*" + todayy + "*", description="The normal bi-weekly nest rotation has happened. To report a nest, please use the `/report-nest` command. For further help, use the `/help` command.", color=0x50BFE6)
    await channel1.send(embed=embedVar)
    await channel2.send(embed=embedVar)
    await channel3.send(embed=embedVar)
    await channel4.send(embed=embedVar)
    await channel11.send(embed=embedVar)
    await channel22.send(embed=embedVar)
    await channel33.send(embed=embedVar)
    embedVar = discord.Embed(title="Bi-Weekly Nest Rotation\n*" + todayy + "*", description="The normal bi-weekly nest rotation has happened. Post in this channel to report a nest using the `/report-nest` command.", color=0x50BFE6)
    file = open('lexnest.txt', 'w')
    file.close()
    file = open('franknest.txt', 'w')
    file.close()
    file = open('georgenest.txt', 'w')
    file.close()
    file = open('datchetnest.txt', 'w')
    file.close()
    file = open('sloughnest.txt', 'w')
    file.close()
    file = open('windsornest.txt', 'w')
    file.close()
    sys.exit()
    
bot.run('PUBLIC_KEY_GOES_HERE') # Add bot token here
    
    
