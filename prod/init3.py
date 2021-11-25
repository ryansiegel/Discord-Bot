import discord,asyncio,os
from datetime import datetime, timedelta, date
from discord.ext import commands, tasks
from discord.utils import get
from urllib import parse, request
import re
from importlib import reload
import commands as mod
from dislash import *
from enum import Enum

bot = commands.Bot(command_prefix='!', description="This is a Helper Bot")
inter_client = InteractionClient(bot)
    
#this is items for the bot to do when waking up
@bot.event
async def on_ready(): 
    print('We have logged in as {0.user}'.format(bot))
    channelAliveID = 000000000000000000 #channel id of where to post the awake messages
    aliveChannel = bot.get_channel(channelAliveID) #gets the channel to post the hourly awake messages in
    currentTime = str(datetime.now())[:-10] #posts date and time in hh:mm
    await aliveChannel.send('Bot restarted - ' + currentTime) #lets me know the bot has restarted
    repeatTasks.start() #start up the tasks that repeat daily
    await asyncio.sleep(60)
    stayAlive.start() #starts up the alive messages for me to monitor the bot

#this posts monitoring messages to make sure the bot is still awake and running
@tasks.loop(seconds=3600) #repeats every 1 hour
async def stayAlive():
    channelAliveID = 000000000000000000 #channel id of where to post the awake messages
    aliveChannel = bot.get_channel(channelAliveID) #gets the channel to post the hourly awake messages in
    currentTime = str(datetime.now())[:-10] #posts date and time in hh:mm
    print('Bot is alive - ' + currentTime) #prints in the bot server for me to monitor
    await aliveChannel.send('Bot is alive - ' + currentTime) #prints in the bot discord for me to monitor

#this is items for the bot to do when added to a discord server
@bot.event
async def on_guild_join(guild):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    await mod.joinServer(guild, channelPrint) #run the joinServer method in commands file

#this runs anytime there is a message in a discord server
@bot.event
async def on_message(message):
    if message.author == bot.user: #ignores messages from bots
        return
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    await mod.allIf(message, bot, channelPrint) #run the allIf method in commands file

#this runs the repeating tasks that post / do items in the discord servers
@tasks.loop(seconds=86400) #repeats every 12 hours
async def repeatTasks():
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    await mod.repeatTask(bot, channelPrint) #run the repeatTask method in commands file

'''
The below are all what is called slash commands. These commands use the prefix / and bring up info on the command inside discord.
'''
#facts command
@inter_client.slash_command(
    description="Generate a random fact!",
    options=[
        Option(
            "facts",
            description="Generate a random fact!",
            type=OptionType.STRING,
            required=True,
            choices=[
                OptionChoice("bidoof", "Bidoof"),
                OptionChoice("seagull", "Seagull"),
            ],
        )
    ]
)
async def facts(inter, facts):
    channelPrint = bot.get_channel(870534414692663356)
    reload(mod)
    await mod.facts(inter, channelPrint, bot, facts)
    
#help command
@inter_client.slash_command(
    description="Get help on the different commands the bot offers",
    options=[
        Option(
            "commands",
            description="Chose a command below to get info on what that command does.",
            type=OptionType.STRING,
            required=True,
            choices=[
                OptionChoice("advance-round", "advance"),
                OptionChoice("close-dispute", "closedispute"),
                OptionChoice("dispute", "dispute"),
                OptionChoice("ditto-disguises", "ditto"),
                OptionChoice("facts", "facts"),
                OptionChoice("friends", "friends"),
                OptionChoice("nest-pool", "nestpool"),
                OptionChoice("report-nest", "reportnest"),
                OptionChoice("set", "set"),
                OptionChoice("start-round", "startround"),
                OptionChoice("toggle", "toggle"),
            ],
        )
    ]
)
async def help(inter, commands):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    await mod.help(inter, channelPrint, bot, commands)


#report command
@inter_client.slash_command(
    name="report-nest", description="Reports a nest. -- NOTE: Action only available for Central KY servers and Slough server.",
    options=[
        Option("location", "Enter the nest location", OptionType.STRING, required=True),
        Option("pokemon", "Enter the nesting Pokemon", OptionType.STRING, required=True)
    ]
)
async def report(inter, location, pokemon):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    await mod.report(inter, location, pokemon, channelPrint, bot)

#dispute command
@inter_client.slash_command(
    description="Alerts the tournament staff of a dispute and creates a private channel to discuss the issue.",
    options=[
        Option("opponent", "Tag your opponent", OptionType.USER, required=True),
    ]
)
async def dispute(inter, opponent):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    await mod.dispute(inter, channelPrint, bot, opponent)

#end dispute command
@inter_client.slash_command(name="close-dispute", description="Closes the dispute channel. -- NOTE: Action can only be used by admins or to's.") 
async def closedispute(inter):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    await mod.enddispute(inter, channelPrint, bot)

#advance round command
@inter_client.slash_command(name="advance-round", description="Notifies tournament staff to advance the round.") 
async def advance(inter):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    await mod.advance(inter, channelPrint, bot)

#nest pool command
@inter_client.slash_command(name="nest-pool", description="Lists the current Pokemon that can nest.") 
async def nestpool(inter):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    await mod.nestpool(inter, channelPrint, bot)

#ditto disguises command    
@inter_client.slash_command(name="ditto-disguises", description="Lists the current Pokemon that can be disguised as ditto.") 
async def ditto(inter):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    await mod.ditto(inter, channelPrint, bot)

#toggle command
@inter_client.slash_command(description="Turns on or off certain actions for Seagull Bot. -- NOTE: Action can only be used by admins.")
@has_permissions(administrator=True)
async def toggle(inter): 
    pass
@toggle.sub_command_group(name="verify-alerts")
async def toggleone(inter):
    pass
@toggleone.sub_command(name="on", description="Sets the 'verify profile' alerts action on.", options=[Option("channel", "Set channel.", OptionType.CHANNEL, required=True)])
async def onone(inter, channel):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    currentSet = 1
    await mod.toggleon(inter, channelPrint, bot, channel, currentSet)
@toggleone.sub_command(name="off", description="Sets the 'verify profile' alerts action off.")
async def offone(inter):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    currentSet = 1
    await mod.toggleoff(inter, channelPrint, bot, currentSet)
@toggle.sub_command_group(name="friend-alerts")
async def toggletwo(inter):
    pass
@toggletwo.sub_command(name="on", description="Sets the 'add friends to database' alerts action on.", options=[Option("channel", "Set channel.", OptionType.CHANNEL, required=True)])
async def onone(inter, channel):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    currentSet = 2
    await mod.toggleon(inter, channelPrint, bot, channel, currentSet)
@toggletwo.sub_command(name="off", description="Sets the 'add friends to database' alerts action off.")
async def offone(inter):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    currentSet = 2
    await mod.toggleoff(inter, channelPrint, bot, currentSet)
@toggle.sub_command_group(name="leaderboard-refresh")
async def togglethree(inter):
    pass
@togglethree.sub_command(name="on", description="Sets the PokeNav 'leaderboard' refresh action on.", options=[Option("channel", "Set channel.", OptionType.CHANNEL, required=True)])
async def onthree(inter, channel):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    currentSet = 3
    await mod.toggleon(inter, channelPrint, bot, channel, currentSet)
@togglethree.sub_command(name="off", description="Sets the PokeNav 'leaderboard' refresh action off.")
async def offthree(inter):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    currentSet = 3
    await mod.toggleoff(inter, channelPrint, bot, currentSet)
@toggle.error
async def toggle_error(inter, error):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    embedVar = discord.Embed(title="ERROR", description="The ***/toggle*** command was not used by a server admin. Please contact your server admin.", color=0x8B0000)
    await inter.reply(embed=embedVar)
    await channelPrint.send('Toggle command not used by an admin - ' + str(inter.guild.name) + ' - ' + str(inter.author) + '.') #send to seagulls discord

#set command
@inter_client.slash_command(description="Sets different things for Seagull Bot.")
@has_permissions(administrator=True)
async def set(inter): 
    pass
@set.sub_command(name="tourny-staff", description="Sets the 'tournament staff' role.", options=[Option("role", "Enter role.", OptionType.ROLE, required=True)])
async def set1(inter, role):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    currentSet = 1
    await mod.set(inter, channelPrint, bot, role, currentSet)
@set.sub_command(name="admin-channel", description="Sets the Seagull Bot 'admin' channel.", options=[Option("channel", "Set channel.", OptionType.CHANNEL, required=True)])
async def set2(inter, channel):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    currentSet = 2
    await mod.set(inter, channelPrint, bot, channel, currentSet)
@set.sub_command(name="friend-channel", description="Sets the 'add friends' channel.", options=[Option("channel", "Set channel.", OptionType.CHANNEL, required=True)])
async def set3(inter, channel):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    currentSet = 3
    await mod.set(inter, channelPrint, bot, channel, currentSet)
@set.sub_command(name="leaderboard-channel", description="Sets the PokeNav 'leaderboard' channel.", options=[Option("channel", "Set channel.", OptionType.CHANNEL, required=True)])
async def set4(inter, channel):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    currentSet = 4
    await mod.set(inter, channelPrint, bot, channel, currentSet)
@set.sub_command(name="verify-channel", description="Sets the PokeNav 'profile setup' channel.", options=[Option("channel", "Set channel.", OptionType.CHANNEL, required=True)])
async def set5(inter, channel):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    currentSet = 5
    await mod.set(inter, channelPrint, bot, channel, currentSet)
@set.error
async def set_error(inter, error):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    embedVar = discord.Embed(title="ERROR", description="The ***/set*** command was not used by a server admin. Please contact your server admin.", color=0x8B0000)
    await inter.reply(embed=embedVar)
    await channelPrint.send('Set command not used by an admin - ' + str(inter.guild.name) + ' - ' + str(inter.author) + '.') #send to seagulls discord
    
#friend command
@inter_client.slash_command(description="All things friend code related!")
async def friends(inter): 
    pass
@friends.sub_command(name="add-profile", description="Add your profile in the Friend Database.", options=[Option("ign", "Enter your in game name.", OptionType.STRING, required=True), Option("code", "Enter your friend code", OptionType.INTEGER, required=True)])
async def addfriend(inter, ign, code):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    await mod.addfriend(inter, channelPrint, bot, ign, code)
@friends.sub_command(name="search", description="Search for friends in the Friend Database", options=[Option("ign", "Enter the trainers in game name.", OptionType.STRING, required=True)])
async def searchfriend(inter, ign):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    await mod.searchfriend(inter, channelPrint, bot, ign)

#round timer command
@inter_client.slash_command(name="round-notices", description="Starts the round notice alerts.")
async def roundtimer(inter): 
    pass
@roundtimer.sub_command(name="start-extended", description="Starts the extended round notice alerts.", options=[Option("hours", "Enter the total hours in round", OptionType.INTEGER, required=True), Option("role", "Enter the role the tournament players are under.", OptionType.ROLE, required=True), Option("channel", "Enter the channel the tournament is under.", OptionType.CHANNEL, required=True), Option("silph", "Enter the Silph tournament code. This is the 4 character code after https://silph.gg/t/ in the url.", OptionType.STRING)])
async def extendedround(inter, hours, role, channel, silph="NONE"):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    if silph == "NONE":
        await mod.extendedround(inter, channelPrint, bot, hours, role, channel)
    else:
        await mod.extendedround(inter, channelPrint, bot, hours, role, channel, silph)
@roundtimer.sub_command(name="start-live", description="Starts the live round notice alerts.", options=[Option("minutes", "Enter the total minutes in round", OptionType.INTEGER, required=True), Option("role", "Enter the role the tournament players are under.", OptionType.ROLE, required=True), Option("channel", "Enter the channel the tournament is under.", OptionType.CHANNEL, required=True), Option("silph", "Enter the Silph tournament code. This is the 4 character code after https://silph.gg/t/ in the url.", OptionType.STRING)])
async def liveround(inter, minutes, role, channel, silph="NONE"):
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    reload(mod) #reloads the command file to be current in case of updates to the script
    if silph == "NONE":
        await mod.liveround(inter, channelPrint, bot, minutes, role, channel)
    else:
        await mod.liveround(inter, channelPrint, bot, minutes, role, channel, silph)
        
#tournament items command
@inter_client.slash_command(name="tournament-items", description="Items for tournament staff to use.")
async def roundtimer(inter): 
    pass
@roundtimer.sub_command(name="staff-dispute", description="Allows a staff member to open a dispute for two trainers.", options=[Option("trainer1", "Trainer one in the dispute.", OptionType.USER, required=True), Option("Trainer two in the dispute.", OptionType.USER, required=True)])
async def staffdispute(inter, trainer1, trainer2):
    reload(mod) #reloads the command file to be current in case of updates to the script
    channelTriggerID = 000000000000000000 #channel id of where to post the trigger messages
    channelPrint = bot.get_channel(channelTriggerID) #gets the channel to post the trigger messages in
    await mod.staffdispute(inter, channelPrint, bot, trainer1, trainer2)


bot.run('PUBLIC_KEY_GOES_HERE', bot=True, reconnect=True)
