# Import ?
import os
import json

import random

# py -3 -m pip install -U discord.py    
import discord
import logging

from pprint import pprint
from discord.ext import commands
from discord.ext.commands.core import before_invoke

# Import all files from the utilities folder
from utilities import *
from cmds import *

# pip install python-dotenv
from dotenv import load_dotenv
# Load the .env file
load_dotenv()
# Get a variable by it's name
liveToken = os.getenv("LIVETOKEN")
devToken = os.getenv("DEVTOKEN")


intents = discord.Intents.default()
intents.members = True

if config.devmode == True:
    defaultPrefix = config.devPrefix
else:
    defaultPrefix = config.defaultPrefix

bot = commands.Bot(
    command_prefix = "",
    activity = config.activity,
    status = discord.Status.dnd,
    intents = intents
    #help_command = None
)

#Initiate the bot
@bot.event 
async def on_ready():

    if config.devmode == True:
        print("DEVMODE IS ENABLED")

    else:

        with open("./utilities/serverInfo.json", "r") as infile:
            serverInfo = json.load(infile)

        for server in serverInfo:
            found = "f"

        for guild in bot.guilds:
            print(guild.name)
            # Update serverInfo.json on bot start

    print(f"{bot.user} has connected to Discord!")

    await bot.get_channel(791216444548579339).send(f"bot online")

@bot.event
async def on_guild_remove(guild):

    colour = 0xFF0000

    embed = discord.Embed(
        title = "Left a Server",
        color = colour,
        description = f"**Server Name:** {guild.name}\n**Server Owner:** <@{guild.owner_id}>\n**Member Count:** {guild.member_count}"
    ).set_thumbnail(
        url = guild.icon_url
    ).set_footer(
        text = f"{colour}"
    )

    await bot.get_channel(791216444548579339).send(embed = embed) 


@bot.event
async def on_guild_join(guild):

    # try:
    await bot.get_user(guild.owner_id).send(f"Thanks for adding me to your server! Please respond with what you would like my prefix to be within {guild.name}. You can change this later using the `prefix` command.")

    def check(msg):
        if msg.author.id == guild.owner_id:
            return True
        else:
            return False

    while True:
        x = await bot.wait_for("message", timeout = 120, check = check)

        if len(x.content) < 4:
            await bot.get_user(guild.owner_id).send(f"The prefix for {guild.name} is now `{x.content}`")

            infoDict = {f"{guild.id}": {
                "name": guild.name,
                "_id": guild.id,
                "ownerID": guild.owner_id,
                "prefix": x.content,
                "settings": {
                    "limited": False
                }
            }}

            break
        else:
            await bot.get_user(guild.owner_id).send(f"Please choose something with less than 3 characters.")




    # 1. Read file contents
    with open("./utilities/serverInfo.json", "r") as infile:
        data = json.load(infile)

    # 2. Update json object
    data.update(infoDict)

    # 3. Write json file
    with open("./utilities/serverInfo.json", "w") as outfile:
        json.dump(data, outfile, indent = 4)

    print("Successfully added a new server to serverInfo.json!")

    colour = 0x198754

    embed = discord.Embed(
        title = "New Server",
        color = colour,
        description = f"**Server Name:** {guild.name}\n**Server Owner:** <@{guild.owner_id}>\n**Member Count:** {guild.member_count}"
    ).set_thumbnail(
        url = guild.icon_url
    ).set_footer(
        text = f"{colour}"
    )

    await bot.get_channel(config.botStatusChannelId).send(embed = embed) 


@bot.event
async def on_message(message):

    # Reject other bots
    if message.author.bot == True:
        return

    if len(message.content) < 2:
        return

    if str(message.channel.type) == "private":
        
        if message.content.strip() in [f"<@{bot.user.id}>", f"<!@{bot.user.id}>"]:
            return await bot.get_channel(message.channel.id).send(f"You don't need to use a prefix in dms")

        if message.content.lower().startswith(defaultPrefix):
            message.content = message.content[len(defaultPrefix):]

        elif message.content.lower().startswith(f"<@{bot.user.id}>"):
            message.content = message.content[len(f"<@{bot.user.id}>"):]

        elif message.content.lower().startswith(f"<!@{bot.user.id}>"):
            message.content = message.content[len(f"<!@{bot.user.id}>"):]


    else:

        server = await s.findServerInfo(bot, message.guild.id)

        if message.content.strip() in [f"<@{bot.user.id}>", f"<!@{bot.user.id}>"]:
            return await bot.get_channel(message.channel.id).send(f"The prefixes you can use in this server are:\n> `{server['prefix']}`\n> `{defaultPrefix}`\n> or mention the bot")

        if message.content.lower().startswith(server['prefix']):
            message.content = message.content[len(server['prefix']):]

        elif message.content.lower().startswith(defaultPrefix):
            message.content = message.content[len(defaultPrefix):]

        elif message.content.lower().startswith(f"<@{bot.user.id}>"):
            message.content = message.content[len(f"<@{bot.user.id}>"):]

        elif message.content.lower().startswith(f"<!@{bot.user.id}>"):
            message.content = message.content[len(f"<!@{bot.user.id}>"):]

        else:
            return print(f"couldnt find a prefix in {server['name']}")

    if message.author.id in [180147146748723200]:
        if random.choice([1, 1, 2]) == 1:
            await bot.get_channel(message.channel.id).send(f"try again bitch")
            return

    message.content = message.content.strip()


        
    if message.author.id in config.blacklist:
        await bot.get_channel(message.channel.id).send(f"<@{message.author.id}>, you have been blacklisted from using this bot. If you believe this is a mistake then fuck you.")
        return

    # Process the message as a command, you must run this if you want to use @bot.commands with the on message event
    await bot.process_commands(message)

@bot.command(
    enabled = True,
    hidden = False,
    name = "example",
    aliases = ["ex"]
)
async def _example(ctx, *args):

    await ctx.send("good job")

    
@bot.command(
    enabled = True,
    hidden = False,
    name = "ping",
    aliases = [],
    usage = "",
    brief = "returns the ms it took for the bot to respond",
    help = f""
)
async def _pingCommand(ctx, *args):

    try:
        await ping.cmd(bot, ctx)
    except:
        await s.cmdFail(discord, config, ctx, bot, args)
        logging.exception('')
    else:
        await s.logCmd(discord, config, ctx, bot, args)

@bot.command(
    enabled = True,
    hidden = False,
    name = "prefix",
    aliases = [],
    usage = "<desired prefix>",
    brief = "changes the prefix for your current server",
    help = "Must have Admin Permissions within the guild to use it. Requires one argument. Must be used within a server. "
)
async def _prefixCommand(ctx, *args):

    if str(ctx.channel.type) == "private":
        return await ctx.send("You must use this command in a server.")

    try:
        await prefix.cmd(json, bot, ctx, args)
    except:
        await s.cmdFail(discord, config, ctx, bot, args)
        logging.exception('')
    else:
        await s.logCmd(discord, config, ctx, bot, args)

@bot.command(
    enabled = True,
    hidden = True,
    name = "leaveserver",
    aliases = ["leave"],
    usage = "<server_id>",
    brief = "makes the bot leave a specific server",
    help = "Owner only command. Makes the bot leave a specific server by ID and then removes it's entry from `serverInfo.json`."
)
async def _leaveServerCommand(ctx, *args):

    try:
        await leaveServer.cmd(discord, json, bot, ctx, args)    
    except:
        await s.cmdFail(discord, config, ctx, bot, args)
        logging.exception('')
    else:
        await s.logCmd(discord, config, ctx, bot, args)

# Start the bot
if config.devmode == True:
    bot.run(devToken)
else:
    bot.run(liveToken)
